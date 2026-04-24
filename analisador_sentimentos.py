"""
💭 SISTEMA DE ANÁLISE DE SENTIMENTOS E CATEGORIZAÇÃO

Detecta emoções e categoriza mensagens para melhor atendimento
"""

import json
from datetime import datetime

# ==================== ANÁLISE DE SENTIMENTO ====================

class AnalisadorSentimento:
    """Analisa sentimento das mensagens sem dependências externas"""
    
    def __init__(self):
        self.palavras_positivas = {
            'pt': ['ótimo', 'excelente', 'adorei', 'perfeito', 'amei', 'maravilhoso',
                   'incrível', 'fantástico', 'bom', 'legal', 'melhor', 'gosto'],
            'en': ['great', 'excellent', 'love', 'perfect', 'amazing', 'wonderful',
                   'incredible', 'fantastic', 'good', 'best', 'like'],
            'es': ['excelente', 'adoré', 'perfecto', 'maravilloso', 'increíble',
                   'fantástico', 'bueno', 'mejor', 'me gusta']
        }
        
        self.palavras_negativas = {
            'pt': ['péssimo', 'horrível', 'odeio', 'ruim', 'problema', 'erro',
                   'falha', 'decepção', 'chato', 'irritante', 'pior', 'raiva'],
            'en': ['terrible', 'horrible', 'hate', 'bad', 'problem', 'error',
                   'fail', 'disappointing', 'annoying', 'worst', 'angry'],
            'es': ['terrible', 'horrible', 'odio', 'malo', 'problema', 'error',
                   'decepción', 'annoying', 'peor']
        }
        
        self.palavras_neutras = {
            'pt': ['sim', 'não', 'ok', 'certo', 'verdade', 'talvez', 'entendi'],
            'en': ['yes', 'no', 'ok', 'right', 'true', 'maybe', 'understand'],
            'es': ['sí', 'no', 'ok', 'verdad', 'tal vez']
        }
        
        self.historico_sentimentos = {}
    
    def analisar(self, texto, idioma='pt'):
        """
        Analisa sentimento de um texto
        Retorna: (sentimento: 'positivo'|'negativo'|'neutro', score: -1 a 1)
        """
        texto = texto.lower().strip()
        
        palavras = texto.split()
        score_positivo = 0
        score_negativo = 0
        
        # Obter palavras do idioma
        positivas = self.palavras_positivas.get(idioma, self.palavras_positivas['pt'])
        negativas = self.palavras_negativas.get(idioma, self.palavras_negativas['pt'])
        
        # Contar palavras positivas e negativas
        for palavra in palavras:
            if palavra in positivas:
                score_positivo += 1
            elif palavra in negativas:
                score_negativo += 1
        
        # Calcular score geral (-1 a 1)
        if score_positivo + score_negativo == 0:
            score = 0
        else:
            score = (score_positivo - score_negativo) / (score_positivo + score_negativo)
        
        # Classificar sentimento
        if score > 0.3:
            sentimento = 'positivo'
        elif score < -0.3:
            sentimento = 'negativo'
        else:
            sentimento = 'neutro'
        
        return sentimento, score
    
    def registrar_sentimento(self, numero_usuario, texto, sentimento, score):
        """Registra sentimento para análise posterior"""
        if numero_usuario not in self.historico_sentimentos:
            self.historico_sentimentos[numero_usuario] = []
        
        self.historico_sentimentos[numero_usuario].append({
            'texto': texto,
            'sentimento': sentimento,
            'score': score,
            'timestamp': datetime.now().isoformat()
        })
    
    def obter_sentimento_medio(self, numero_usuario):
        """Calcula sentimento médio do usuário"""
        if numero_usuario not in self.historico_sentimentos:
            return None
        
        historico = self.historico_sentimentos[numero_usuario]
        if not historico:
            return None
        
        scores = [item['score'] for item in historico]
        media = sum(scores) / len(scores)
        
        if media > 0.3:
            sentimento_medio = 'positivo'
        elif media < -0.3:
            sentimento_medio = 'negativo'
        else:
            sentimento_medio = 'neutro'
        
        return {
            'sentimento': sentimento_medio,
            'score_medio': media,
            'total_mensagens': len(historico),
            'ultimas_mensagens': historico[-5:]
        }

# ==================== CATEGORIZADOR DE MENSAGENS ====================

class CategorizadorMensagens:
    """Categoriza mensagens para melhor roteamento"""
    
    def __init__(self):
        self.categorias = {
            'saudacao': {
                'palavras': ['oi', 'olá', 'opa', 'hey', 'hola', 'hello', 'hi', 'bom dia', 'boa tarde', 'boa noite'],
                'prioridade': 'baixa'
            },
            'informacao': {
                'palavras': ['horário', 'preço', 'endereço', 'localização', 'how', 'what', 'cuando', 'onde'],
                'prioridade': 'media'
            },
            'problema': {
                'palavras': ['problema', 'erro', 'bug', 'não funciona', 'issue', 'problema', 'help', 'ayuda'],
                'prioridade': 'alta'
            },
            'reclamacao': {
                'palavras': ['reclamação', 'insatisfeito', 'decepção', 'ruins', 'complaint', 'disappointed'],
                'prioridade': 'alta'
            },
            'elogio': {
                'palavras': ['excelente', 'perfeito', 'adorei', 'ótimo', 'excellent', 'perfect', 'love'],
                'prioridade': 'baixa'
            },
            'sugestao': {
                'palavras': ['sugestão', 'sugerir', 'melhorar', 'sugest', 'propose', 'propongo'],
                'prioridade': 'media'
            },
            'pagamento': {
                'palavras': ['pagamento', 'boleto', 'cartão', 'débito', 'crédito', 'payment', 'pago'],
                'prioridade': 'alta'
            },
            'urgente': {
                'palavras': ['urgente', 'emergência', 'rápido', 'imediato', 'urgent', 'emergency', 'asap'],
                'prioridade': 'critica'
            }
        }
        
        self.historico_categorias = {}
    
    def categorizar(self, texto):
        """
        Categoriza uma mensagem
        Retorna: (categoria, prioridade)
        """
        texto = texto.lower().strip()
        palavras = texto.split()
        
        categoria_encontrada = None
        melhor_score = 0
        
        # Procurar por cada categoria
        for cat_nome, cat_info in self.categorias.items():
            score = 0
            for palavra in cat_info['palavras']:
                if palavra in texto:
                    score += 1
            
            if score > melhor_score:
                melhor_score = score
                categoria_encontrada = cat_nome
        
        if categoria_encontrada is None:
            categoria_encontrada = 'geral'
            prioridade = 'baixa'
        else:
            prioridade = self.categorias[categoria_encontrada]['prioridade']
        
        return categoria_encontrada, prioridade
    
    def registrar_categoria(self, numero_usuario, texto, categoria, prioridade):
        """Registra categoria para análise"""
        if numero_usuario not in self.historico_categorias:
            self.historico_categorias[numero_usuario] = []
        
        self.historico_categorias[numero_usuario].append({
            'texto': texto,
            'categoria': categoria,
            'prioridade': prioridade,
            'timestamp': datetime.now().isoformat()
        })
    
    def obter_distribuicao_categorias(self, numero_usuario):
        """Mostra distribuição de categorias do usuário"""
        if numero_usuario not in self.historico_categorias:
            return None
        
        historico = self.historico_categorias[numero_usuario]
        distribuicao = {}
        
        for item in historico:
            cat = item['categoria']
            if cat not in distribuicao:
                distribuicao[cat] = 0
            distribuicao[cat] += 1
        
        return distribuicao
    
    def obter_itens_urgentes(self, numero_usuario=None):
        """Retorna mensagens urgentes"""
        urgentes = []
        
        if numero_usuario:
            historico = self.historico_categorias.get(numero_usuario, [])
        else:
            historico = []
            for items in self.historico_categorias.values():
                historico.extend(items)
        
        for item in historico:
            if item['prioridade'] == 'critica':
                urgentes.append(item)
        
        return sorted(urgentes, key=lambda x: x['timestamp'], reverse=True)

# ==================== INTEGRAÇÃO ====================

class AnalisadorCompleto:
    """Integra análise de sentimento e categorização"""
    
    def __init__(self):
        self.sentimento = AnalisadorSentimento()
        self.categorizador = CategorizadorMensagens()
    
    def analisar_completo(self, texto, numero_usuario=None, idioma='pt'):
        """Análise completa de uma mensagem"""
        
        # Análise de sentimento
        sent, score = self.sentimento.analisar(texto, idioma)
        
        # Categorização
        cat, prio = self.categorizador.categorizar(texto)
        
        # Registrar
        if numero_usuario:
            self.sentimento.registrar_sentimento(numero_usuario, texto, sent, score)
            self.categorizador.registrar_categoria(numero_usuario, texto, cat, prio)
        
        return {
            'texto': texto,
            'sentimento': sent,
            'score_sentimento': score,
            'categoria': cat,
            'prioridade': prio,
            'timestamp': datetime.now().isoformat()
        }
    
    def gerar_perfil_usuario(self, numero_usuario):
        """Gera perfil comportamental do usuário"""
        
        sentimento_medio = self.sentimento.obter_sentimento_medio(numero_usuario)
        distribuicao_cat = self.categorizador.obter_distribuicao_categorias(numero_usuario)
        
        return {
            'sentimento': sentimento_medio,
            'categorias': distribuicao_cat,
            'timestamp': datetime.now().isoformat()
        }
    
    def gerar_relatorio_admin(self):
        """Gera relatório para administradores"""
        
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'total_usuarios': len(self.sentimento.historico_sentimentos),
            'usuarios_com_problemas': [],
            'urgentes': self.categorizador.obter_itens_urgentes(),
            'sentimentos_por_usuario': {}
        }
        
        for numero, historico in self.sentimento.historico_sentimentos.items():
            media = self.sentimento.obter_sentimento_medio(numero)
            relatorio['sentimentos_por_usuario'][numero] = media
            
            # Flagar usuários com muitos sentimentos negativos
            if media and media['sentimento'] == 'negativo':
                relatorio['usuarios_com_problemas'].append({
                    'numero': numero,
                    'score_medio': media['score_medio']
                })
        
        return relatorio

# ==================== TESTE ====================

if __name__ == '__main__':
    print("🧪 Testando Análise de Sentimentos\n")
    
    analisador = AnalisadorCompleto()
    
    # Teste 1
    print("1️⃣ Teste Positivo:")
    resultado = analisador.analisar_completo(
        "Adorei! Vosso serviço é perfeito e excelente!",
        "5585999887766"
    )
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    print()
    
    # Teste 2
    print("2️⃣ Teste Negativo:")
    resultado = analisador.analisar_completo(
        "Que péssimo! Tem um problema terrível!",
        "5585999887766"
    )
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    print()
    
    # Teste 3
    print("3️⃣ Teste Urgente:")
    resultado = analisador.analisar_completo(
        "Tenho um problema urgente com meu pedido!",
        "5585999887766"
    )
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    print()
    
    # Teste 4
    print("4️⃣ Perfil do Usuário:")
    perfil = analisador.gerar_perfil_usuario("5585999887766")
    print(json.dumps(perfil, ensure_ascii=False, indent=2))
    print()
    
    # Teste 5
    print("5️⃣ Relatório Admin:")
    relatorio = analisador.gerar_relatorio_admin()
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    print()
    
    print("✅ Testes concluídos!")

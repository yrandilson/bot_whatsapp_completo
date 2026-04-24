"""
🌍 BOT WHATSAPP COM SUPORTE A MÚLTIPLAS LINGUAGENS
E CONTEXTO DE CONVERSA

Use este arquivo para substituir a função processar_mensagem() do bot principal
"""

from datetime import datetime
import json
import os

# ==================== SISTEMA DE LINGUAGEM ====================

IDIOMAS_SUPORTADOS = {
    'pt': {
        'nome': 'Português',
        'saudacao': 'Olá! 👋 Bem-vindo ao nosso bot.',
        'horario': '📅 Funcionamos de seg-sex 09:00-18:00\n⏰ Sábado: 10:00-14:00',
        'preco': '💰 Nossos preços:\n• Plano A: R$ 50\n• Plano B: R$ 100\n• Plano C: R$ 150',
        'menu': '📋 Menu Principal:\n1️⃣ Horário\n2️⃣ Preços\n3️⃣ Endereço\n4️⃣ Atendente\n5️⃣ Consultoria',
        'endereco': '📍 Endereço: Rua Principal, 123\nCidade, Estado\n☎️ (85) 3456-7890',
        'atendente': '👤 Conectando com atendente...\nTempo: 2 minutos',
        'consultoria': '🎯 Agende sua consultoria!\nClique: bit.ly/consultoria',
        'desconhecido': '❓ Não entendi. Digite "menu" para opções.',
        'idioma_changed': '✅ Idioma alterado para Português',
    },
    'en': {
        'nome': 'English',
        'saudacao': 'Hello! 👋 Welcome to our bot.',
        'horario': '📅 We operate Mon-Fri 09:00-18:00\n⏰ Saturday: 10:00-14:00',
        'preco': '💰 Our prices:\n• Plan A: $20\n• Plan B: $40\n• Plan C: $60',
        'menu': '📋 Main Menu:\n1️⃣ Hours\n2️⃣ Prices\n3️⃣ Address\n4️⃣ Support\n5️⃣ Consultation',
        'endereco': '📍 Address: Main Street, 123\nCity, State\n☎️ +1-555-0123',
        'atendente': '👤 Connecting to support...\nTime: 2 minutes',
        'consultoria': '🎯 Book your consultation!\nClick: bit.ly/consultation',
        'desconhecido': '❓ I did not understand. Type "menu" for options.',
        'idioma_changed': '✅ Language changed to English',
    },
    'es': {
        'nome': 'Español',
        'saudacao': '¡Hola! 👋 Bienvenido a nuestro bot.',
        'horario': '📅 Operamos de lunes a viernes 09:00-18:00\n⏰ Sábado: 10:00-14:00',
        'preco': '💰 Nuestros precios:\n• Plan A: €20\n• Plan B: €40\n• Plan C: €60',
        'menu': '📋 Menú Principal:\n1️⃣ Horario\n2️⃣ Precios\n3️⃣ Dirección\n4️⃣ Soporte\n5️⃣ Consulta',
        'endereco': '📍 Dirección: Calle Principal, 123\nCiudad, Estado\n☎️ +34-555-0123',
        'atendente': '👤 Conectando con soporte...\nTiempo: 2 minutos',
        'consultoria': '🎯 ¡Reserva tu consulta!\nHaz clic: bit.ly/consulta',
        'desconhecido': '❓ No entendí. Escribe "menu" para opciones.',
        'idioma_changed': '✅ Idioma cambiado a Español',
    }
}

# ==================== GERENCIADOR DE CONTEXTO ====================

class GerenciadorContexto:
    """Mantém contexto de conversas por usuário"""
    
    def __init__(self):
        self.conversas = {}
        self.carregar_conversas()
    
    def carregar_conversas(self):
        """Carrega histórico de conversas do arquivo"""
        try:
            if os.path.exists('conversas.json'):
                with open('conversas.json', 'r', encoding='utf-8') as f:
                    self.conversas = json.load(f)
        except:
            self.conversas = {}
    
    def salvar_conversas(self):
        """Salva histórico de conversas"""
        try:
            with open('conversas.json', 'w', encoding='utf-8') as f:
                json.dump(self.conversas, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def obter_contexto(self, numero_usuario):
        """Obtém contexto do usuário"""
        if numero_usuario not in self.conversas:
            self.conversas[numero_usuario] = {
                'idioma': 'pt',
                'nome': '',
                'historico': [],
                'primeira_vez': True,
                'mensagens_recebidas': 0,
                'data_inicio': datetime.now().isoformat()
            }
        return self.conversas[numero_usuario]
    
    def atualizar_contexto(self, numero_usuario, mensagem, resposta):
        """Atualiza contexto com nova mensagem"""
        contexto = self.obter_contexto(numero_usuario)
        
        contexto['historico'].append({
            'mensagem': mensagem,
            'resposta': resposta,
            'hora': datetime.now().isoformat()
        })
        
        # Manter apenas últimas 20 mensagens
        if len(contexto['historico']) > 20:
            contexto['historico'] = contexto['historico'][-20:]
        
        contexto['mensagens_recebidas'] += 1
        contexto['primeira_vez'] = False
        
        self.salvar_conversas()
    
    def obter_historico(self, numero_usuario, ultimas=5):
        """Retorna últimas N mensagens"""
        contexto = self.obter_contexto(numero_usuario)
        return contexto['historico'][-ultimas:]
    
    def definir_idioma(self, numero_usuario, idioma):
        """Define idioma do usuário"""
        contexto = self.obter_contexto(numero_usuario)
        if idioma in IDIOMAS_SUPORTADOS:
            contexto['idioma'] = idioma
            self.salvar_conversas()
            return True
        return False
    
    def definir_nome(self, numero_usuario, nome):
        """Define nome do usuário"""
        contexto = self.obter_contexto(numero_usuario)
        contexto['nome'] = nome
        self.salvar_conversas()

# Instância global
gerenciador = GerenciadorContexto()

# ==================== PROCESSADOR DE MENSAGENS AVANÇADO ====================

def processar_mensagem_avancado(texto_entrada, numero_usuario=None):
    """
    Versão avançada com suporte a múltiplos idiomas e contexto
    """
    
    # Obter contexto do usuário
    if numero_usuario:
        contexto = gerenciador.obter_contexto(numero_usuario)
        idioma = contexto['idioma']
        nome_usuario = contexto['nome']
    else:
        idioma = 'pt'
        contexto = None
    
    # Acessar strings do idioma
    strings = IDIOMAS_SUPORTADOS[idioma]
    
    texto_entrada = texto_entrada.lower().strip()
    resposta = None
    
    # ========== COMANDOS DE IDIOMA ==========
    if 'idioma' in texto_entrada or 'language' in texto_entrada or 'langue' in texto_entrada:
        resposta = """🌍 Idiomas disponíveis:
1️⃣ Português (pt)
2️⃣ English (en)
3️⃣ Español (es)

Digite: "português", "english" ou "español"
        """
    
    elif texto_entrada in ['português', 'pt', 'português']:
        if numero_usuario:
            gerenciador.definir_idioma(numero_usuario, 'pt')
        resposta = strings['idioma_changed']
    
    elif texto_entrada in ['english', 'en', 'english']:
        if numero_usuario:
            gerenciador.definir_idioma(numero_usuario, 'en')
        resposta = IDIOMAS_SUPORTADOS['en']['idioma_changed']
    
    elif texto_entrada in ['español', 'es', 'espanhol']:
        if numero_usuario:
            gerenciador.definir_idioma(numero_usuario, 'es')
        resposta = IDIOMAS_SUPORTADOS['es']['idioma_changed']
    
    # ========== COMANDOS DE SAUDAÇÃO ==========
    elif any(word in texto_entrada for word in ['oi', 'olá', 'opa', 'hey', 'hola', 'hi']):
        if nome_usuario:
            resposta = f"Olá {nome_usuario}! 👋 Bem-vindo de volta."
        else:
            resposta = strings['saudacao']
    
    # ========== COMANDOS DE INFORMAÇÃO ==========
    elif 'horário' in texto_entrada or 'horario' in texto_entrada or 'hours' in texto_entrada or 'hora' in texto_entrada:
        resposta = strings['horario']
    
    elif 'preço' in texto_entrada or 'precio' in texto_entrada or 'price' in texto_entrada or 'custa' in texto_entrada:
        resposta = strings['preco']
    
    elif 'endereço' in texto_entrada or 'endereco' in texto_entrada or 'address' in texto_entrada or 'dirección' in texto_entrada:
        resposta = strings['endereco']
    
    elif 'menu' in texto_entrada or 'menú' in texto_entrada or 'options' in texto_entrada:
        resposta = strings['menu']
    
    elif 'ajuda' in texto_entrada or 'help' in texto_entrada or 'ayuda' in texto_entrada:
        resposta = strings['menu']
    
    elif 'atendente' in texto_entrada or 'support' in texto_entrada or 'soporte' in texto_entrada or 'falar' in texto_entrada:
        resposta = strings['atendente']
    
    elif 'consultoria' in texto_entrada or 'consulta' in texto_entrada or 'consultation' in texto_entrada:
        resposta = strings['consultoria']
    
    # ========== CONTEXTO E HISTÓRICO ==========
    elif 'histórico' in texto_entrada or 'historial' in texto_entrada or 'history' in texto_entrada:
        if numero_usuario:
            historico = gerenciador.obter_historico(numero_usuario, ultimas=3)
            if historico:
                resposta = "📜 Últimas conversas:\n"
                for msg in historico:
                    resposta += f"Você: {msg['mensagem']}\nBot: {msg['resposta']}\n\n"
            else:
                resposta = "Nenhum histórico ainda."
        else:
            resposta = "Histórico não disponível."
    
    # ========== RESPOSTA PADRÃO ==========
    else:
        resposta = strings['desconhecido']
    
    # Atualizar contexto se disponível
    if numero_usuario and contexto and resposta:
        gerenciador.atualizar_contexto(numero_usuario, texto_entrada, resposta)
    
    return resposta

# ==================== FUNÇÕES AUXILIARES ====================

def obter_estatisticas_usuario(numero_usuario):
    """Retorna estatísticas do usuário"""
    contexto = gerenciador.obter_contexto(numero_usuario)
    
    return {
        'nome': contexto['nome'],
        'idioma': contexto['idioma'],
        'mensagens_recebidas': contexto['mensagens_recebidas'],
        'primeira_vez': contexto['primeira_vez'],
        'data_inicio': contexto['data_inicio'],
        'ultimas_mensagens': contexto['historico'][-5:]
    }

def resetar_usuario(numero_usuario):
    """Reseta contexto do usuário"""
    if numero_usuario in gerenciador.conversas:
        del gerenciador.conversas[numero_usuario]
        gerenciador.salvar_conversas()
        return True
    return False

def exportar_conversas():
    """Exporta todas as conversas em JSON"""
    return json.dumps(gerenciador.conversas, ensure_ascii=False, indent=2)

def gerar_relatorio():
    """Gera relatório de uso"""
    relatorio = {
        'total_usuarios': len(gerenciador.conversas),
        'usuarios': {}
    }
    
    for numero, contexto in gerenciador.conversas.items():
        relatorio['usuarios'][numero] = {
            'idioma': contexto['idioma'],
            'mensagens': contexto['mensagens_recebidas'],
            'primeira_vez': contexto['primeira_vez'],
        }
    
    return relatorio

# ==================== PARA USAR NO WHATSAPP_BOT.PY ====================

"""
No arquivo whatsapp_bot.py, na função webhook(), troque:

    resposta = processar_mensagem(mensagem_entrada)

Por:

    resposta = processar_mensagem_avancado(mensagem_entrada, numero_remetente)

E importe este arquivo:

    from bot_avancado import processar_mensagem_avancado
"""

# ==================== TESTE ====================

if __name__ == '__main__':
    print("🧪 Testando Bot Avançado\n")
    
    # Teste 1: Português
    print("1️⃣ Teste em Português:")
    resposta = processar_mensagem_avancado("oi", "5585999887766")
    print(f"Resposta: {resposta}\n")
    
    # Teste 2: Trocar idioma
    print("2️⃣ Teste - Trocar Idioma:")
    resposta = processar_mensagem_avancado("english", "5585999887766")
    print(f"Resposta: {resposta}\n")
    
    # Teste 3: English
    print("3️⃣ Teste em English:")
    resposta = processar_mensagem_avancado("hello", "5585999887766")
    print(f"Resposta: {resposta}\n")
    
    # Teste 4: Menu
    print("4️⃣ Teste Menu:")
    resposta = processar_mensagem_avancado("menu", "5585999887766")
    print(f"Resposta: {resposta}\n")
    
    # Teste 5: Histórico
    print("5️⃣ Teste Histórico:")
    resposta = processar_mensagem_avancado("histórico", "5585999887766")
    print(f"Resposta: {resposta}\n")
    
    # Teste 6: Estatísticas
    print("6️⃣ Estatísticas do Usuário:")
    stats = obter_estatisticas_usuario("5585999887766")
    print(f"Stats: {json.dumps(stats, indent=2, ensure_ascii=False)}\n")
    
    print("✅ Testes concluídos!")

╔════════════════════════════════════════════════════════════════════════╗
║      🚀 GUIA DE INTEGRAÇÃO - MÓDULOS AVANÇADOS DO BOT                ║
║                                                                        ║
║  Como integrar os novos módulos ao seu bot WhatsApp                  ║
╚════════════════════════════════════════════════════════════════════════╝

═════════════════════════════════════════════════════════════════════════
📦 NOVOS MÓDULOS CRIADOS
═════════════════════════════════════════════════════════════════════════

1. bot_avancado.py
   ├─ Múltiplas linguagens (PT, EN, ES)
   ├─ Contexto de conversa por usuário
   ├─ Histórico de mensagens
   └─ Gerenciador de contexto persistente

2. analisador_sentimentos.py
   ├─ Análise de sentimento (Positivo/Negativo/Neutro)
   ├─ Categorização de mensagens
   ├─ Detecção de urgência
   └─ Relatórios comportamentais

3. admin_dashboard.py
   ├─ Painel web em tempo real
   ├─ Estatísticas de usuários
   ├─ Gráficos e relatórios
   └─ APIs para integração

═════════════════════════════════════════════════════════════════════════
1️⃣ INTEGRAR BOT_AVANCADO.PY (Múltiplos Idiomas)
═════════════════════════════════════════════════════════════════════════

PASSO 1: Importar no whatsapp_bot.py
─────────────────────────────────────

No início do arquivo whatsapp_bot.py, adicione:

from bot_avancado import processar_mensagem_avancado

PASSO 2: Modificar a função webhook()
──────────────────────────────────────

Encontre a função webhook() no whatsapp_bot.py e troque:

    # ANTES:
    resposta = processar_mensagem(mensagem_entrada)
    
    # DEPOIS:
    resposta = processar_mensagem_avancado(mensagem_entrada, numero_remetente)

PASSO 3: Testar
────────────────

No testador web (http://localhost:5000/test), teste:

Mensagem: "english"
Resposta: ✅ Idioma alterado para English

Mensagem: "hello"
Resposta: Should be in English

Mensagem: "menu"
Resposta: Should show menu in English

RECURSOS DISPONÍVEIS:

✓ 3 idiomas suportados (português, english, español)
✓ Contexto persistente (nome, histórico)
✓ Histórico de 20 últimas mensagens
✓ Arquivo conversas.json com tudo salvo

COMANDOS NOVOS:

• "idioma" - Escolher idioma
• "português" - Mudar para português
• "english" - Mudar para english
• "español" - Mudar para español
• "histórico" - Ver últimas conversas

═════════════════════════════════════════════════════════════════════════
2️⃣ INTEGRAR ANALISADOR_SENTIMENTOS.PY
═════════════════════════════════════════════════════════════════════════

PASSO 1: Importar no whatsapp_bot.py
─────────────────────────────────────

from analisador_sentimentos import AnalisadorCompleto

analisador = AnalisadorCompleto()

PASSO 2: Usar na função webhook()
──────────────────────────────────

Antes de processar a mensagem, adicione:

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        mensagem_entrada = request.values.get('Body', '').strip()
        numero_remetente = request.values.get('From', '').strip()
        
        # NOVA ANÁLISE
        analise = analisador.analisar_completo(
            mensagem_entrada, 
            numero_remetente
        )
        
        # Log da análise
        print(f"Sentimento: {analise['sentimento']}")
        print(f"Categoria: {analise['categoria']}")
        print(f"Prioridade: {analise['prioridade']}")
        
        # Processar normalmente
        resposta = processar_mensagem_avancado(mensagem_entrada, numero_remetente)
        
        # ... resto do código ...

PASSO 3: Obter perfil do usuário
──────────────────────────────────

Em qualquer momento, para analisar um usuário:

perfil = analisador.gerar_perfil_usuario("5585999887766")
print(perfil)

Retorna:
{
  "sentimento": {
    "sentimento": "positivo",
    "score_medio": 0.45,
    "total_mensagens": 10
  },
  "categorias": {
    "informacao": 5,
    "saudacao": 3,
    "problema": 2
  }
}

PASSO 4: Gerar relatório admin
───────────────────────────────

relatorio = analisador.gerar_relatorio_admin()

Mostra:
- Usuários com problemas
- Mensagens urgentes
- Distribuição de sentimentos

═════════════════════════════════════════════════════════════════════════
3️⃣ INTEGRAR ADMIN_DASHBOARD.PY (Painel Web)
═════════════════════════════════════════════════════════════════════════

OPÇÃO A: Dashboard Separado (Recomendado)
──────────────────────────────────────────

Execute o dashboard em outro terminal:

$ python admin_dashboard.py

Acesse:
http://localhost:5001/dashboard

APIs disponíveis:
- http://localhost:5001/api/usuarios
- http://localhost:5001/api/estatisticas
- http://localhost:5001/api/usuario/<numero>
- http://localhost:5001/api/relatorio

OPÇÃO B: Integrado ao Bot Principal
────────────────────────────────────

No whatsapp_bot.py, adicione antes de app.run():

# Importar dashboard
from admin_dashboard import app_dashboard

# Registrar rotas
@app.route('/admin/dashboard')
def admin_dashboard_view():
    # Código do dashboard aqui
    pass

# Depois acesse em:
# http://localhost:5000/admin/dashboard

═════════════════════════════════════════════════════════════════════════
🎯 INTEGRAÇÃO COMPLETA (Exemplo Pronto)
═════════════════════════════════════════════════════════════════════════

Veja o arquivo whatsapp_bot_avancado.py para um exemplo completo
que integra tudo (múltiplos idiomas, análise de sentimentos, dashboard).

═════════════════════════════════════════════════════════════════════════
💾 ESTRUTURA DE ARQUIVOS APÓS INTEGRAÇÃO
═════════════════════════════════════════════════════════════════════════

meu_bot_whatsapp/
├── whatsapp_bot.py              # Bot principal (modificado)
├── bot_avancado.py              # Novo: Múltiplos idiomas
├── analisador_sentimentos.py     # Novo: Análise de sentimentos
├── admin_dashboard.py             # Novo: Painel web
├── conversas.json                # Arquivo gerado: histórico
├── requirements.txt
├── .env
├── run_bot.py
├── test_bot.py
└── ...

═════════════════════════════════════════════════════════════════════════
🧪 TESTANDO TUDO JUNTO
═════════════════════════════════════════════════════════════════════════

TESTE 1: Múltiplos Idiomas
─────────────────────────

$ python whatsapp_bot.py
# Abra http://localhost:5000/test

Mensagens:
✓ "oi" → Resposta em português
✓ "english" → Muda para English
✓ "hello" → Resposta em English
✓ "español" → Muda para español
✓ "hola" → Resposta em español

TESTE 2: Análise de Sentimentos
──────────────────────────────

$ python analisador_sentimentos.py
# Verá testes automatizados:
✓ Texto positivo detectado
✓ Texto negativo detectado
✓ Mensagem urgente categorizada

TESTE 3: Dashboard
────────────────

# Terminal 1:
$ python whatsapp_bot.py

# Terminal 2:
$ python admin_dashboard.py

# Abra:
http://localhost:5001/dashboard
# Veja estatísticas em tempo real

TESTE 4: Integração Completa
────────────────────────────

Edite whatsapp_bot.py com todas as integrações
$ python whatsapp_bot.py
# Abra http://localhost:5000/test
# Teste múltiplos idiomas
# Veja análise de sentimentos nos logs
# Acesse dashboard em outra aba

═════════════════════════════════════════════════════════════════════════
⚙️ CONFIGURAÇÕES AVANÇADAS
═════════════════════════════════════════════════════════════════════════

ADICIONAR MAIS IDIOMAS:

No bot_avancado.py, encontre IDIOMAS_SUPORTADOS e adicione:

'fr': {
    'nome': 'Français',
    'saudacao': 'Bonjour! 👋 Bienvenue...',
    'horario': '...',
    # ... etc
}

CUSTOMIZAR CATEGORIAS:

No analisador_sentimentos.py, encontre self.categorias e adicione:

'marketing': {
    'palavras': ['promoção', 'desconto', 'oferta'],
    'prioridade': 'media'
}

CONECTAR COM BANCO DE DADOS:

# Adicione ao bot_avancado.py:

import sqlite3

def salvar_conversa_bd(numero, mensagem, resposta):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO conversas (numero, mensagem, resposta, data)
        VALUES (?, ?, ?, ?)
    ''', (numero, mensagem, resposta, datetime.now()))
    conn.commit()
    conn.close()

═════════════════════════════════════════════════════════════════════════
🔍 TROUBLESHOOTING
═════════════════════════════════════════════════════════════════════════

"ModuleNotFoundError: No module named 'bot_avancado'"
→ Certifique-se que bot_avancado.py está na mesma pasta
→ Ou adicione ao sys.path

"conversas.json fica muito grande"
→ Implemente limpeza automática:
    if len(conversas[numero]['historico']) > 100:
        conversas[numero]['historico'] = conversas[numero]['historico'][-50:]

"Dashboard não carrega os dados reais"
→ Integre o analisador ao dashboard
→ Use APIs do bot para atualizar dados

"Análise de sentimentos não detecta idioma X"
→ Adicione palavras do idioma em analisador_sentimentos.py

═════════════════════════════════════════════════════════════════════════
📚 PRÓXIMOS PASSOS
═════════════════════════════════════════════════════════════════════════

1. Integrar múltiplos idiomas (bot_avancado.py) ✓
2. Adicionar análise de sentimentos ✓
3. Criar painel de admin ✓
4. Conectar com banco de dados (próxima fase)
5. Integrar com ChatGPT (próxima fase)
6. Sistema de notificações (próxima fase)
7. API pública (próxima fase)

═════════════════════════════════════════════════════════════════════════
✨ RESUMO
═════════════════════════════════════════════════════════════════════════

Você agora tem um bot profissional com:

✅ Múltiplos idiomas
✅ Análise de sentimentos
✅ Painel de administração
✅ Histórico de conversas
✅ Categorização de mensagens
✅ Detecção de urgência
✅ Relatórios comportamentais
✅ APIs prontas

Isso é suficiente para um bot enterprise!

═════════════════════════════════════════════════════════════════════════

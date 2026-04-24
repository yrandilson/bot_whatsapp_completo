"""
Bot WhatsApp Completo com Python
Responde mensagens automaticamente usando Twilio
"""

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações Twilio (você vai obter essas valores)
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'seu_account_sid')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'seu_auth_token')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+1234567890')

# Inicializa cliente Twilio
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ==================== LÓGICA DO BOT ====================

def processar_mensagem(texto_entrada):
    """
    Processa mensagem recebida e retorna resposta
    Adicione aqui a lógica do seu bot
    """
    
    texto_entrada = texto_entrada.lower().strip()
    
    # Exemplos de respostas automáticas
    if 'oi' in texto_entrada or 'olá' in texto_entrada or 'opa' in texto_entrada:
        return "Olá! 👋 Bem-vindo ao nosso bot. Como posso ajudar?"
    
    elif 'horário' in texto_entrada or 'funciona' in texto_entrada:
        return "📅 Funcionamos de seg-sex 09:00-18:00\n⏰ Sábado: 10:00-14:00"
    
    elif 'preço' in texto_entrada or 'custa' in texto_entrada or 'valor' in texto_entrada:
        return "💰 Nossos preços:\n• Plano A: R$ 50\n• Plano B: R$ 100\n• Plano C: R$ 150"
    
    elif 'endereço' in texto_entrada or 'localização' in texto_entrada:
        return "📍 Endereço: Rua Principal, 123\nCidade, Estado\n☎️ (85) 3456-7890"
    
    elif 'ajuda' in texto_entrada or 'menu' in texto_entrada:
        return """📋 Menu Principal:
1️⃣ Horário de funcionamento
2️⃣ Preços
3️⃣ Endereço
4️⃣ Falar com atendente
5️⃣ Consultoria

Digite: 'horário', 'preço', 'endereço', 'atendente' ou 'consultoria'"""
    
    elif 'atendente' in texto_entrada or 'falar' in texto_entrada:
        return "👤 Conectando com um atendente...\nTempo estimado: 2 minutos"
    
    elif 'consultoria' in texto_entrada or 'consulta' in texto_entrada:
        return "🎯 Agende sua consultoria gratuita!\nClique no link: bit.ly/consultoria"
    
    elif 'obrigado' in texto_entrada or 'valeu' in texto_entrada or 'thanks' in texto_entrada:
        return "De nada! 😊 Estamos sempre aqui para ajudar!"
    
    else:
        return """❓ Não entendi sua pergunta.
Digite 'menu' para ver as opções disponíveis ou 'atendente' para falar com uma pessoa."""

# ==================== ROTAS FLASK ====================

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    Webhook que recebe mensagens do WhatsApp
    """
    
    if request.method == 'GET':
        # Verificação do webhook (Twilio valida assim)
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'seu_verify_token')
        
        if token == VERIFY_TOKEN:
            return challenge
        return 'Token inválido', 403
    
    if request.method == 'POST':
        # Processa mensagem recebida
        mensagem_entrada = request.values.get('Body', '').strip()
        numero_remetente = request.values.get('From', '').strip()
        
        print(f"📨 Mensagem recebida de {numero_remetente}: {mensagem_entrada}")
        
        # Processa a mensagem
        resposta = processar_mensagem(mensagem_entrada)
        
        # Envia resposta de volta
        response = MessagingResponse()
        response.message(resposta)
        
        print(f"✅ Resposta enviada: {resposta}\n")
        
        return str(response)

@app.route('/', methods=['GET'])
def home():
    """Página inicial para teste"""
    return """
    <h1>🤖 Bot WhatsApp Online!</h1>
    <p>O bot está funcionando e pronto para receber mensagens.</p>
    <p>Webhook em: <code>/webhook</code></p>
    """

# ==================== TESTE LOCAL ====================

@app.route('/test', methods=['GET', 'POST'])
def test():
    """Rota para testar o bot sem WhatsApp"""
    
    if request.method == 'POST':
        mensagem = request.form.get('mensagem', '')
        resposta = processar_mensagem(mensagem)
        return f"""
        <h2>Resultado do Teste</h2>
        <p><strong>Mensagem:</strong> {mensagem}</p>
        <p><strong>Resposta:</strong> {resposta}</p>
        <hr>
        <a href='/test'><button>Testar novamente</button></a>
        """
    
    return """
    <h2>🧪 Testador de Bot</h2>
    <form method='POST'>
        <input type='text' name='mensagem' placeholder='Digite uma mensagem...' required>
        <button type='submit'>Testar</button>
    </form>
    """

# ==================== FUNÇÃO PARA ENVIAR MENSAGEM ====================

def enviar_mensagem_manual(numero_destino, mensagem):
    """
    Envia mensagem manualmente (útil para notificações)
    numero_destino: ex: 'whatsapp:+5585999887766'
    """
    try:
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=numero_destino,
            body=mensagem
        )
        print(f"✅ Mensagem enviada! ID: {msg.sid}")
        return msg.sid
    except Exception as e:
        print(f"❌ Erro ao enviar: {str(e)}")
        return None

# ==================== EXECUÇÃO ====================

if __name__ == '__main__':
    print("🚀 Bot WhatsApp iniciado!")
    print("📍 Teste local: http://localhost:5000/test")
    print("🔗 Webhook: http://localhost:5000/webhook")
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
🚀 EXEMPLOS AVANÇADOS - Bot WhatsApp

Copie e cole esses exemplos no seu whatsapp_bot.py para adicionar funcionalidades!
"""

# ==================== EXEMPLO 1: BOT COM BANCO DE DADOS ====================

"""
Salvar histórico de conversas
Instale: pip install sqlite3 (já vem com Python)
"""

import sqlite3
from datetime import datetime

def inicializar_banco():
    '''Cria banco de dados se não existir'''
    conn = sqlite3.connect('bot_conversas.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY,
            numero TEXT,
            mensagem TEXT,
            resposta TEXT,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_conversa(numero, mensagem, resposta):
    '''Salva conversa no banco'''
    conn = sqlite3.connect('bot_conversas.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO mensagens (numero, mensagem, resposta, data)
        VALUES (?, ?, ?, ?)
    ''', (numero, mensagem, resposta, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    print(f"💾 Conversa salva no banco de dados")

# Adicione isso no webhook:
# salvar_conversa(numero_remetente, mensagem_entrada, resposta)


# ==================== EXEMPLO 2: BOT COM IA (ChatGPT) ====================

"""
Usar ChatGPT para respostas inteligentes
Instale: pip install openai
"""

import openai

def resposta_com_ia(mensagem):
    '''Gera resposta com ChatGPT'''
    try:
        openai.api_key = "sua-chave-openai-aqui"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Você é um assistente de atendimento ao cliente amigável e útil"
                },
                {
                    "role": "user",
                    "content": mensagem
                }
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        return f"Desculpe, erro ao processar: {str(e)}"

# Use assim em processar_mensagem():
# return resposta_com_ia(texto_entrada)


# ==================== EXEMPLO 3: BOT COM AGENDAMENTO ====================

"""
Integrar agendamentos
Instale: pip install google-calendar-simple-api
"""

from datetime import datetime, timedelta

# Banco de dados simples para agendamentos
agendamentos = {}

def agendar_consulta(numero, data_hora, nome):
    '''Agenda uma consulta'''
    try:
        agendamentos[numero] = {
            'nome': nome,
            'data': data_hora,
            'status': 'confirmado'
        }
        return f"✅ Consulta agendada para {data_hora}\nConfirmação enviada!"
    except:
        return "❌ Erro ao agendar. Tente novamente."

def verificar_agendamentos(numero):
    '''Verifica agendamentos do usuário'''
    if numero in agendamentos:
        agenda = agendamentos[numero]
        return f"📅 Sua consulta está marcada para {agenda['data']}"
    return "Você não tem consultas agendadas."

# Use assim:
# if 'agendar' in texto_entrada:
#     return "Qual data você prefere? (formato: DD/MM/YYYY HH:MM)"


# ==================== EXEMPLO 4: BOT COM IMAGENS ====================

"""
Enviar imagens e mídia
"""

from twilio.twiml.messaging_response import MessagingResponse

def enviar_resposta_com_midia():
    '''Exemplo de como enviar imagem'''
    
    response = MessagingResponse()
    
    # Adicionar texto
    response.message("Confira nosso catálogo de produtos!")
    
    # Adicionar imagem
    response.message(
        media_url="https://example.com/imagem.jpg"
    )
    
    # Adicionar vídeo
    response.message(
        media_url="https://example.com/video.mp4"
    )
    
    return str(response)


# ==================== EXEMPLO 5: BOT COM ANÁLISE DE SENTIMENTO ====================

"""
Detectar emoções nas mensagens
Instale: pip install textblob
"""

from textblob import TextBlob

def analisar_sentimento(mensagem):
    '''Analisa se a mensagem é positiva/negativa'''
    blob = TextBlob(mensagem)
    polaridade = blob.sentiment.polarity
    
    if polaridade > 0.1:
        return "😊 Mensagem positiva detectada"
    elif polaridade < -0.1:
        return "😞 Parece que você está insatisfeito. Posso ajudar?"
    else:
        return "😐 Mensagem neutra"

# Use em processar_mensagem():
# if 'problema' in texto_entrada or 'bug' in texto_entrada:
#     return analisar_sentimento(texto_entrada)


# ==================== EXEMPLO 6: BOT COM BUSCA NA INTERNET ====================

"""
Buscar informações na internet
Instale: pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup

def buscar_informacao(termo):
    '''Busca simples na internet (exemplo com Wikipedia)'''
    try:
        url = f"https://pt.wikipedia.org/w/api.php?action=query&titles={termo}&prop=extracts&explaintext=True&formatjson"
        
        resposta = requests.get(url)
        dados = resposta.json()
        
        # Extrair texto
        pages = dados['query']['pages']
        for page in pages.values():
            if 'extract' in page:
                texto = page['extract'][:300]  # Primeiros 300 caracteres
                return texto + "..."
        
        return "Não encontrei informações sobre isso."
    
    except:
        return "Erro ao buscar informações."

# Use assim:
# if 'busca' in texto_entrada or 'o que é' in texto_entrada:
#     termo = texto_entrada.replace('busca ', '')
#     return buscar_informacao(termo)


# ==================== EXEMPLO 7: BOT COM NOTIFICAÇÕES AGENDADAS ====================

"""
Enviar mensagens em horários específicos
Instale: pip install schedule
"""

import schedule
import threading
import time

def notificacao_diaria():
    '''Envia notificação diária'''
    print("📢 Enviando notificação diária...")
    # Adicione código para enviar via Twilio

def agendar_notificacoes():
    '''Agenda notificações'''
    schedule.every().day.at("09:00").do(notificacao_diaria)
    schedule.every().day.at("15:00").do(notificacao_diaria)
    
    def executor():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    thread = threading.Thread(executor, daemon=True)
    thread.start()

# Chame no __main__:
# agendar_notificacoes()


# ==================== EXEMPLO 8: BOT COM MENU INTERATIVO ====================

"""
Menu com botões (alguns clientes WhatsApp suportam)
"""

def menu_interativo():
    '''Exemplo de resposta com formatação de menu'''
    
    menu = """
🎯 *MENU PRINCIPAL*

*1️⃣ Produtos*
Veja nosso catálogo completo

*2️⃣ Promoções*
Ofertas especiais desta semana

*3️⃣ Atendimento*
Fale com um especialista

*4️⃣ Minha Conta*
Gerencie sua conta

_Digite o número da opção desejada_
    """
    
    return menu

# Use assim:
# if 'menu' in texto_entrada:
#     return menu_interativo()


# ==================== EXEMPLO 9: BOT COM FEEDBACK ====================

"""
Sistema de avaliação de atendimento
"""

avaliacoes = {}

def coletar_feedback(numero, mensagem):
    '''Coleta feedback do usuário'''
    
    if 'avalie' in mensagem.lower():
        return """
⭐ *Ajudei você?*

Reaja com:
😞 - Péssimo
😕 - Ruim  
😐 - Neutro
😊 - Bom
😍 - Ótimo

Digite a reação para enviar seu feedback!
        """
    
    # Salvar avaliação
    if mensagem in ['😞', '😕', '😐', '😊', '😍']:
        avaliacoes[numero] = {
            'reacao': mensagem,
            'data': datetime.now()
        }
        return "✅ Obrigado pela sua avaliação!"

# Use em processar_mensagem()


# ==================== EXEMPLO 10: BOT COM INTEGRAÇÃO STRIPE ====================

"""
Aceitar pagamentos
Instale: pip install stripe
"""

import stripe

def processar_pagamento(quantidade, email):
    '''Processa pagamento via Stripe'''
    
    stripe.api_key = "sua-chave-stripe"
    
    try:
        # Criar sessão de pagamento
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': 'Serviço do Bot',
                    },
                    'unit_amount': quantidade * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://seusite.com/sucesso',
            cancel_url='https://seusite.com/cancelado',
            customer_email=email,
        )
        
        return f"💳 Link de pagamento: {session.url}"
    
    except Exception as e:
        return f"Erro ao processar pagamento: {str(e)}"


# ==================== RESUMO ====================

"""
RESUMO DOS EXEMPLOS:

1. ✅ Banco de dados - Salvar conversas
2. ✅ ChatGPT - Respostas inteligentes
3. ✅ Agendamentos - Marcar consultas
4. ✅ Mídia - Enviar imagens/vídeos
5. ✅ Sentimento - Detectar emoções
6. ✅ Busca - Informações da internet
7. ✅ Notificações - Mensagens agendadas
8. ✅ Menu - Interface interativa
9. ✅ Feedback - Coletar avaliações
10. ✅ Pagamentos - Integração Stripe

COMO USAR:
1. Copie a função que quer
2. Instale a dependência necessária
3. Integre em processar_mensagem()
4. Teste localmente em /test
5. Deploy na nuvem

BOA SORTE! 🚀
"""

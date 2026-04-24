# 🤖 GUIA COMPLETO - BOT WHATSAPP COM PYTHON

## 📋 ÍNDICE
1. [Pré-requisitos](#pré-requisitos)
2. [Configuração Twilio](#configuração-twilio)
3. [Instalação Local](#instalação-local)
4. [Teste do Bot](#teste-do-bot)
5. [Deploy na Nuvem](#deploy-na-nuvem)
6. [Personalizar o Bot](#personalizar-o-bot)
7. [Troubleshooting](#troubleshooting)

---

## ✅ PRÉ-REQUISITOS

Antes de começar, você precisa ter:
- **Python 3.8+** instalado
- **Conta no Twilio** (gratuita: https://www.twilio.com/try-twilio)
- **Um número WhatsApp ou usar o sandbox do Twilio**
- **Editor de código** (VS Code, PyCharm, etc)
- **Git** (para deploy na nuvem)

### Verificar Python:
```bash
python --version
# ou
python3 --version
```

---

## 🔧 CONFIGURAÇÃO TWILIO (PASSO A PASSO)

### 1️⃣ Criar Conta Twilio
- Acesse: https://www.twilio.com/console
- Faça signup/login
- Confirme seu email

### 2️⃣ Obter Credenciais
- Vá para: https://www.twilio.com/console
- Na página inicial, você verá:
  ```
  Account SID: ACxxxxxxxxxx (copie)
  Auth Token: xxxxxxxxxxxx (copie)
  ```
- Guarde essas informações!

### 3️⃣ Configurar WhatsApp Sandbox
- Vá para: https://console.twilio.com/sms/whatsapp/learn
- Clique em "Get Started"
- Você receberá um número Twilio tipo: `+1234567890`
- Copie esse número!

### 4️⃣ Conectar seu WhatsApp (Sandbox)
- O Twilio fornecerá um código (ex: `join apple-juice`)
- Envie esse código como mensagem WhatsApp para: `+1 415-523-8886`
- Você receberá confirmação
- Agora seu número está conectado!

**Nota**: O sandbox é gratuito. Para produção, você precisa de um número de negócio.

---

## 💻 INSTALAÇÃO LOCAL

### PASSO 1: Criar Pasta do Projeto
```bash
# No terminal/CMD
mkdir meu_bot_whatsapp
cd meu_bot_whatsapp
```

### PASSO 2: Criar Ambiente Virtual (IMPORTANTE!)
```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Você deve ver `(venv)` no início da linha do terminal.

### PASSO 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

Isto irá instalar:
- Flask (servidor web)
- Twilio (integração WhatsApp)
- python-dotenv (gerenciar credenciais)

### PASSO 4: Configurar Credenciais
1. Abra o arquivo `.env`
2. Substitua pelos seus valores Twilio:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+15551234567
VERIFY_TOKEN=meu_token_secreto_aleatorio
```

---

## 🧪 TESTE DO BOT

### TESTE 1: Testador Web (SEM WHATSAPP)
```bash
# Execute o bot
python whatsapp_bot.py

# No navegador, acesse:
# http://localhost:5000/test
```

Você verá um formulário onde pode digitar mensagens e ver as respostas do bot!

**Mensagens para testar:**
- "oi" → Resposta de boas-vindas
- "horário" → Mostra horário
- "preço" → Mostra preços
- "menu" → Mostra todas as opções
- "qualquer coisa" → Resposta padrão

### TESTE 2: Teste com WhatsApp Real

#### Opção A: Localhost (teste rápido, sem deploy)
1. Execute o bot: `python whatsapp_bot.py`
2. Use um serviço como **ngrok** para expor local:
   ```bash
   # Baixe de: https://ngrok.com/download
   ngrok http 5000
   ```
3. Você receberá uma URL tipo: `https://abc123def456.ngrok.io`
4. Copie essa URL

#### Opção B: Configurar Webhook Twilio (O Caminho Certo)

**Passo 1: Configure o Webhook no Twilio**
- Acesse: https://console.twilio.com/sms/whatsapp/sandbox
- Em "Webhook Settings", coloque:
  ```
  URL: https://seu_dominio.com/webhook
  Método: HTTP POST
  ```
- Salve

**Passo 2: Teste com WhatsApp**
- Envie uma mensagem para o número Twilio
- O bot deve responder automaticamente!

---

## 🚀 DEPLOY NA NUVEM (Heroku, Render, Railway, etc)

### Opção 1: Heroku (Recomendado para iniciantes)

**Passo 1: Criar Procfile**
```
# Arquivo: Procfile
web: gunicorn whatsapp_bot:app
```

**Passo 2: Instalar Gunicorn**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

**Passo 3: Deploy**
```bash
# Instale Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create seu-bot-whatsapp
git push heroku main

# Adicionar variáveis de ambiente
heroku config:set TWILIO_ACCOUNT_SID=xxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxx
heroku config:set TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
heroku config:set VERIFY_TOKEN=seu_token
```

**Passo 4: Configurar Webhook**
- URL: `https://seu-bot-whatsapp.herokuapp.com/webhook`

---

### Opção 2: Render (Mais fácil que Heroku)

1. Acesse: https://render.com
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn whatsapp_bot:app`
5. Adicione variáveis de ambiente (Environment)
6. Deploy!

---

### Opção 3: Railway (Mais simples ainda)

1. Acesse: https://railway.app
2. Clique em "New Project" → "GitHub Repo"
3. Selecione seu repositório
4. Adicione variáveis de ambiente
5. Deploy automático!

---

## 🎨 PERSONALIZAR O BOT

### Adicionar Novos Comandos

Edite a função `processar_mensagem()`:

```python
def processar_mensagem(texto_entrada):
    texto_entrada = texto_entrada.lower().strip()
    
    # ADICIONE AQUI:
    elif 'produto' in texto_entrada:
        return "🛍️ Nossos produtos são: Produto A, B, C"
    
    elif 'boleto' in texto_entrada or 'pagamento' in texto_entrada:
        return "💳 Acesse: seusite.com/pagar"
    
    elif 'duvida' in texto_entrada:
        return "🤔 Qual é sua dúvida? Estou aqui para ajudar!"
```

### Adicionar Imagens e Mídia

```python
from twilio.twiml.messaging_response import MessagingResponse

def webhook():
    response = MessagingResponse()
    
    # Texto
    response.message("Confira nosso catálogo!")
    
    # Imagem
    response.message(media_url="https://example.com/imagem.jpg")
    
    return str(response)
```

### Conectar a um Banco de Dados

```python
import sqlite3

def salvar_contato(numero, nome):
    conn = sqlite3.connect('contatos.db')
    c = conn.cursor()
    c.execute('INSERT INTO contatos VALUES (?, ?)', (numero, nome))
    conn.commit()
    conn.close()
```

### Integrar com IA (ChatGPT)

```python
import openai

openai.api_key = "sua-chave-openai"

def processar_mensagem(texto_entrada):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": texto_entrada}]
    )
    return response['choices'][0]['message']['content']
```

---

## 🐛 TROUBLESHOOTING

### Problema 1: "ModuleNotFoundError: No module named 'flask'"
**Solução:**
```bash
# Verifique se o venv está ativo (deve ter (venv) no terminal)
pip install -r requirements.txt
```

### Problema 2: "Invalid API credentials"
**Solução:**
- Verifique o arquivo `.env`
- Copie exatamente seus valores do Twilio Console
- Reinicie o bot

### Problema 3: "Webhook not receiving messages"
**Solução:**
- Verifique a URL no Twilio Console
- Certifique-se que o bot está rodando
- Use ngrok para testar localhost: `ngrok http 5000`
- Cheque os logs no Twilio Console

### Problema 4: "Port 5000 is already in use"
**Solução:**
```bash
# Mude a porta no código (última linha)
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 📊 ESTRUTURA DO PROJETO FINAL

```
meu_bot_whatsapp/
├── whatsapp_bot.py        # Código principal do bot
├── requirements.txt       # Dependências
├── .env                   # Credenciais (NÃO COMITE!)
├── Procfile              # Para deploy Heroku
├── .gitignore            # Ignorar arquivos sensíveis
└── README.md             # Documentação
```

---

## ✨ PRÓXIMOS PASSOS

1. **Testar localmente** com o testador web
2. **Conectar seu WhatsApp** ao sandbox
3. **Deploy na nuvem** (escolha uma opção)
4. **Personalizar respostas** conforme sua necessidade
5. **Adicionar banco de dados** se precisar histórico
6. **Integrar com APIs** externas

---

## 📞 RECURSOS ÚTEIS

- Twilio Docs: https://www.twilio.com/docs/whatsapp
- Flask Guide: https://flask.palletsprojects.com/
- Deploy Guides: https://devcenter.heroku.com/
- Python WhatsApp: https://github.com/twilio/twilio-python

---

## 🎓 DICAS FINAIS

✅ Sempre use um `.env` para credenciais
✅ Teste localmente antes de fazer deploy
✅ Use try/except para tratar erros
✅ Monitore os logs do seu servidor
✅ Implemente rate limiting se necessário
✅ Faça backup de seus dados

---

**Pronto! Seu bot WhatsApp está funcionando! 🎉**

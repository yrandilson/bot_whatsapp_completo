# 🤖 Bot WhatsApp Completo com Python

Um bot WhatsApp profissional e completo, pronto para produção. Responde mensagens automaticamente usando a API Twilio.

## ✨ Características

✅ Respostas automáticas em tempo real  
✅ Múltiplos comandos customizáveis  
✅ Interface web para testes  
✅ Integração com Twilio  
✅ Fácil de configurar e fazer deploy  
✅ Testes automatizados inclusos  
✅ Documentação completa  

## 🚀 Iniciar em 3 Minutos

### 1. Clonar/Baixar o Projeto
```bash
git clone seu-repositorio
cd seu_bot_whatsapp
```

### 2. Instalar Dependências
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Mac/Linux)
source venv/bin/activate

# Instalar bibliotecas
pip install -r requirements.txt
```

### 3. Configurar Twilio
1. Crie conta em: https://www.twilio.com/try-twilio
2. Obtenha suas credenciais no console
3. Edite o arquivo `.env` com seus valores

### 4. Testar Localmente
```bash
# Terminal 1: Iniciar o bot
python whatsapp_bot.py

# Terminal 2: Acessar teste web
# Abra no navegador: http://localhost:5000/test
```

### 5. Deploy
```bash
# Heroku
heroku create seu-bot
git push heroku main

# Ou use Render/Railway para deploy mais fácil
```

## 📋 Estrutura

```
├── whatsapp_bot.py          # Código principal
├── run_bot.py               # Script de inicialização
├── test_bot.py              # Testes automatizados
├── requirements.txt         # Dependências
├── .env                     # Credenciais (não versione!)
├── GUIA_COMPLETO.md        # Documentação detalhada
└── README.md               # Este arquivo
```

## 🧪 Testar o Bot

### Opção 1: Web (Recomendado)
```bash
python whatsapp_bot.py
# Abra: http://localhost:5000/test
```

### Opção 2: Terminal
```bash
python test_bot.py
```

### Opção 3: WhatsApp Real
Configure o webhook no Twilio apontando para sua URL pública.

## 🎨 Customizar

Edite a função `processar_mensagem()` em `whatsapp_bot.py`:

```python
def processar_mensagem(texto_entrada):
    if 'seu_comando' in texto_entrada.lower():
        return "Sua resposta aqui! 😊"
```

## 📚 Documentação Completa

Veja o arquivo `GUIA_COMPLETO.md` para:
- Configuração passo a passo
- Deploy em diferentes plataformas
- Solução de problemas
- Integração com APIs externas
- Exemplos avançados

## 🔧 Menu Rápido

```bash
# Rodar com interface gráfica
python run_bot.py

# Opções:
# 1. Iniciar Bot
# 2. Testar Bot
# 3. Rodar Testes
# 4. Ver Credenciais
# 5. Editar .env
# 6. Instalar Dependências
# 7. Ver Guia Completo
```

## ⚡ Comandos Disponíveis

| Comando | Resposta |
|---------|----------|
| `oi`, `olá` | Boas-vindas |
| `horário`, `funciona` | Horário de funcionamento |
| `preço`, `custa` | Tabela de preços |
| `endereço`, `localização` | Endereço e contato |
| `menu` | Lista de opções |
| `ajuda` | Menu principal |
| `atendente` | Conectar com pessoa |
| `consultoria` | Agendar consultoria |

## 🔐 Segurança

- ✅ Use `.env` para credenciais
- ✅ Adicione `.env` ao `.gitignore`
- ✅ Nunca commite credenciais
- ✅ Use tokens únicos por ambiente
- ✅ Habilite 2FA no Twilio

## 🐛 Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Port already in use
```python
# Mude a porta no código
app.run(port=5001)
```

### Webhook não recebe mensagens
- Verifique URL no Twilio Console
- Use ngrok para testar localhost
- Confirme o POST é para /webhook

## 📞 Recursos

- [Twilio Docs](https://www.twilio.com/docs/whatsapp)
- [Flask Guide](https://flask.palletsprojects.com/)
- [Python Docs](https://docs.python.org/3/)

## 📄 Licença

MIT License - Sinta-se livre para usar e modificar!

## 💡 Contribuições

Quer melhorar? Faça um fork e mande um pull request! 🎉

---

**Dúvidas?** Leia o `GUIA_COMPLETO.md` para mais detalhes.

**Sucesso com seu bot! 🚀**

#!/usr/bin/env python3
"""
Script de Inicialização Rápida do Bot WhatsApp
Use: python run_bot.py
"""

import os
import sys
import subprocess
from pathlib import Path

def colorir(texto, cor):
    """Colorir texto no terminal"""
    cores = {
        'verde': '\033[92m',
        'vermelho': '\033[91m',
        'amarelo': '\033[93m',
        'azul': '\033[94m',
        'reset': '\033[0m'
    }
    return f"{cores.get(cor, '')}{texto}{cores['reset']}"

def verificar_python():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print(colorir("❌ Python 3.8+ é necessário", 'vermelho'))
        sys.exit(1)
    print(colorir(f"✅ Python {sys.version.split()[0]}", 'verde'))

def verificar_venv():
    """Verifica se o venv está ativo"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(colorir("✅ Ambiente virtual está ativo", 'verde'))
        return True
    else:
        print(colorir("⚠️  Ambiente virtual NÃO está ativo", 'amarelo'))
        print("   Execute primeiro:")
        if os.name == 'nt':
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        return False

def verificar_arquivo_env():
    """Verifica se arquivo .env existe"""
    if os.path.exists('.env'):
        print(colorir("✅ Arquivo .env encontrado", 'verde'))
        
        # Verificar se contém valores reais
        with open('.env') as f:
            content = f.read()
            if 'seu_' in content or 'xxxx' in content:
                print(colorir("⚠️  .env contém placeholders! Configure com seus valores Twilio", 'amarelo'))
                return False
        return True
    else:
        print(colorir("❌ Arquivo .env não encontrado!", 'vermelho'))
        print("   Crie um arquivo .env com suas credenciais Twilio")
        return False

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    dependencias = ['flask', 'twilio', 'dotenv']
    todas_ok = True
    
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            print(colorir(f"✅ {dep}", 'verde'))
        except ImportError:
            print(colorir(f"❌ {dep} não instalado", 'vermelho'))
            todas_ok = False
    
    if not todas_ok:
        print("\nInstale as dependências com:")
        print(colorir("pip install -r requirements.txt", 'azul'))
        return False
    return True

def menu_principal():
    """Menu principal do script"""
    print("\n" + colorir("=" * 50, 'azul'))
    print(colorir("   🤖 BOT WHATSAPP COM PYTHON", 'azul'))
    print(colorir("=" * 50, 'azul'))
    
    print("\nEscolha uma opção:\n")
    print("1️⃣  Iniciar Bot (servidor principal)")
    print("2️⃣  Testar Bot (sem WhatsApp)")
    print("3️⃣  Rodar Testes Automatizados")
    print("4️⃣  Ver Credenciais Configuradas")
    print("5️⃣  Editar Arquivo .env")
    print("6️⃣  Instalar Dependências")
    print("7️⃣  Ver Guia Completo")
    print("8️⃣  Sair\n")
    
    opcao = input("Digite o número da opção: ").strip()
    return opcao

def iniciar_bot():
    """Inicia o bot"""
    print("\n" + colorir("🚀 Iniciando Bot WhatsApp...", 'verde'))
    print("📍 Acesse em: http://localhost:5000")
    print("🧪 Teste em: http://localhost:5000/test")
    print("🔗 Webhook: http://localhost:5000/webhook")
    print("\nPressione Ctrl+C para parar\n")
    
    try:
        import whatsapp_bot
        print(colorir("✅ Bot iniciado com sucesso!", 'verde'))
    except Exception as e:
        print(colorir(f"❌ Erro ao iniciar: {e}", 'vermelho'))

def testar_bot():
    """Testa o bot sem WhatsApp"""
    print("\n" + colorir("🧪 Modo Teste", 'azul'))
    print("Digite mensagens para testar o bot (Ctrl+C para sair)\n")
    
    from whatsapp_bot import processar_mensagem
    
    while True:
        try:
            mensagem = input("Sua mensagem: ").strip()
            if not mensagem:
                continue
            
            resposta = processar_mensagem(mensagem)
            print(colorir(f"Bot: {resposta}\n", 'verde'))
        except KeyboardInterrupt:
            print("\n" + colorir("Saindo...", 'amarelo'))
            break

def rodar_testes():
    """Executa testes automatizados"""
    print("\n" + colorir("🧪 Executando Testes Automatizados...", 'azul'))
    try:
        import test_bot
    except Exception as e:
        print(colorir(f"❌ Erro ao rodar testes: {e}", 'vermelho'))

def ver_credenciais():
    """Mostra credenciais configuradas"""
    print("\n" + colorir("🔐 Credenciais Configuradas", 'azul'))
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        sid = os.getenv('TWILIO_ACCOUNT_SID', 'NÃO CONFIGURADO')
        token = os.getenv('TWILIO_AUTH_TOKEN', 'NÃO CONFIGURADO')
        numero = os.getenv('TWILIO_WHATSAPP_NUMBER', 'NÃO CONFIGURADO')
        
        # Mostrar apenas primeiros e últimos caracteres por segurança
        def mascarar(valor):
            if len(valor) > 10:
                return f"{valor[:4]}...{valor[-4:]}"
            return "***"
        
        print(f"Account SID: {mascarar(sid)}")
        print(f"Auth Token: {mascarar(token)}")
        print(f"WhatsApp Number: {numero}")
        
        if 'NÃO CONFIGURADO' in [sid, token, numero]:
            print(colorir("\n⚠️  Algumas credenciais não estão configuradas!", 'amarelo'))
    except Exception as e:
        print(colorir(f"❌ Erro: {e}", 'vermelho'))

def editar_env():
    """Abre arquivo .env no editor padrão"""
    print("\n" + colorir("Abrindo arquivo .env...", 'azul'))
    
    if os.name == 'nt':
        os.startfile('.env')
    elif os.name == 'posix':
        os.system(f"$EDITOR .env")
    else:
        print("Use seu editor favorito para abrir o arquivo .env")

def instalar_dependencias():
    """Instala dependências"""
    print("\n" + colorir("📦 Instalando Dependências...", 'azul'))
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print(colorir("✅ Dependências instaladas!", 'verde'))
    except Exception as e:
        print(colorir(f"❌ Erro: {e}", 'vermelho'))

def ver_guia():
    """Mostra o guia completo"""
    try:
        with open('GUIA_COMPLETO.md') as f:
            print("\n" + f.read())
    except FileNotFoundError:
        print(colorir("❌ Arquivo GUIA_COMPLETO.md não encontrado", 'vermelho'))

def main():
    """Função principal"""
    print(colorir("\n🔍 Verificando Configuração...", 'azul'))
    print("-" * 50)
    
    # Verificações
    verificar_python()
    venv_ativo = verificar_venv()
    env_existe = verificar_arquivo_env()
    deps_ok = verificar_dependencias()
    
    print("-" * 50)
    
    if venv_ativo and env_existe and deps_ok:
        print(colorir("\n✅ Tudo está configurado!", 'verde'))
    else:
        print(colorir("\n⚠️  Resolva os problemas acima", 'amarelo'))
    
    # Menu
    while True:
        opcao = menu_principal()
        
        if opcao == '1':
            iniciar_bot()
            break
        elif opcao == '2':
            testar_bot()
        elif opcao == '3':
            rodar_testes()
        elif opcao == '4':
            ver_credenciais()
        elif opcao == '5':
            editar_env()
        elif opcao == '6':
            instalar_dependencias()
        elif opcao == '7':
            ver_guia()
        elif opcao == '8':
            print(colorir("\nAté logo! 👋", 'verde'))
            break
        else:
            print(colorir("❌ Opção inválida", 'vermelho'))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(colorir("\n\nInterrompido pelo usuário", 'amarelo'))
    except Exception as e:
        print(colorir(f"❌ Erro: {e}", 'vermelho'))

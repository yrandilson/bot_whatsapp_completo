"""
Testes Automatizados para o Bot WhatsApp
Execute com: python test_bot.py
"""

import unittest
from whatsapp_bot import processar_mensagem, app

class TestBotWhatsApp(unittest.TestCase):
    """Testes para as funções do bot"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.app = app.test_client()
        self.app.testing = True
    
    # ========== TESTES DE RESPOSTA ==========
    
    def test_saudacao_oi(self):
        """Testa resposta para 'oi'"""
        resposta = processar_mensagem("oi")
        self.assertIn("Olá", resposta)
        self.assertIn("bem-vindo", resposta.lower())
    
    def test_saudacao_ola(self):
        """Testa resposta para 'olá'"""
        resposta = processar_mensagem("olá")
        self.assertIn("Olá", resposta)
    
    def test_horario(self):
        """Testa resposta para 'horário'"""
        resposta = processar_mensagem("horário")
        self.assertIn("09:00", resposta)
    
    def test_preco(self):
        """Testa resposta para 'preço'"""
        resposta = processar_mensagem("preço")
        self.assertIn("R$", resposta)
    
    def test_menu(self):
        """Testa resposta para 'menu'"""
        resposta = processar_mensagem("menu")
        self.assertIn("Menu", resposta)
    
    def test_endereco(self):
        """Testa resposta para 'endereço'"""
        resposta = processar_mensagem("endereço")
        self.assertIn("📍", resposta)
    
    def test_atendente(self):
        """Testa resposta para 'atendente'"""
        resposta = processar_mensagem("atendente")
        self.assertIn("atendente", resposta.lower())
    
    def test_mensagem_desconhecida(self):
        """Testa resposta para mensagem desconhecida"""
        resposta = processar_mensagem("xyz123abc")
        self.assertIn("menu", resposta.lower())
    
    def test_case_insensitive(self):
        """Testa se as respostas funcionam em maiúsculas/minúsculas"""
        resposta1 = processar_mensagem("OI")
        resposta2 = processar_mensagem("oi")
        self.assertEqual(resposta1, resposta2)
    
    # ========== TESTES DE ROTA ==========
    
    def test_home_page(self):
        """Testa se a página inicial carrega"""
        resposta = self.app.get('/')
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Online", resposta.data)
    
    def test_test_page(self):
        """Testa se a página de teste carrega"""
        resposta = self.app.get('/test')
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Testador", resposta.data)
    
    def test_test_post(self):
        """Testa envio de mensagem na página de teste"""
        resposta = self.app.post('/test', data={'mensagem': 'oi'})
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Resultado", resposta.data)
    
    # ========== TESTES DE PERFORMANCE ==========
    
    def test_resposta_nao_vazia(self):
        """Garante que as respostas nunca são vazias"""
        testes = [
            "oi", "olá", "opa", "horário", "preço", 
            "menu", "ajuda", "endereço", "xyz", "123"
        ]
        for msg in testes:
            resposta = processar_mensagem(msg)
            self.assertGreater(len(resposta), 0, f"Resposta vazia para '{msg}'")
    
    def test_resposta_com_emoji(self):
        """Verifica se as respostas contêm emojis (melhor UX)"""
        resposta = processar_mensagem("oi")
        self.assertTrue(any(ord(c) > 127 for c in resposta), 
                       "Resposta sem emojis")

# ========== TESTES CUSTOMIZADOS ==========

class TestCustom(unittest.TestCase):
    """Adicione seus próprios testes aqui"""
    
    def test_sua_funcionalidade(self):
        """Exemplo: teste sua funcionalidade específica"""
        resposta = processar_mensagem("consultoria")
        self.assertIn("consultoria", resposta.lower())

# ========== EXECUTAR TESTES ==========

if __name__ == '__main__':
    print("🧪 Executando testes do Bot WhatsApp...\n")
    
    # Configuração dos testes
    unittest.main(
        verbosity=2,  # Saída detalhada
        exit=False    # Não sai do programa
    )
    
    print("\n✅ Testes concluídos!")

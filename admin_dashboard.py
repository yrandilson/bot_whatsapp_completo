"""
📊 DASHBOARD DE ADMINISTRAÇÃO DO BOT WHATSAPP

Painel web para monitorar e gerenciar o bot em tempo real
Adicione ao seu whatsapp_bot.py ou execute como aplicação separada
"""

from flask import Flask, render_template_string, jsonify, request
from datetime import datetime, timedelta
import json
import os

app_dashboard = Flask(__name__)

# ==================== DADOS SIMULADOS (Use seus dados reais) ====================

DADOS_USUARIOS = {
    "5585999887766": {
        "nome": "João Silva",
        "mensagens_total": 45,
        "mensagens_hoje": 5,
        "sentimento": "positivo",
        "categoria_principal": "informacao",
        "ativo": True,
        "primeira_msg": "2024-03-20T10:30:00",
        "ultima_msg": "2024-03-29T15:45:00"
    },
    "5585988776655": {
        "nome": "Maria Santos",
        "mensagens_total": 120,
        "mensagens_hoje": 8,
        "sentimento": "negativo",
        "categoria_principal": "problema",
        "ativo": True,
        "primeira_msg": "2024-03-15T14:20:00",
        "ultima_msg": "2024-03-29T14:10:00"
    },
    "5585977665544": {
        "nome": "Pedro Costa",
        "mensagens_total": 23,
        "mensagens_hoje": 0,
        "sentimento": "neutro",
        "categoria_principal": "saudacao",
        "ativo": False,
        "primeira_msg": "2024-03-25T09:00:00",
        "ultima_msg": "2024-03-28T16:30:00"
    }
}

ESTATISTICAS_GERAIS = {
    "total_usuarios": len(DADOS_USUARIOS),
    "usuarios_ativos": sum(1 for u in DADOS_USUARIOS.values() if u["ativo"]),
    "mensagens_hoje": sum(u["mensagens_hoje"] for u in DADOS_USUARIOS.values()),
    "mensagens_total": sum(u["mensagens_total"] for u in DADOS_USUARIOS.values()),
    "sentimento_geral": "positivo"
}

# ==================== ROTAS DO DASHBOARD ====================

@app_dashboard.route('/dashboard')
def dashboard():
    """Página principal do dashboard"""
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 Dashboard Bot WhatsApp</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .header {
                background: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            
            .header h1 {
                color: #333;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .header p {
                color: #666;
                font-size: 14px;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                text-align: center;
            }
            
            .stat-card h3 {
                color: #666;
                font-size: 14px;
                margin-bottom: 10px;
                text-transform: uppercase;
            }
            
            .stat-card .number {
                font-size: 32px;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 5px;
            }
            
            .stat-card .label {
                color: #999;
                font-size: 12px;
            }
            
            .content-grid {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 20px;
            }
            
            .card {
                background: white;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .card-header {
                background: #f8f9fa;
                padding: 20px;
                border-bottom: 1px solid #eee;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .card-header h2 {
                color: #333;
                font-size: 18px;
            }
            
            .card-body {
                padding: 20px;
            }
            
            .user-item {
                padding: 15px;
                border-bottom: 1px solid #eee;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .user-item:last-child {
                border-bottom: none;
            }
            
            .user-info {
                flex: 1;
            }
            
            .user-name {
                font-weight: bold;
                color: #333;
            }
            
            .user-stats {
                font-size: 12px;
                color: #999;
                margin-top: 5px;
            }
            
            .badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
            }
            
            .badge-positivo {
                background: #d4edda;
                color: #155724;
            }
            
            .badge-negativo {
                background: #f8d7da;
                color: #721c24;
            }
            
            .badge-neutro {
                background: #e2e3e5;
                color: #383d41;
            }
            
            .badge-ativo {
                background: #cfe2ff;
                color: #084298;
            }
            
            .badge-inativo {
                background: #e7d4f5;
                color: #6c757d;
            }
            
            .chart {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
                margin: 15px 0;
            }
            
            .chart-bar {
                display: flex;
                margin-bottom: 15px;
                align-items: center;
            }
            
            .chart-label {
                width: 100px;
                font-size: 12px;
                color: #666;
            }
            
            .chart-value {
                flex: 1;
                background: #667eea;
                height: 30px;
                border-radius: 5px;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                padding-right: 10px;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }
            
            .action-buttons {
                display: flex;
                gap: 10px;
            }
            
            button {
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 12px;
                font-weight: bold;
                transition: all 0.3s;
            }
            
            .btn-primary {
                background: #667eea;
                color: white;
            }
            
            .btn-primary:hover {
                background: #5568d3;
            }
            
            .btn-danger {
                background: #dc3545;
                color: white;
            }
            
            .btn-danger:hover {
                background: #c82333;
            }
            
            @media (max-width: 768px) {
                .content-grid {
                    grid-template-columns: 1fr;
                }
                
                .stats-grid {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Dashboard Bot WhatsApp</h1>
                <p>Monitoramento e administração do bot em tempo real</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total de Usuários</h3>
                    <div class="number" id="total-usuarios">3</div>
                    <div class="label">usuarios cadastrados</div>
                </div>
                
                <div class="stat-card">
                    <h3>Usuários Ativos</h3>
                    <div class="number" id="usuarios-ativos">2</div>
                    <div class="label">online nas últimas 24h</div>
                </div>
                
                <div class="stat-card">
                    <h3>Mensagens Hoje</h3>
                    <div class="number" id="msgs-hoje">13</div>
                    <div class="label">mensagens recebidas</div>
                </div>
                
                <div class="stat-card">
                    <h3>Total de Mensagens</h3>
                    <div class="number" id="msgs-total">188</div>
                    <div class="label">desde o início</div>
                </div>
            </div>
            
            <div class="content-grid">
                <div class="card">
                    <div class="card-header">
                        <h2>👥 Usuários Ativos</h2>
                        <button class="btn-primary" onclick="recarregarDados()">🔄 Atualizar</button>
                    </div>
                    <div class="card-body" id="usuarios-list">
                        <!-- Preenchido por JavaScript -->
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h2>📊 Distribuição</h2>
                    </div>
                    <div class="card-body">
                        <div class="chart">
                            <strong style="font-size: 12px; color: #666;">Sentimentos</strong>
                            <div class="chart-bar">
                                <div class="chart-label">Positivo</div>
                                <div class="chart-value" style="width: 45%;">45%</div>
                            </div>
                            <div class="chart-bar">
                                <div class="chart-label">Neutro</div>
                                <div class="chart-value" style="width: 35%; background: #999;">35%</div>
                            </div>
                            <div class="chart-bar">
                                <div class="chart-label">Negativo</div>
                                <div class="chart-value" style="width: 20%; background: #dc3545;">20%</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function carregarDados() {
                // Simular carregamento de dados
                const usuarios = {
                    "5585999887766": {
                        "nome": "João Silva",
                        "mensagens_total": 45,
                        "sentimento": "positivo",
                        "ativo": true
                    },
                    "5585988776655": {
                        "nome": "Maria Santos",
                        "mensagens_total": 120,
                        "sentimento": "negativo",
                        "ativo": true
                    },
                    "5585977665544": {
                        "nome": "Pedro Costa",
                        "mensagens_total": 23,
                        "sentimento": "neutro",
                        "ativo": false
                    }
                };
                
                let html = '';
                for (const [numero, dados] of Object.entries(usuarios)) {
                    const statusBadge = dados.ativo ? 
                        '<span class="badge badge-ativo">Ativo</span>' : 
                        '<span class="badge badge-inativo">Inativo</span>';
                    
                    const sentimentoBadge = `<span class="badge badge-${dados.sentimento}">${dados.sentimento}</span>`;
                    
                    html += `
                        <div class="user-item">
                            <div class="user-info">
                                <div class="user-name">${dados.nome}</div>
                                <div class="user-stats">${numero} • ${dados.mensagens_total} mensagens</div>
                            </div>
                            <div class="action-buttons">
                                ${sentimentoBadge}
                                ${statusBadge}
                                <button class="btn-primary" onclick="verDetalhes('${numero}')">Ver</button>
                            </div>
                        </div>
                    `;
                }
                
                document.getElementById('usuarios-list').innerHTML = html;
            }
            
            function recarregarDados() {
                carregarDados();
                alert('✅ Dados atualizados!');
            }
            
            function verDetalhes(numero) {
                alert('Detalhes do usuário: ' + numero);
            }
            
            // Carregar dados ao abrir
            carregarDados();
            
            // Atualizar a cada 30 segundos
            setInterval(carregarDados, 30000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app_dashboard.route('/api/usuarios')
def api_usuarios():
    """API para obter lista de usuários"""
    return jsonify(DADOS_USUARIOS)

@app_dashboard.route('/api/estatisticas')
def api_estatisticas():
    """API para obter estatísticas gerais"""
    return jsonify(ESTATISTICAS_GERAIS)

@app_dashboard.route('/api/usuario/<numero>')
def api_usuario(numero):
    """API para obter dados de um usuário específico"""
    if numero in DADOS_USUARIOS:
        return jsonify(DADOS_USUARIOS[numero])
    return jsonify({'erro': 'Usuário não encontrado'}), 404

@app_dashboard.route('/api/relatorio')
def api_relatorio():
    """API para gerar relatório"""
    relatorio = {
        'gerado_em': datetime.now().isoformat(),
        'periodo': '24h',
        'estatisticas': ESTATISTICAS_GERAIS,
        'usuarios': DADOS_USUARIOS
    }
    return jsonify(relatorio)

# ==================== PARA USAR NO WHATSAPP_BOT.PY ====================

"""
Para integrar o dashboard ao seu bot, adicione ao whatsapp_bot.py:

from admin_dashboard import app_dashboard

# Registrar blueprint
app.register_blueprint(app_dashboard, url_prefix='/admin')

# Depois acesse em:
# http://localhost:5000/admin/dashboard
"""

# ==================== EXECUTAR COMO APLICAÇÃO SEPARADA ====================

if __name__ == '__main__':
    print("📊 Dashboard iniciado!")
    print("🔗 Acesse em: http://localhost:5001/dashboard")
    print("📱 API disponível em: http://localhost:5001/api/")
    print("\nEndpoints disponíveis:")
    print("  GET /api/usuarios - Lista de usuários")
    print("  GET /api/estatisticas - Estatísticas gerais")
    print("  GET /api/usuario/<numero> - Dados de um usuário")
    print("  GET /api/relatorio - Relatório completo")
    print("\nPressione Ctrl+C para parar\n")
    
    app_dashboard.run(debug=True, port=5001)

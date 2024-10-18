import os
from flask import Flask, request, jsonify, render_template_string
import secrets
import time
import uuid

app = Flask(__name__)
application = app  # Para compatibilidade com ambientes como o Render ou AWS

# Armazenamento para chave, timestamp e sessões ativas
key_data = {
    "key": None,
    "timestamp": None
}
active_sessions = {}  # Para armazenar sessões ativas

# Usuários permitidos
allowed_users = {
    "pstfr", "emda", "wndrsn", "thglm", "emrsnc", "cslxnd", 
    "wlsn", "edrd", "vttb", "tmmz", "wltr", "crtntt", 
    "wndrsn", "rcrd", "ndrtx", "vttbt", "mrn", "rflcr", 
    "cnt", "wbss", "zr1", "nbsbt"
}

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)  # Gera uma chave hexadecimal de 16 bytes

# Função para verificar se a chave ainda é válida
def is_key_valid():
    if key_data["key"] and key_data["timestamp"]:
        current_time = time.time()
        # Verifica se a chave ainda é válida (5 minutos = 300 segundos)
        if current_time - key_data["timestamp"] <= 300:
            return True
    return False

# Rota da página de login
@app.route('/')
def login():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f9;
            }
            .login-container {
                text-align: center;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                background-color: white;
                width: 300px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .login-container h1 {
                margin-bottom: 20px;
            }
            .login-container form {
                display: flex;
                flex-direction: column;
                width: 100%;
            }
            .login-container input {
                padding: 10px;
                margin-bottom: 10px;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .login-container button {
                padding: 10px 20px;
                background-color: #0088cc;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }
            .login-container button:hover {
                background-color: #005f99;
            }
            .contact {
                margin-top: 20px;
            }
            .author-link {
                color: #0088cc;
                text-decoration: none;
                font-weight: bold;
            }
            .telegram-group {
                margin-top: 10px;
            }
            .telegram-group a {
                color: #ffcc00;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>Login</h1>
            <form action="/generate" method="post">
                <input type="text" id="username" name="username" placeholder="Usuário" required><br>
                <button type="submit">Login</button>
            </form>
            <div class="contact">
                <p>Para acessar entre em contato:</p>
                <a class="author-link" href="https://t.me/Keno_venas" target="_blank">Keno Venas</a>
            </div>
            <div class="telegram-group">
                <p>Grupo do Telegram:</p>
                <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Crypto Faucets</a>
            </div>
        </div>
    </body>
    </html>
    '''

# Rota para geração de chave de acesso
@app.route('/generate', methods=['POST'])
def generate():
    username = request.form.get('username')
    
    if username in allowed_users:
        if username in active_sessions:  # Verifica se já existe uma sessão ativa
            return jsonify({"error": "Usuário já está logado em outro dispositivo."}), 403
        
        # Gera a nova sessão
        session_id = str(uuid.uuid4())
        active_sessions[username] = session_id

        if not is_key_valid():
            key_data["key"] = generate_key()
            key_data["timestamp"] = time.time()

        return render_template_string(f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Access Key</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    position: relative;
                    flex-direction: column;
                }}
                .content {{
                    text-align: center;
                    margin-top: 20px;
                }}
                .author {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    color: #000;
                    font-size: 18px;
                }}
                .banner-telegram {{
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background-color: #0088cc;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }}
                .banner-telegram a {{
                    color: #ffcc00;
                    text-decoration: none;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="author">Autor: Keno Venas</div>
            <div class="banner-telegram">
                <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Grupo do Telegram</a>
            </div>
            <div class="content">
                <h1>Access Key</h1>
                <p>{key_data["key"]}</p>
                <p>Session ID: {session_id}</p>
            </div>
        </body>
        </html>
        ''')
    else:
        return jsonify({"error": "Acesso negado"}), 403

# Rota para logout
@app.route('/logout', methods=['POST'])
def logout():
    username = request.form.get('username')
    if username in active_sessions:
        del active_sessions[username]
        return jsonify({"message": "Logout realizado com sucesso!"}), 200
    return jsonify({"error": "Usuário não está logado."}), 404

# Rota para validação da chave
@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.get_json()
    if 'key' in data:
        if data['key'] == key_data['key'] and is_key_valid():
            return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

# Inicializa o servidor, ajustando a porta para o ambiente de produção
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

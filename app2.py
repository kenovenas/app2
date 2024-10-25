from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Lista de usuários autorizados
usuarios_autorizados = [
    "fiel", "ok6675", "crtntt", "ok3286", "ok1390", "zr1", "nbsbt", "mxchk",
    "pdrrm", "mro", "hmd", "mrclm", "mxwll", "nmmr", "mts", "jncmps", "dnln",
    "ok1698", "ok0091", "ok0908", "ok2508", "ok2956", "ok1203"
]

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    usuario = data.get('usuario')

    # Verifica se o usuário é autorizado
    if usuario in usuarios_autorizados:
        # Imprime no console o usuário autorizado e o horário da requisição
        print(f"[{datetime.now()}] Usuário autorizado: {usuario}")
        return jsonify({'autorizado': True}), 200
    else:
        # Imprime no console a tentativa de acesso não autorizada
        print(f"[{datetime.now()}] Tentativa de acesso negada para o usuário: {usuario}")
        return jsonify({'autorizado': False}), 403  # Forbidden

if __name__ == '__main__':
    # Certifique-se de que a porta está configurada para ser dinâmica no Render
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

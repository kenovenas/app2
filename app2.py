from flask import Flask, request, jsonify

app = Flask(__name__)

# Dicionário para armazenar informações dos usuários
users = {}
# Dicionário para contar as visitas dos usuários
visit_count = {}

@app.route('/add_user', methods=['POST'])
def add_user():
    """Adiciona um novo usuário com uma quantidade de acesso definida."""
    data = request.json
    username = data['username']
    access_limit = data['access_limit']
    
    # Verifica se o usuário já existe
    if username in users:
        return jsonify({"message": "Usuário já existe."}), 400
    
    # Adiciona o usuário
    users[username] = access_limit
    visit_count[username] = 0  # Inicia o contador de visitas em 0
    return jsonify({"message": "Usuário adicionado com sucesso!"}), 201

@app.route('/visit/<username>', methods=['GET'])
def visit(username):
    """Registra uma visita de um usuário."""
    if username not in users:
        return jsonify({"message": "Usuário não encontrado."}), 404

    # Verifica se o limite de visitas foi atingido
    if visit_count[username] >= users[username]:
        return jsonify({"message": "Acesso negado. Limite de visitas atingido."}), 403

    # Incrementa o contador de visitas
    visit_count[username] += 1
    return jsonify({"message": f"Visita registrada. Total de visitas: {visit_count[username]}."}), 200

@app.route('/set_access_limit/<username>', methods=['PATCH'])
def set_access_limit(username):
    """Define a nova quantidade de acesso para um usuário."""
    if username not in users:
        return jsonify({"message": "Usuário não encontrado."}), 404
    
    data = request.json
    new_limit = data['access_limit']
    
    # Atualiza o limite de acesso do usuário
    users[username] = new_limit
    return jsonify({"message": "Limite de acesso atualizado."}), 200

@app.route('/status/<username>', methods=['GET'])
def status(username):
    """Retorna o status de acesso do usuário."""
    if username not in users:
        return jsonify({"message": "Usuário não encontrado."}), 404
    
    return jsonify({
        "username": username,
        "access_limit": users[username],
        "current_visits": visit_count[username],
        "remaining_access": users[username] - visit_count[username]
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

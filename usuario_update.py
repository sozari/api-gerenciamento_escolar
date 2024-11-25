from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from utils import connect_to_database

usuario_update_bp = Blueprint('usuario_update_bp', __name__)

# Rota para editar o usuário
@usuario_update_bp.route('/usuario_update/<int:idusuario>', methods=['GET', 'PUT'])
def usuario_update(idusuario):
    if request.method == 'GET':
        # Buscar o usuário no banco para editar
        try:
            connection = connect_to_database()
            cursor = connection.cursor(dictionary=True)

            # Seleciona os dados do usuário pelo id
            cursor.execute("SELECT idusuario, nome, email FROM usuarios WHERE idusuario = %s", (idusuario,))
            usuario = cursor.fetchone()

            if usuario is None:
                return jsonify({'mensagem': 'Usuário não encontrado.'}), 404
            
            return jsonify(usuario), 200  # Retorna os dados do usuário para edição
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    if request.method == 'PUT':
        dados = request.json
        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')

        if not nome or not email or not senha:
            return jsonify({'mensagem': 'Todos os campos são obrigatórios.'}), 400

        senha_criptografada = generate_password_hash(senha)

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            # Atualiza os dados do usuário no banco
            cursor.execute("""
                UPDATE usuarios
                SET nome = %s, email = %s, senha = %s
                WHERE idusuario = %s
            """, (nome, email, senha_criptografada, idusuario))

            if cursor.rowcount == 0:
                return jsonify({'mensagem': 'Nenhum usuário encontrado com esse ID.'}), 404

            connection.commit()
            return jsonify({'mensagem': 'Dados do usuário atualizados com sucesso!'}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from utils import connect_to_database

usuario_update_bp = Blueprint('usuario_update_bp', __name__)

@usuario_update_bp.route('/usuario_update/<int:idusuario>', methods=['PUT'])
def usuario_update(idusuario):

    dados = request.json
    senha_criptografada = generate_password_hash(dados['senha'])

    try:
        with connect_to_database() as db:
            cursor = db.cursor()

            sql = """
                UPDATE usuarios
                SET nome = %s, email = %s, senha = %s
                WHERE idusuario = %s
            """
            valores = (dados['nome'], dados['email'], senha_criptografada, idusuario)
            cursor.execute(sql, valores)

            if cursor.rowcount == 0:
                return jsonify({'mensagem': 'Nenhum usuario encontrado com este ID e tipo de usuário.'}), 404

            db.commit()
            return jsonify({'mensagem': 'Dados do usuario atualizados com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

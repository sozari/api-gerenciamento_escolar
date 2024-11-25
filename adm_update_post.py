from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from utils import connect_to_database

adm_update2_bp = Blueprint('adm_update_bp', __name__)

@adm_update2_bp.route('/adm_update_post/<int:idusuario>/<string:tipo_usuario>', methods=['POST'])
def atualizar_administrador(idusuario, tipo_usuario):
    # Verifica se o tipo_usuario é "administrador"
    if tipo_usuario != 'administrador':
        return jsonify({'mensagem': 'Atualização permitida apenas para administradores.'}), 403

    # Recebe os dados da requisição (dados do formulário)
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    if not nome or not email or not senha:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios.'}), 400

    senha_criptografada = generate_password_hash(senha)  # Criptografa a nova senha

    # Comando SQL para atualizar os dados do administrador
    sql = """
        UPDATE usuarios 
        SET nome = %s, email = %s, senha = %s 
        WHERE idusuario = %s AND tipo_usuario = %s
    """
    valores = (nome, email, senha_criptografada, idusuario, tipo_usuario)

    try:
        # Conectar ao banco de dados utilizando a função do utils.py
        connection = connect_to_database()
        if connection is None:
            return jsonify({'mensagem': 'Erro ao conectar ao banco de dados.'}), 500

        with connection as mydb:
            mycursor = mydb.cursor()
            mycursor.execute(sql, valores)
            
            if mycursor.rowcount == 0:  # Nenhum registro foi atualizado
                return jsonify({'mensagem': 'Nenhum administrador encontrado com este ID e tipo de usuário.'}), 404

            # Commit e retorno de sucesso
            mydb.commit()
            return jsonify({'mensagem': 'Dados do administrador atualizados com sucesso!'}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500


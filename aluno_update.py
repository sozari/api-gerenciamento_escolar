from flask import Blueprint, Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash

from utils import connect_to_database

aluno_update_bp = Blueprint('aluno_update',__name__)


@app.route('/aluno_update/<string:nome>/<string:tipo_usuario>', methods=['PUT'])
def atualizar_aluno(nome, tipo_usuario):  # Ajustado para coincidir com os parâmetros da URL
    dados = request.json
    senha_criptografada = generate_password_hash(dados['senha'])  # Criptografa a nova senha
    connection = connect_to_database()

    sql = """
        UPDATE usuarios 
        SET nome = %s, email = %s, senha = %s 
        WHERE nome = %s AND tipo_usuario = %s
    """
    valores = (dados['nome'], dados['email'], senha_criptografada, nome, tipo_usuario)

    try:
        with connection as mydb:
            mycursor = mydb.cursor()
            mycursor.execute(sql, valores)
            mydb.commit()
            return jsonify({'mensagem': 'Dados do aluno atualizados com sucesso!'}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500



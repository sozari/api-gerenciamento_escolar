from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

@app.route('/aluno_update/<string:nome>/<string:tipo_usuario>', methods=['PUT'])
def atualizar_aluno(nome, tipo_usuario):  # Ajustado para coincidir com os parâmetros da URL
    dados = request.json
    senha_criptografada = generate_password_hash(dados['senha'])  # Criptografa a nova senha

    sql = """
        UPDATE usuarios 
        SET nome = %s, email = %s, senha = %s 
        WHERE nome = %s AND tipo_usuario = %s
    """
    valores = (dados['nome'], dados['email'], senha_criptografada, nome, tipo_usuario)

    try:
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()
            mycursor.execute(sql, valores)
            mydb.commit()
            return jsonify({'mensagem': 'Dados do aluno atualizados com sucesso!'}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)

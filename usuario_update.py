from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

@app.route('/usuario_update/<int:idusuario>', methods=['PUT'])
def atualizar_usuario(idusuario):
    dados = request.json
    senha_criptografada = generate_password_hash(dados['senha'], method='pbkdf2:sha256')  # Criptografando a senha
    sql = "UPDATE usuarios SET nome=%s, email=%s, senha=%s  WHERE idusuario=%s"
    valores = (dados['nome'], dados['email'], senha_criptografada, idusuario)

    try:
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()  # Corrigido aqui
            mycursor.execute(sql, valores)
            mydb.commit()
            return jsonify({'mensagem': 'Usuário atualizado com sucesso'}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500

@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':  # Corrigido aqui
    app.run(debug=True)

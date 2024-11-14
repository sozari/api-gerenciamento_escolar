from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

# Rota para processar o formulário de cadastro de professor
@app.route('/professor_cadastro', methods=['POST'])
def cadastro_professor():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone = request.form['telefone']

    if not nome or not email or not senha or not telefone:
        return "Todos os campos são obrigatórios!"

    senha_hash = generate_password_hash(senha)

    try:
        # Conectar ao banco de dados
        connection = get_db_connection()
        cursor = connection.cursor()

        # Primeiro, inserir o usuário para gerar um idusuario
        sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_usuario, (nome, email, senha_hash, 'professor'))
        idusuario = cursor.lastrowid  # Pega o ID do usuário recém-criado

        # Inserir o professor com o idusuario gerado
        sql_professor = "INSERT INTO professor (idusuario, telefone) VALUES (%s, %s)"
        cursor.execute(sql_professor, (idusuario, telefone))
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return f"Erro ao processar os dados: {err}"

    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

    return redirect(url_for('sucesso'))

# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)


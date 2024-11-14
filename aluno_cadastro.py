from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

# Rota para processar o formulário
@app.route('/aluno_cadastro', methods=['POST'])
def submit_formulario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone_responsavel = request.form['telefone_responsavel']

    if not nome or not email or not senha or not telefone_responsavel:
        return "Todos os campos são obrigatórios!"

    senha_hash = generate_password_hash(senha)

    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Primeiro, inserir o usuário para gerar um idusuario
        sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_usuario, (nome, email, senha_hash, 'aluno'))
        idusuario = cursor.lastrowid  # Pega o ID do usuário recém-criado

        # Inserir o aluno com o idusuario gerado
        sql_aluno = "INSERT INTO aluno (idusuario, telefone_responsavel) VALUES (%s, %s)"
        cursor.execute(sql_aluno, (idusuario, telefone_responsavel))
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return "Erro ao processar os dados. Tente novamente mais tarde."

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

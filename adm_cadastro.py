from flask import Blueprint, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash

adm_cadastro_bp = Blueprint('adm_cadastro_bp', __name__)

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

# Rota para processar o formulário de cadastro de administrador
@adm_cadastro_bp.route('/adm_cadastro', methods=['POST'])
def cadastro_professor():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    # Verificar se todos os campos foram preenchidos
    if not nome or not email or not senha:
        return "Todos os campos são obrigatórios!"

    # Gerar hash da senha
    senha_hash = generate_password_hash(senha)

    try:
        # Conectar ao banco de dados
        connection = get_db_connection()
        cursor = connection.cursor()

        # Inserir o usuário na tabela 'usuarios'
        sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_usuario, (nome, email, senha_hash, 'administrador'))
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return f"Erro ao processar os dados: {err}"

    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

    return redirect(url_for('adm_cadastro_bp.sucesso'))  # Correção aqui!

@adm_cadastro_bp.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

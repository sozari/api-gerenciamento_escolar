from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash
import mysql.connector
from utils import connect_to_database

professor_cadastro_bp = Blueprint('professor_cadastro_bp', __name__)

# Rota para exibir o formulário de cadastro de professor
@professor_cadastro_bp.route('/professor_cadastro', methods=['GET'])
def mostrar_formulario_professor():
    return render_template('professor_cadastro.html')

# Rota para processar os dados do formulário via POST
@professor_cadastro_bp.route('/professor_cadastro', methods=['POST'])
def submit_formulario_professor():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if not nome or not email or not senha:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios!'}), 400

    senha_hash = generate_password_hash(senha)

    sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
    sql_professor = "INSERT INTO professor (idusuario) VALUES (%s)"

    try:
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()
            mycursor.execute(sql_usuario, (nome, email, senha_hash, 'professor'))
            idusuario = mycursor.lastrowid
            mycursor.execute(sql_professor, (idusuario,))
            mydb.commit()

            return jsonify({'mensagem': 'Dados do professor cadastrados com sucesso!'}), 201

    except mysql.connector.Error as error:
        return jsonify({'error': f'Erro ao processar os dados: {str(error)}'}), 500

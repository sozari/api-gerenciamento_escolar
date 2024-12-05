from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash
import mysql.connector
from utils import connect_to_database

adm_cadastro_bp = Blueprint('adm_cadastro_bp', __name__)

# Rota para exibir o formulário de cadastro de administrador
@adm_cadastro_bp.route('/adm_cadastro', methods=['GET'])
def mostrar_formulario_adm():
    return render_template('adm_cadastro.html')

# Rota para processar os dados do formulário via POST
@adm_cadastro_bp.route('/adm_cadastro', methods=['POST'])
def submit_formulario_adm():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if not nome or not email or not senha:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios!'}), 400

    senha_hash = generate_password_hash(senha)

    sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
    sql_adm = "INSERT INTO administrador (idusuario) VALUES (%s)"

    try:
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()
            mycursor.execute(sql_usuario, (nome, email, senha_hash, 'administrador'))
            idusuario = mycursor.lastrowid
            mycursor.execute(sql_adm, (idusuario,))
            mydb.commit()

            return jsonify({'mensagem': 'Dados do administrador cadastrados com sucesso!'}), 201

    except mysql.connector.Error as error:
        return jsonify({'error': f'Erro ao processar os dados: {str(error)}'}), 500

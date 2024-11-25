from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from utils import connect_to_database

professor_cadastro_bp = Blueprint('professor_cadastro_bp', __name__)

@professor_cadastro_bp.route('/professor_cadastro', methods=['POST'])
def professor_cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone = request.form['telefone']

    if not nome or not email or not senha or not telefone:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios!'}), 400

    senha_hash = generate_password_hash(senha)

    try:
        with connect_to_database() as db:
            cursor = db.cursor()

            sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_usuario, (nome, email, senha_hash, 'professor'))
            idusuario = cursor.lastrowid

            sql_professor = "INSERT INTO professor (idusuario, telefone) VALUES (%s, %s)"
            cursor.execute(sql_professor, (idusuario, telefone))
            db.commit()

            return jsonify({'mensagem': 'Professor cadastrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

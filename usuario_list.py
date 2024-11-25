from flask import Blueprint, jsonify
import mysql.connector

usuario_list_bp = Blueprint('usuario_list_bp', __name__)

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

@usuario_list_bp.route('/usuario_list', methods=['GET'])
def listar_usuarios():
    try:
        with get_db_connection() as mydb:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT idusuario, nome, email, tipo_usuario FROM usuarios")
            usuarios = mycursor.fetchall()

            # Criar uma lista de dicionários para retornar como JSON
            lista_usuarios = [
                {'idusuario': usuario[0], 'nome': usuario[1], 'email': usuario[2], 'tipo_usuario': usuario[3]}
                for usuario in usuarios
            ]
            return jsonify(lista_usuarios), 200

    except mysql.connector.Error as error:
        return jsonify({'error': f'Erro ao listar os usuários: {str(error)}'}), 500

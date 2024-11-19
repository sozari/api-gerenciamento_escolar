from flask import Blueprint, request, jsonify
import mysql.connector

adm_delete_bp = Blueprint('adm_delete_bp', __name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

@adm_delete_bp.route('/adm_delete/<int:idusuario>/<string:tipo_usuario>', methods=['DELETE'])
def deletar_usuario(idusuario, tipo_usuario):
    try:
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()

            # Verifica se o tipo_usuario é 'administrador'
            if tipo_usuario == 'administrador':
                # Primeiro, deleta os registros da tabela 'usuarios' relacionados ao usuário
                delete_aluno_sql = "DELETE FROM usuarios WHERE idusuario = %s"
                mycursor.execute(delete_aluno_sql, (idusuario,))
                if mycursor.rowcount == 0:
                    return jsonify({'mensagem': 'Nenhum administrador encontrado com este ID.'}), 404

            mydb.commit()
            return jsonify({'mensagem': f'{tipo_usuario.capitalize()} excluído com sucesso!'}), 200

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500



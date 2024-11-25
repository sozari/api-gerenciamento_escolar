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
                # Verifica se o usuário existe antes de tentar excluir
                check_sql = "SELECT * FROM usuarios WHERE idusuario = %s AND tipo_usuario = %s"
                mycursor.execute(check_sql, (idusuario, tipo_usuario))
                user = mycursor.fetchone()

                if user is None:
                    return jsonify({'mensagem': 'Nenhum administrador encontrado com este ID.'}), 404

                # Exclui o usuário da tabela 'usuarios'
                delete_sql = "DELETE FROM usuarios WHERE idusuario = %s AND tipo_usuario = %s"
                mycursor.execute(delete_sql, (idusuario, tipo_usuario))
                
                # Verifica se a exclusão foi bem-sucedida
                if mycursor.rowcount > 0:
                    mydb.commit()
                    return jsonify({'mensagem': 'Administrador excluído com sucesso!'}), 200
                else:
                    return jsonify({'mensagem': 'Erro ao excluir administrador. Tente novamente.'}), 500

            return jsonify({'mensagem': 'Tipo de usuário não suportado para exclusão.'}), 400

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500

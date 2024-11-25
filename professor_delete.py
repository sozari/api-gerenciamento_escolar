from flask import Blueprint, jsonify
import mysql.connector

professor_delete_bp = Blueprint('professor_delete_bp', __name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

@professor_delete_bp.route('/professor_delete/<int:idusuario>', methods=['DELETE'])
def deletar_professor(idusuario):
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        )
        mycursor = mydb.cursor()

        # Exclui primeiro os registros relacionados na tabela 'professor'
        delete_professor_sql = "DELETE FROM professor WHERE idusuario = %s"
        mycursor.execute(delete_professor_sql, (idusuario,))

        # Em seguida, exclui o registro na tabela 'usuarios'
        delete_usuario_sql = "DELETE FROM usuarios WHERE idusuario = %s"
        mycursor.execute(delete_usuario_sql, (idusuario,))

        if mycursor.rowcount == 0:
            # Nenhum registro foi encontrado para exclusão
            return jsonify({'mensagem': 'Nenhum professor encontrado com este ID.'}), 404

        mydb.commit()
        return jsonify({'mensagem': 'Professor excluído com sucesso!'}), 200

    except mysql.connector.Error as error:
        # Trata erros relacionados ao banco de dados
        return jsonify({'error': f'Erro no banco de dados: {str(error)}'}), 500
    finally:
        # Garante o fechamento da conexão e do cursor
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

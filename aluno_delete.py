from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

@app.route('/aluno_delete/<int:idusuario>/<string:tipo_usuario>', methods=['DELETE'])
def deletar_usuario(idusuario, tipo_usuario):
    try:
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()

            # Verifica se o tipo_usuario é 'aluno' ou 'professor'
            if tipo_usuario == 'aluno':
                # Primeiro, deleta os registros da tabela 'aluno' relacionados ao usuário
                delete_aluno_sql = "DELETE FROM aluno WHERE idusuario = %s"
                mycursor.execute(delete_aluno_sql, (idusuario,))
                if mycursor.rowcount == 0:
                    return jsonify({'mensagem': 'Nenhum aluno encontrado com este ID.'}), 404
            elif tipo_usuario == 'professor':
                # Deleta os registros da tabela 'professor' relacionados ao usuário
                delete_professor_sql = "DELETE FROM professor WHERE idusuario = %s"
                mycursor.execute(delete_professor_sql, (idusuario,))
                if mycursor.rowcount == 0:
                    return jsonify({'mensagem': 'Nenhum professor encontrado com este ID.'}), 404

            # Depois de remover da tabela correspondente, deleta o usuário da tabela 'usuarios'
            delete_usuario_sql = "DELETE FROM usuarios WHERE idusuario = %s AND tipo_usuario = %s"
            mycursor.execute(delete_usuario_sql, (idusuario, tipo_usuario))

            if mycursor.rowcount == 0:
                return jsonify({'mensagem': 'Nenhum usuário encontrado com este ID e tipo de usuário.'}), 404

            mydb.commit()
            return jsonify({'mensagem': f'{tipo_usuario.capitalize()} excluído com sucesso!'}), 200

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)

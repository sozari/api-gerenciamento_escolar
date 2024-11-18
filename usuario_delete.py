from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

@app.route('/usuario_delete/<int:idusuario>', methods=['DELETE'])
def del_usuario(idusuario):
    try:
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()

            # Verificar se o usuário está na tabela aluno
            mycursor.execute("SELECT COUNT(*) FROM aluno WHERE idusuario = %s", (idusuario,))
            aluno_count = mycursor.fetchone()[0]

            # Verificar se o usuário está na tabela professor
            mycursor.execute("SELECT COUNT(*) FROM professor WHERE idusuario = %s", (idusuario,))
            professor_count = mycursor.fetchone()[0]

            # Se o usuário estiver na tabela aluno, exclua o registro de aluno primeiro
            if aluno_count > 0:
                mycursor.execute("DELETE FROM aluno WHERE idusuario = %s", (idusuario,))
                mydb.commit()

            # Se o usuário estiver na tabela professor, exclua o registro de professor primeiro
            if professor_count > 0:
                mycursor.execute("DELETE FROM professor WHERE idusuario = %s", (idusuario,))
                mydb.commit()

            # Agora, exclua o registro de usuário na tabela usuarios
            sql_delete_usuario = "DELETE FROM usuarios WHERE idusuario = %s"
            mycursor.execute(sql_delete_usuario, (idusuario,))
            mydb.commit()

            if mycursor.rowcount == 0:
                return jsonify({'mensagem': 'Nenhum usuário encontrado com este ID.'}), 404

            return jsonify({'mensagem': 'Usuário e seus registros relacionados (aluno/professor) deletados com sucesso!'}), 200

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500


if __name__ == '__main__':
    app.run(debug=True)

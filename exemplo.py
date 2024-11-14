from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciador_escolar'

# Rota para processar o formulário
@app.route('/submit_formulario', methods=['POST'])
def submit_formulario():
    # Obter dados do formulário
    
    aluno = request.form['aluno']
    nota1 = request.form['nota1']
    nota2 = request.form['nota2']
    nota3 = request.form['nota3']
    media = request.form['media']

    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Executar comando SQL para inserir dados
        sql = "INSERT INTO turma (aluno, nota1, nota2, nota3, media) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (aluno, nota1, nota2, nota3, media))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return "Erro ao processar os dados. Tente novamente mais tarde."
    finally:
        # Fechar conexão com o banco de dados
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

    # Redirecionar para página de sucesso ou outra página
    return redirect(url_for('sucesso'))

# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)

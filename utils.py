import mysql.connector
import os

# Função para conectar ao banco de dados
def connect_to_database():
    db_host = os.getenv('localhost')
    db_user = os.getenv('root')
    db_password = os.getenv('')
    db_name = os.getenv('gerenciamento_escolar')

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
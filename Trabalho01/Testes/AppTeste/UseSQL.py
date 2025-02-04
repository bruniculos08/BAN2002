import mysql.connector
import psycopg2
from mysql.connector import Error
import pandas as pd

# (1) Criando objeto de conexão com o banco de dados:
conn = psycopg2.connect(database="Mecânica de Veículos (para Funções)",
                        host="localhost",
                        user="postgres",
                        password="1234",
                        port="5433")

# (2) Criando um objeto cursor para realizar query's:
cursor = conn.cursor()

# (3) Executando um comando SQL por meio do objeto cursor:
cursor.execute("DELETE FROM mecanico where cpf = '88787055511' ")
cursor.execute("INSERT INTO mecanico VALUES(7, '88787055511', 'Python', 54, 'Central Park', 'New York', 'desamassa', 3)")
cursor.execute("SELECT * FROM mecanico")

# (4) Printando a primeira linha obtida da última query executada:
print(cursor.fetchone())

# (5) Printando todas as linhas obtidas da última query executada:
for line in cursor.fetchall():
    print(line)

# (6) Printando uma determinada quantidade de linhas da última query executada:
for line in cursor.fetchmany(size = 4):
    print(line)
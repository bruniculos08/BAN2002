from concurrent.futures import as_completed
import pandas as pd
import mysql.connector
import psycopg2
from mysql.connector import Error

# (1) Criando objeto de conexão com o banco de dados:
conn = psycopg2.connect(database="IMDB Titles",
                        host="localhost",
                        user="postgres",
                        password="1234",
                        port="5433")

# (2) Criando um objeto cursor para realizar query's:
cursor = conn.cursor()

# (3) Abrindo e lendo o arquivo csv:
csv_file = pd.read_table('data.csv', sep=',', low_memory=False)

# (4) Criando uma dataBase de pandas por meio do arquivo csv:
dataBase = pd.DataFrame(csv_file)
print(dataBase)

# (5) Criando a tabela para colocar os dados no banco de dados:
#cursor.execute("delete from filmes")
cursor.execute('''create table filmes 
                (movie_id char(10), 
                titleType varchar(50), 
                primaryTitle varchar(200), 
                originalTitle varchar(200), 
                isAdult integer,
                startYear varchar (10),
                endYear varchar (10),
                runtimeMinutes varchar (200),
                genres varchar (200),
                primary key (movie_id))
                ''')

# (6) Inserindo os dados no banco de dados:
for row in dataBase.itertuples():
    cursor.execute('''insert into filmes values ('%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s')''' 
    %(row.tconst, row.titleType, row.primaryTitle.replace('\'', '')[1:50], row.originalTitle.replace('\'', '')[1:50], row.isAdult, row.startYear, 
    row.endYear, row.runtimeMinutes[1:200], row.genres))

    print(row.originalTitle)
conn.commit()
# Camada de interface com usuário; 
# Camada de negócios, com a lógica da aplicação; e
# Camada de dados, com funcionalidade de armazenamento e recuperação.

# Camada de apresentação (view), camada de negócio (controller) e camada de persistência.
# Objeto da camada de dados -> só contém atributos e estão diretamente relacionados com o esquema do banco de dados(ER,...
# ... no máximo pode (e deve ter) os métodos de 'Get' e 'Set' (o acesso aos atributos não deve ser direto).
# Objeto da camada de negócio -> exemplo: uma turma não pode estar lotada, para isso tem se uma classe que se comunica com...
# ... o banco de dados para inserir mas faz alguma verificação como verificar se a turma está lotada.
# Objeto da camada de persistência -> se comunica com o banco de dados e transforma linhas do banco de dados em objetos.

from View import *
import mysql.connector
import psycopg2
from mysql.connector import Error
import pandas as pd

if __name__ == "__main__":
    app = View()
    app.run()
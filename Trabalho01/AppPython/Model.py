# Camada de interface com usuário; 
# Camada de negócios, com a lógica da aplicação (na qual se encontra); e
# Camada de dados, com funcionalidade de armazenamento e recuperação.

import psycopg2 as postgres

class Connection():

    __instance = None
    __connection = None

#    About __new__ vs __init__ constructor methods:
#
#   - Python __new__() is the constructor method that controls the creation of the new instance.                    
#   - It is called first and it returns a new class instance.                                   
#                    
#   - Python __init__() is the initializer method to set the attributes (i.e., state) of the newly-created instance.
#   - It is called after creation and returns nothing, i.e., None.              
#
#   About cls vs self attributes and methods:
#
#   - cls is about the class and self is about a particular instance of the class.
      
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__connection = postgres.connect(database="Mecânica de Veículos (para Funções)",
                    host="localhost",
                    user="postgres",
                    password="1234",
                    port="5433")
        return cls.__instance
    
    def cursor(self):
        return self.__connection.cursor()
    
    def commit(self):
        self.__connection.commit()

    def close(self):
        return self.__connection.close()        

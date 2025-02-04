# Camada de interface com usuário; 
# Camada de negócios, com a lógica da aplicação (na qual se encontra); e
# Camada de dados, com funcionalidade de armazenamento e recuperação.

from pymongo import MongoClient

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
            cls.__connection = MongoClient("mongodb://localhost:27017")
        return cls.__instance

    def getCollection(self, database_name, collection_name):
        return self.__connection[database_name][collection_name]

    def close(self):
        return self.__connection.close()

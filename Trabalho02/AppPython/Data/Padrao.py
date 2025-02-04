from Model import *

# Para herdar métodos delete e update:
class PadraoDAO():

    __collection = None
    __mongoDBFields = None
    __connection = None

    def __init__(self, mongoDBFields, dataBaseName, collectionName):
        self.__mongoDBFields = mongoDBFields
        self.__connection = Connection()
        self.__collection = self.__connection.getCollection(dataBaseName, collectionName)

    def findAll(self, dataCond = []):

        # Monta o dicionário que contem os atributos do novo item...
        # ... a ser procurado na collection:
        dictionaryCond = {}
        for field, value in zip(self.__mongoDBFields, dataCond):
            if value != "":
                dictionaryCond[field] = value

        return self.__collection.find(dictionaryCond)

    def project(self, projectFields):

        dictionaryFields = {}
        for field, projectField in zip(self.__mongoDBFields, projectFields):
            if projectField == 0:
                dictionaryFields[field] = 0

        dictionaryFields = {"$project": dictionaryFields}

        return self.__collection.aggregate([dictionaryFields])


    def insert(self, dataSet):

        # Monta o dicionário que contem os atributos do novo item...
        # ... a ser adicionado na collection:
        dictionarySet = {}
        for field, value in zip(self.__mongoDBFields, dataSet):
            if(value == "" and field != "_id"):
                raise Exception()
            elif(value != ""):
                dictionarySet[field] = value
                

        self.__collection.insert_one(dictionarySet)

    def delete(self, data):

        # Monta o dicionário cujos campos representão os valores dos respectivos campos...
        # ... dos documentos a serem deletados:
        dictionaryCond = {}
        for field, value in zip(self.__mongoDBFields, data):
            if value != "":
                dictionaryCond[field] = value

        # Deleta a lista de documentos:
        return self.__collection.delete_many(dictionaryCond)

    def update(self, dataSet, dataCond, operator):

        # Monta o dicionário cujos campos representão os antigos valores dos respectivos campos...
        # ... dos documentos a serem atualizados:
        dictionaryCond = {}
        for field, value in zip(self.__mongoDBFields, dataCond):
            if value != "":
                dictionaryCond[field] = value

        # Monta o dicionário cujos campos representão os novos valores dos respectivos campos...
        # ... dos documentos a serem atualizados:
        dictionarySet = {}
        for field, value in zip(self.__mongoDBFields, dataSet):
            if value != "":
                dictionarySet[field] = value  

        dictionarySet = {operator: dictionarySet}
        
        return self.__collection.update_many(dictionaryCond, dictionarySet)
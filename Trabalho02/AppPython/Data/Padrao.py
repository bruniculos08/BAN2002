from Model import *
from Data.Padrao import *

# Para herdar métodos delete e update:
class PadraoDAO():

    __collectionName = None
    __mongoDBFields = None

    def __init__(self, collectionName, mongoDBInsert, mongoDBUpdate, mongoDBDelete, mongoDBFind, mongoDBFields):
        self.__collectionName = collectionName
        self.__mongoDBFields = mongoDBFields

    def insert(self, collection_item):
        collection_item.save()

    def delete(self, dados = None):
        con = Connection()
        collection = con.getCollection("Personalização", self.__collectionName)

        # Construindo condicionais:
        string = "{"
        for field, dado in zip(self.__mongoDBFields, dados):
            if dado != "":
                string += "\'" + field + "\'" + ":" + "\'" + dado + "\'"
        string += "}"
        collection.deleteMany({string})

    def update(self, operator, dadosSet,  dadosCond):
        con = Connection()
        collection = con.getCollection("Personalização", self.__collectionName)

        # Construindo condicionais:
        stringCond = {}
        for field, dado in zip(self.__mongoDBFields, dadosCond):
            if dado != "":
                stringCond[field] = dado

        # Montando argumento de alteração:
        stringSet = {}
        for field, dado in zip(self.__mongoDBFields, dadosSet):
            if dado != "":
               stringSet[field] = dado

        collection.update(stringCond, {operator: stringSet})
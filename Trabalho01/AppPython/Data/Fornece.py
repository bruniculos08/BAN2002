from Model import *
from Data.Padrao import *

class Fornece():

    __nome = None
    __cnpj = None

    def __init__(self):
        self.__nome = ""
        self.__cnpj = ""
        
    def nome(self, nome):
        self.__nome = nome
        return self
    
    def getNome(self):
        return self.__nome
    
    def cnpj(self ,cnpj):
        self.__cnpj = cnpj
        return self
    
    def getCnpj(self):
        return self.__cnpj
    
    def fromTupla(self, tupla):
        self.__nome = tupla[0]
        self.__cnpj = tupla[1]
        return self
    
    def __repr__(self):
        return u'{}:{}'.format(self.__nome, self.__cnpj)
    
class ForneceDAO(PadraoDAO):

    __sqlSelectAll = None
    __sqlInsert = None
    # __sqlDelete = None
    # __sqlUpdate = None
    # __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from fornece"
        self.__sqlInsert = "insert into fornece values('{}', '{}')"
        # self.__sqlDelete = "delete from fornece"
        # self.__sqlUpdate = "update fornece set"
        # self.__columns = ["nome_componente", "cnpj"]
        super().__init__("delete from fornece", "update fornece set", ["nome_componente", "cnpj"])

    # Retorna uma lista com um objeto de cada componente_necessario do banco de dados:
    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        fornecem = []
        for line in result:
            fornecem.append(Fornece().fromTupla(line))
        return fornecem
    
    def insertFornece(self, fornece):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(fornece.getNome(), fornece.getCnpj()))
        con.commit()
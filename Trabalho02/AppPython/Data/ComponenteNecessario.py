from Model import *
from Data.Padrao import *

class ComponenteNecessario():

    __nome = None
    __codDept = None
    __quantidade = None

    def __init__(self):
        self.__nome = ""
        self.__codDept = -1

    def nome(self, nome):
        self.__nome = nome
        return self
    
    def getNome(self):
        return self.__nome
    
    def codDept(self ,codDept):
        self.__codDept = codDept
        return self
    
    def getCodDept(self):
        return self.__codDept
    
    def quantidade(self, quantidade):
        self.__quantidade = quantidade
        return self
    
    def getQuantidade(self):
        return self.__quantidade
    
    def fromTupla(self, tupla):
        self.__nome = tupla[0]
        self.__codDept = tupla[1]
        self.__quantidade = tupla[2]
        return self
    
    def __repr__(self):
        return u'{}:{}:{}'.format(self.__nome, self.__codDept, self.__quantidade)
    
class ComponenteNecessarioDAO(PadraoDAO):

    __sqlSelectAll = None
    __sqlInsert = None
    # __sqlDelete = None
    # __sqlUpdate = None
    # __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from componente_necessario"
        self.__sqlInsert = "insert into componente_necessario values('{}', '{}', {})"
        # self.__sqlDelete = "delete from componente_necessario"
        # self.__sqlUpdate = "update componente_necessario set"
        # self.__columns = ["cod_dept", "nome_componente", "quantidade"]
        super().__init__("delete from componente_necessario", "update componente_necessario set", ["cod_dept", "nome_componente", "quantidade"])

    # Retorna uma lista com um objeto de cada componente_necessario do banco de dados:
    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        componentesNecessarios = []
        for line in result:
            componentesNecessarios.append(ComponenteNecessario().fromTupla(line))
        return componentesNecessarios
    
    def insertComponenteNecessario(self, componenteNecessario):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(componenteNecessario.getNome(), componenteNecessario.getCodDept(), componenteNecessario.getQuantidade()))
        con.commit()
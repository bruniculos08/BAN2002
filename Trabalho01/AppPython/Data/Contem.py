from Model import *
from Data.Padrao import *

class Contem():

    __nome = None
    __idPedido = None
    __quantidade = None

    def __init__(self):
        self.__nome = ""
        self.__idPedido = -1
        self.__quantidade = 0

    def nome(self, nome):
        self.__nome = nome
        return self
    
    def getNome(self):
        return self.__nome
    
    def idPedido(self, idPedido):
        self.__idPedido = idPedido
        return self

    def getIdPedido(self):
        return self.__idPedido

    def quantidade(self, quantidade):
        self.__quantidade = quantidade
        return self
    
    def getQuantidade(self):
        return self.__quantidade
    
    def fromTupla(self, tupla):
        self.__nome = tupla[0]
        self.__idPedido = tupla[1]
        self.__quantidade = tupla[2]
        return self
    
    def __repr__(self):
        return u'{}:{}:{}'.format(self.__nome, self.__idPedido, self.__quantidade)
    
class ContemDAO(PadraoDAO):

    __sqlSelectAll = None
    __sqlInsert = None
    # __sqlDelete = None
    # __sqlUpdate = None
    # __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from contem"
        self.__sqlInsert = "insert into contem values('{}', {}, {})"
        # self.__sqlDelete = "delete from contem"
        # self.__sqlUpdate = "update contem set"
        # self.__columns = ["nome_componente", "id_pedido", "quantidade"]
        super().__init__("delete from contem", "update contem set", ["nome_componente", "id_pedido", "quantidade"])


    # Retorna uma lista com um objeto de cada contem do banco de dados:
    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        contemLista = []
        for line in result:
            contemLista.append(Contem().fromTupla(line))
        return contemLista
    
    def insertContem(self, contem):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(contem.getNome(), contem.getIdPedido(), contem.getQuantidade()))
        con.commit()
from Model import *
from Data.Padrao import *

class Pedido():

    __id = None
    __dataCriacao = None
    __cnpj = None
    __codDeptCompra = None

    def __init__(self):
        self.__id = -1
        self.__dataCriacao = ''
        self.__cnpj = ""
        self.__codDeptCompra = -1

    def id(self, id):
        self.__id = id
        return self
    
    def getId(self):
        return self.__id
    
    def dataCriacao(self, dataCriacao):
        self.__dataCriacao = dataCriacao
        return self
    
    def getDataCriacao(self):
        return self.__dataCriacao

    def cnpj(self, cnpj):
        self.__cnpj = cnpj
        return self

    def getCnpj(self):
        return self.__cnpj
    
    def codDeptCompra(self, codDeptCompra):
        self.__codDeptCompra = codDeptCompra
        return self
    
    def getCodDeptCompra(self):
        return self.__codDeptCompra

    def fromTupla(self, tupla):
        self.__idPedido = tupla[0]
        self.__dataCriacao = tupla[1]
        self.__cnpj = tupla[2]
        self.__codDeptCompra = tupla[3]
        return self
    
    def __repr__(self):
        return u'{}:{}:{}:{}'.format(self.__idPedido, self.__dataCriacao, self.__cnpj, self.__codDeptCompra)    

class PedidoDAO(PadraoDAO):

    __sqlSelectAll = None
    __sqlSelectNewId= None
    __sqlInsert = None
    # __sqlDelete = None
    # __sqlUpdate = None
    # __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from pedido"
        self.__sqlSelectNewId = "select nextval('pedido_id')"
        self.__sqlInsert = "insert into pedido values({}, '{}', '{}', {})"
        # self.__sqlDelete = "delete from pedido"
        # self.__sqlUpdate = "update pedido set"
        # self.__columns = ["id", "valor", "data_criacao", "cnpj", "cod_dept_compra"]
        super().__init__("delete from pedido", "update pedido set", ["id", "data_criacao", "cnpj", "cod_dept_compra"])

    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        pedidos = []
        for line in result:
            pedidos.append(Pedido().fromTupla(line))
        return pedidos

    def __selectNewId(self) -> int:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectNewId)
        result = cursor.fetchone()
        return result[0]

    def insertPedido(self, pedido):
        id = self.__selectNewId()
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(id, pedido.getDataCriacao(), pedido.getCnpj(), pedido.getCodDeptCompra()))
        con.commit()
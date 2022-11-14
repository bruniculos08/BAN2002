from Model import *

class Pedido():

    __id = None
    __valor = None
    __cnpj = None
    __codDeptCompra = None

    def __init__(self):
        self.__id = -1
        self.__valor = 0
        self.__cnpj = ""
        self.__codDeptCompra = -1

    def id(self, id):
        self.__id = id
        return self
    
    def getId(self):
        return self.__id

    def valor(self, valor):
        self.__valor = valor
        return self
    
    def getValor(self):
        return self.__valor

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
        self.__valor = tupla[1]
        self.__cnpj = tupla[2]
        self.__codDeptCompra = tupla[3]
        return self
    
    def __repr__(self):
        return u'{}:{}:{}:{}'.format(self.__idPedido, self.__valor, self.__cnpj, self.__codDeptCompra)    

class PedidoDAO():

    __sqlSelectAll = None
    __sqlSelectNewId= None
    __sqlInsert = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from pedido"
        self.__sqlSelectNewId = "select nextval('pedido_id')"
        self.__sqlInsert = "insert into pedido values({}, {}, '{}', {})"

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
        cursor.execute(self.__sqlInsert.format(id, pedido.getCnpj(), pedido.getCodDeptCompra()))
        con.commit()

    def delete(self, campos = None, dados = None):
        con = Connection()
        cursor = con.cursor()

        # Se não há condicionais se deletam todos as linhas:
        if campos is None:
            cursor.execute(self.__sqlDelete)

        # Construindo condicionais:
        string = ""
        for campo, dado in zip(campos, dados):
            if dado == "":
                continue
            string = string + " " + campo + " = " + dado
            if campo != campos[-1]:
                string = string + ","
        
        cursor.execute(self.__sqlDelete + " " + "where" + string)
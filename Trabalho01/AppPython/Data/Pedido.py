from Model import *

class Pedido():

    __id = None
    __valor = None
    __dataCriacao = None
    __cnpj = None
    __codDeptCompra = None

    def __init__(self):
        self.__id = -1
        self.__valor = 0
        self.__dataCriacao = 'YYYY-MM-DD'
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
    
    def dataCriacao(self, dataCriacao):
        self.__dataCriacao = dataCriacao
        return self
    
    def getDataCriacao(self):
        self.__dataCriacao

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
    __sqlDelete = None
    __sqlUpdate = None
    __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from pedido"
        self.__sqlSelectNewId = "select nextval('pedido_id')"
        self.__sqlInsert = "insert into pedido values({}, '{}', '{}', {})"
        self.__sqlDelete = "delete from pedido"
        self.__sqlUpdate = "update pedido set"
        self.__columns = ["id", "valor", "data_criacao", "cnpj", "cod_dept_compra"]

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
        cursor.execute(self.__sqlInsert.format(id, pedido.getValor(), pedido.getDataCriacao(), pedido.getCnpj(), pedido.getCodDeptCompra()))
        con.commit()

    def delete(self, dados = None):
        con = Connection()
        cursor = con.cursor()
        campos = self.__columns

        # Construindo condicionais:
        string = ""
        for campo, dado in zip(campos, dados):
            if dado == '' or dado == '\'\'':
                continue
            if len(string) > 0:
                string = string + "," + " " + campo + " = " + dado
            else:
                string = string + " " + campo + " = " + dado

        # Se não há condicional:
        if string == "":
            cursor.execute(self.__sqlDelete) 
        
        cursor.execute(self.__sqlDelete + " " + "where" + string)

    def update(self, dadosSet,  dadosWhere):
        con = Connection()
        cursor = con.cursor()
        campos = self.__columns

        stringSet = ""
        stringWhere = ""

        # Montando stringSet:
        for campo, dado in zip(campos, dadosSet):
            if dado == '' or dado == '\'\'':
                continue
            if len(stringSet) > 0:
                stringSet = stringSet + "," + " " + campo + " = " + dado
            else:
                stringSet = stringSet + " " + campo + " = " + dado

        # Montando stringWhere:
        for campo, dado in zip(campos, dadosWhere):
            if dado == '' or dado == '\'\'':
                continue
            if len(stringWhere) > 0:
                stringWhere = stringWhere + "," + " " + campo + " = " + dado
            else:
                stringWhere = stringWhere + " " + campo + " = " + dado

        # Se não há condicional:
        if stringWhere == "":
            cursor.execute(self.__sqlUpdate + " " + stringSet) 

        cursor.execute(self.__sqlUpdate + stringSet + " " + "where" + stringWhere)
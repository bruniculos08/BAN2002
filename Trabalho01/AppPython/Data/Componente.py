from Model import *
from Data.Padrao import *

class Componente():

    __nome = None
    __tipo = None
    __valorCompra = None
    __quantidadeMin = None
    __quantidade = None
    __cnpjPrincipal = None

    def __init__(self):
        self.__nome = ""
        self.__tipo = ""
        self.__valorCompra = 0.0
        self.__quantidadeMin = -1
        self.__quantidade = -1
        self.__cnpjPrincipal = ""

    def nome(self, nome):
        self.__nome = nome
        return self
    
    def getNome(self):
        return self.__nome
    
    def tipo(self, tipo):
        self.__tipo = tipo
        return self

    def getTipo(self):
        return self.__tipo

    def valorCompra(self, valorCompra):
        self.__valorCompra = valorCompra
        return self

    def getValorCompra(self):
        return self.__valorCompra
    
    def quatidadeMin(self, quatidadeMin):
        self.__quantidadeMin = quatidadeMin
        return self
    
    def getQuatidadeMin(self):
        return self.__quantidadeMin
    
    def quantidade(self, quantidade):
        self.__quantidade = quantidade
        return self
    
    def getQuantidade(self):
        return self.__quantidade
    
    def cnpjPrincipal(self, cnpjPrincipal):
        self.__cnpjPrincipal = cnpjPrincipal
        return self
    
    def getCnpjPrincipal(self):
        return self.__cnpjPrincipal
    
    def fromTupla(self, tupla):
        self.__nome = tupla[0]
        self.__tipo = tupla[1]
        self.__valorCompra = tupla[2]
        self.__quantidadeMin = tupla[3]
        self.__quantidade = tupla[4]
        self.__cnpjPrincipal = tupla[5]
        return self
    
    def __repr__(self):
        return u'{}:{}:{}:{}:{}:{}'.format(self.__nome, self.__tipo, self.__valorCompra, self.__quantidadeMin, self.__quantidade, self.__cnpjPrincipal)
    
class ComponenteDAO(PadraoDAO):

    __sqlSelectAll = None
    __sqlInsert = None
    # __sqlDelete = None
    # __sqlUpdate = None
    # __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from componente"
        self.__sqlInsert = "insert into componente values('{}', '{}', {}, {}, {}, '{}')"
        # self.__sqlDelete = "delete from componente"
        # self.__sqlUpdate = "update componente set"
        # self.__columns = ["nome", "tipo", "minimo_quant", "quantidade", "cnpj_principal"]
        super().__init__("delete from componente", "update componente set", ["nome", "tipo", "valor_compra", "minimo_quant", "quantidade", "cnpj_principal"])

    # Retorna uma lista com um objeto de cada componente do banco de dados:
    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        componentes = []
        for line in result:
            componentes.append(Componente().fromTupla(line))
        return componentes
    
    def insertComponente(self, componente):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(componente.getNome(), componente.getTipo(), 
            componente.getValorCompra(), componente.getQuatidadeMin(),
            componente.getQuantidade(), componente.getCnpjPrincipal()))
        con.commit()
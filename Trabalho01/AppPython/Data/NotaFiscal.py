from Model import *
from Data.Padrao import *

class NotaFiscal():

    __codNota = None
    __idPedido = None

    def __init__(self):
        self.__codNota = ""
        self.__idPedido = -1

    def codNota(self, codNota):
        self.__codNota = codNota
        return self
    
    def getCodNota(self):
        return self.__codNota
    
    def idPedido(self, idPedido):
        self.__idPedido = idPedido
        return self
    
    def getIdPedido(self):
        return self.__idPedido
    
    def fromTupla(self, tupla):
        self.__codNota = tupla[0]
        self.__idPedido = tupla[1]
        return self
    
    def __repr__(self):
        return u'{}:{}'.format(self.__codNota, self.__idPedido)

class NotaFiscalDAO(PadraoDAO):
    
    __sqlSelectAll = None
    __sqlInsert = None
    # __sqlDelete = None
    # __sqlUpdate = None
    # __columns = None
    __sqlSelectNewCodNota= None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from nota_fiscal"
        self.__sqlInsert = "insert into nota_fiscal values('{}', {})"
        # self.__sqlDelete = "delete from nota_fiscal"
        # self.__sqlUpdate = "update nota_fiscal set"
        # self.__columns = ["cod_nota", "id_pedido"]
        super().__init__("delete from nota_fiscal", "update nota_fiscal set", ["cod_nota", "id_pedido"])

    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        notas = []
        for line in result:
            notas.append(NotaFiscal().fromTupla(line))
        return notas

    def insertNotaFiscal(self, notaFiscal):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(notaFiscal.getCodNota(), notaFiscal.getIdPedido()))
        con.commit()
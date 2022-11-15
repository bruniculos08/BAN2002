from Model import *

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

class NotaFiscalDAO():
    
    __sqlSelectAll = None
    __sqlInsert = None
    __sqlDelete = None
    __sqlUpdate = None
    __columns = None
    __sqlSelectNewCodNota= None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from nota_fiscal"
        self.__sqlInsert = "insert into nota_fiscal values('{}', {})"
        self.__sqlDelete = "delete from nota_fiscal"
        self.__sqlUpdate = "update nota_fiscal set"
        self.__columns = ["cod_nota", "id_pedido"]

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
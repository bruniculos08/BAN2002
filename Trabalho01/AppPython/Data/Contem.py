from Model import *

class Contem():

    __nome = None
    __idPedido = None

    def __init__(self):
        self.__nome = ""
        self.__idPedido = -1

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
    
    def fromTupla(self, tupla):
        self.__nome = tupla[0]
        self.__idPedido = tupla[1]
        return self
    
    def __repr__(self):
        return u'{}:{}'.format(self.__nome, self.__idPedido)
    
class ContemDAO():

    __sqlSelectAll = None
    __sqlInsert = None
    __sqlDelete = None
    __sqlUpdate = None
    __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from contem"
        self.__sqlInsert = "insert into contem values('{}', {})"
        self.__sqlDelete = "delete from contem"
        self.__sqlUpdate = "update contem set"
        self.__columns = ["nome_componente", "id_pedido"]

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
        cursor.execute(self.__sqlInsert.format(contem.getNome(), contem.getIdPedido()))
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
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
    
    def __init__(self):
        self.__sqlSelectAll = "select * from contem"
        self.__sqlInsert = "insert into contem values('{}', {})"

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
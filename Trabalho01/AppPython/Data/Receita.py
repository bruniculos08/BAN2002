from Model import *

class Receita():

    __valor = None
    __mes = None
    __ano = None
    
    def __init__(self):
        self.__valor = 0
        self.__mes = 0
        self.__ano = -1

    def valor(self, valor):
        self.__valor = valor
        return self
    
    def getValor(self):
        return self.__valor
    
    def mes(self, mes):
        self.__mes = mes
        return self
    
    def getMes(self):
        return self.__mes
    
    def ano(self, ano):
        self.__ano = ano
        return self
    
    def getAno(self):
        return self.__ano
    
    def fromTupla(self, tupla):
        self.__valor = tupla[0]
        self.__mes = int(tupla[1])
        self.__ano = int(tupla[2])
        return self
    
    def __repr__(self):
        return u'{}:{}:{}'.format(self.__valor, self.__mes, self.__ano)

class ReceitaDAO():

    __sqlSelectAll = None
    __sqlSelectData = None
    __sqlSelectMore = None
    __sqlSelectLess = None
    __columns = None

    def __init__(self):
        self.__sqlSelectAll = "select * from Receita"
        self.__sqlSelectData = "select valor from Receita where"
        self.__sqlSelectMore = "select * from Receita where valor >"
        self.__sqlSelectLess = "select * from Receita where valor <"
        self.__columns = ["valor, mes, ano"]

    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        receitas = []
        for line in result:
            receitas.append(Receita().fromTupla(line))
        return receitas
    
    def selectData(self, mes, ano) -> int:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectData + f" mes = {mes} and ano = {ano}")
        result = cursor.fetchone()
        return result[0]
    
    def selectMore(self, valor):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectMore + f" {valor}")
        result = cursor.fetchall()
        receitas = []
        for line in result:
            receitas.append(Receita().fromTupla(line))
        return receitas
    
    def selectLess(self, valor):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectLess + f" {valor}")
        result = cursor.fetchall()
        receitas = []
        for line in result:
            receitas.append(Receita().fromTupla(line))
        return receitas
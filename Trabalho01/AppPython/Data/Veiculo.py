# Para esta classe precisaremos gerar um chassi:
# https://geradorbrasileiro.com/chassi
from Model import *

class Veiculo():

    __chassi = None
    __valorProducao = None
    __codDept = None

    def __init__(self):
        self.__chassi = ""
        self.__valorProducao = 0
        self.__codDept = -1

    def chassi(self, chassi):
        self.chassi = chassi
        return self
    
    def getChassi(self):
        return self.__chassi
    
    def valorProducao(self, valorProducao):
        self.__valorProducao = valorProducao
        return self
    
    def getValorProducao(self):
        return self.__valorProducao
    
    def codDept(self ,codDept):
        self.__codDept = codDept
        return self
    
    def getCodDept(self):
        return self.__codDept
    
    def fromTupla(self, tupla):
        self.__chassi = tupla[0]
        self.__valorProducao = tupla[1]
        self.__codDept = tupla[2]
    # Obs.: essa função também serve para listas(para qualquer estrutura indexada no geral)!

    def __repr__(self):
        return u'{}:{}:{}'.format(self.__chassi, self.__valorProducao, self.__codDept)
    
class VeiculoDAO():

    __sqlSelectAll = None
    __sqlSelectNewChassi = None
    __sqlInsert = None
    __sqlDelete = None
    __sqlUpdate = None
    __columns = None

    
    def __init__(self):
        self.__sqlSelectAll = "select * from veiculo"
        self.__sqlInsert = "insert into veiculo values('{}', {}, {}, {}, {})" 
        self.__sqlDelete = "delete from veiculo"
        self.__sqlUpdate = "update veiculo set"
        self.__columns = ["chassi", "valor_prod", "cod_dept"]
        
    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        veiculos = []
        for line in result:
            veiculos.append(Veiculo().fromTupla(line))
        return veiculos
    
    def insertVeiculo(self, veiculo):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(veiculo.getChassi(), veiculo.getValorProducao(), veiculo.getCodDept()))
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
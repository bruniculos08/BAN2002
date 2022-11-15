# Para esta classe precisaremos gerar um chassi:
# https://geradorbrasileiro.com/chassi
from Model import *

class Veiculo():

    __chassi = None
    __manualAutomatico = None
    __arCondicionado = None
    __vidrosTravas = None
    __codDept = None

    def __init__(self):
        self.__chassi = ""
        self.__manualAutomatico = False
        self.__arCondicionado = False
        self.__vidrosTravas = False
        self.__codDept = -1

    def chassi(self, chassi):
        self.chassi = chassi
        return self
    
    def getChassi(self):
        return self.__chassi
    
    def manualAutomatico(self, manualAutomatico):
        self.manualAutomatico = manualAutomatico
        return self
    
    def getManualAutomatico(self):
        return self.__manualAutomatico

    def vidroTravas(self, vidroTravas):
        self.__vidrosTravas = vidroTravas
        return self
    
    def getVidroTravas(self):
        return self.__vidrosTravas
    
    def arCondicionado(self, arCondicionado):
        self.__arCondicionado = arCondicionado
        return self
    
    def getArCondicionado(self):
        return self.__arCondicionado
    
    def codDept(self ,codDept):
        self.__codDept = codDept
        return self
    
    def getCodDept(self):
        return self.__codDept
    
    def fromTupla(self, tupla):
        self.__chassi = tupla[0]
        self.__manualAutomatico = tupla[1]
        self.__arCondicionado = tupla[2]
        self.__vidrosTravas = tupla[3]
        self.__codDept = tupla[4]
    # Obs.: essa função também serve para listas(para qualquer estrutura indexada no geral)!

    def __repr__(self):
        return u'{}:{}:{}:{}:{}'.format(self.__chassi, self.__manualAutomatico, self.__arCondicionado, self.__vidrosTravas, self.__codDept)
    
class VeiculoDAO():

    __sqlSelectAll = None
    __sqlSelectNewChassi = None
    __sqlInsert = None
    __columns = None
    __sqlDelete = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from veiculo"
        self.__sqlInsert = "insert into veiculo values('{}', {}, {}, {}, {})" 
        self.__sqlDelete = "delete from veiculo"
        self.__columns = ["chassi", "manual_automatico", "ar_condicionado", "vidro_travas", "cod_dept"]
        
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
        cursor.execute(self.__sqlInsert.format(veiculo.getChassi(), veiculo.getManualAutomatico(), veiculo.getVidroTravas(),
            veiculo.getArCondicionado(), veiculo.getCodDept()))
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
            if campo != campos[-1]:
                string = string + " " + campo + " = " + dado + ","
            else:
                string = string + " " + campo + " = " + dado

        # Se não há condicional:
        if string == "":
            cursor.execute(self.__sqlDelete) 
        
        cursor.execute(self.__sqlDelete + " " + "where" + string) 
# Para esta classe precisaremos gerar um chassi:
# https://geradorbrasileiro.com/chassi
from Model import *
from Data.Padrao import *

class Veiculo():

    __chassi = None
    __valorProducao = None
    __dataProducao = None
    __codDept = None
    __estagio = None

    def __init__(self):
        self.__chassi = ""
        self.__valorProducao = 0
        self.__dataProducao = "0001-01-01"
        self.__codDept = -1
        self.__estagio = ""

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
    
    def dataProducao(self, dataProducao):
        self.__dataProducao = dataProducao
        return self
    
    def getDataProducao(self):
        return self.__dataProducao
    
    def codDept(self ,codDept):
        self.__codDept = codDept
        return self
    
    def getCodDept(self):
        return self.__codDept
    
    def estagio(self, estagio):
        self.__estagio = estagio
        return self
    
    def getEstagio(self):
        return self.__estagio
            
    def fromTupla(self, tupla):
        self.__chassi = tupla[0]
        self.__valorProducao = tupla[1]
        self.__dataProducao = tupla[2]
        self.__codDept = tupla[3]
        self.__estagio = tupla[4]
        return self
    # Obs.: essa função também serve para listas(para qualquer estrutura indexada no geral)!

    def __repr__(self):
        return u'{}:{}:{}:{}:{}'.format(self.__chassi, self.__valorProducao, self.__dataProducao, self.__codDept, self.__estagio)
    
class VeiculoDAO(PadraoDAO):

    __sqlSelectAll = None
    __sqlInsert = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from veiculo"
        self.__sqlInsert = "insert into veiculo values('{}', {},  '{}', {}, '{}')"
        super().__init__("delete from veiculo", "update veiculo set", ["chassi", "valor_producao", "data_producao", "cod_dept", "estagio"])
        
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
        cursor.execute(self.__sqlInsert.format(veiculo.getChassi(), veiculo.getValorProducao(), 
            veiculo.getDataProducao(), veiculo.getCodDept(), veiculo.getEstagio()))
        con.commit()
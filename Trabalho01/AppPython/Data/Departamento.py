from Model import *

class Departamento():

    __codDept = None
    __tipo = None

    def __init__(self, codDept, tipo):
        self.__codDept = -1
        self.__tipo = ""

    def codDept(self ,codDept):
        self.__codDept = codDept
        return self
    
    def getCodDept(self):
        return self.__codDept
    
    def tipo(self ,tipo):
        self.__tipo = tipo
        return self

    def getTipo(self):
        return self.__tipo
    
    def fromTupla(self, tupla):
        self.__codDept = tupla[0]
        self.__tipo = tupla[1]
        return self
    
    def __repr__(self):
        return u'{}:{}'.format(self.__codDept, self.__tipo)
    
class DepartamentoDAO():

    __sqlSelectAll = None
    __sqlSelectNewCodDept = None
    __sqlInsert = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from departamento"
        self.__sqlSelectNewCodDept = "select cast(max(cod_dept) as int) + 1 from departamento"
        self.__sqlInsert = "insert into departamento departamento values({}, '{}')"

    # Retorna uma lista com um objeto de cada departamento do banco de dados:
    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        departamentos = []
        for line in result:
            departamentos.append(Departamento().fromTupla(line))
        return departamentos
    
    def selectNewCodDept(self) -> int:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectNewCodDept)
        result = cursor.fetchone()
        return result[0]
    
    def insertDepartamento(self, departamento):
        codDept = self.selectNewCodDept()
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(codDept, departamento.getTipo()))
        con.commit()
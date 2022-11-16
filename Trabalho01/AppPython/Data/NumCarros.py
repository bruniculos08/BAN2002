from Model import *

class NumCarros():

    __codDept = None
    __numOfCarros = None

    def __init__(self):
        self.__codDept = -1
        self.__numOfCarros = -1

    def codDept(self, codDept):
        self.__codDept = codDept
        return self
    
    def getCodDept(self):
        return self.__codDept
    
    def numOfCarros(self, numOfCarros):
        self.__numOfCarros = numOfCarros
        return self
    
    def getNumOfCarros(self):
        return self.__numOfCarros
    
    def fromTupla(self, tupla):
        self.__codDept = tupla[0]
        self.__numOfCarros = tupla[1]
        return self
    
    def __repr__(self):
        return u'{}:{}'.format(self.__codDept, self.__numOfCarros)

class NumCarrosDAO():

    __sqlSelectAll = None
    __sqlSelectDept = None
    __sqlSelectMore = None
    __sqlSelectLess = None
    __columns = None

    def __init__(self):
        self.__sqlSelectAll = "select * from NumCarros"
        self.__sqlSelectDept = "select NumOfCarros from NumCarros where"
        self.__sqlSelectMore = "select * from NumCarros where NumOfCarros >"
        self.__sqlSelectLess = "select * from NumCarros where NumOfCarros <"
        self.__columns = ["cod_dept, numOfCarros"]

    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        nums = []
        for line in result:
            nums.append(NumCarros().fromTupla(line))
        return nums
    
    def selectDept(self, cod_dept) -> int:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectDept + f" cod_dept = {cod_dept}")
        result = cursor.fetchone()
        return result[0]
    
    def selectMore(self, numOfCarros):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectMore + f" {numOfCarros}")
        result = cursor.fetchall()
        nums = []
        for line in result:
            nums.append(NumCarros().fromTupla(line))
        return nums
    
    def selectLess(self, numOfCarros):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectLess + f" {numOfCarros}")
        result = cursor.fetchall()
        nums = []
        for line in result:
            nums.append(NumCarros().fromTupla(line))
        return nums
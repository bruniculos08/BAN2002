from Model import *

class NumPedidos():

    __codDept = None
    __numOfPedidos = None

    def __init__(self):
        self.__codDept = -1
        self.__numOfPedidos = -1

    def codDept(self, codDept):
        self.__codDept = codDept
        return self
    
    def getCodDept(self):
        return self.__codDept

    def numOfPedidos(self, numOfPedidos):
        self.__numOfPedidos = numOfPedidos
        return self
    
    def getNumOfPedidos(self):
        return self.__numOfPedidos
    
    def fromTupla(self, tupla):
        self.__codDept = tupla[0]
        self.__numOfPedidos = tupla[1]
        return self
    
    def __repr__(self):
        return u'{}:{}'.format(self.__codDept, self.__numOfPedidos)

class NumPedidosDAO():

    __sqlSelectAll = None
    __sqlSelectDept = None
    __sqlSelectMore = None
    __sqlSelectLess = None
    __columns = None

    def __init__(self):
        self.__sqlSelectAll = "select * from NumPedidos"
        self.__sqlSelectDept = "select NumOfPedidos from NumPedidos where"
        self.__sqlSelectMore = "select * from NumPedidos where NumOfPedidos >"
        self.__sqlSelectLess = "select * from NumPedidos where NumOfPedidos <"
        self.__columns = ["cod_dept", "NumOfPedidos"]

    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        nums = []
        for line in result:
            nums.append(NumPedidos().fromTupla(line))
        return nums
    
    def selectDept(self, cod_dept) -> int:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectDept + f" cod_dept = {cod_dept}")
        result = cursor.fetchone()
        return result[0]
        
    def selectMore(self, numOfPedidos):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectMore + f" {numOfPedidos}")
        result = cursor.fetchall()
        nums = []
        for line in result:
            nums.append(NumPedidos().fromTupla(line))
        return nums
    
    def selectLess(self, numOfPedidos):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectLess + f" {numOfPedidos}")
        result = cursor.fetchall()
        nums = []
        for line in result:
            nums.append(NumPedidos().fromTupla(line))
        return nums
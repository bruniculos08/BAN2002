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
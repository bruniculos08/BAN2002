from Model import *

class Fornecedor():

    __cnpj = None
    __nome = None

    def __init__(self):
        self.__cnpj = ""
        self.__nome = ""

    def cnpj(self, cnpj):
        self.__cnpj = cnpj
        return self
    
    def getCnpj(self):
        return self.__cnpj
    
    def nome(self, nome):
        self.__nome = nome
        return self

    def getNome(self):
        return self.__nome
    
    def fromTupla(self, tupla):
        self.__cnpj = tupla[0]
        self.__nome = tupla[1]
        return self
    
    def __repr__(self):
        return u'{}:{}'.format(self.__cnpj, self.__nome)
    
class FornecedorDAO():

    __sqlSelectAll = None
    __sqlSelectNewCodDept = None
    __sqlInsert = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from fornecedor"
        self.__sqlInsert = "insert into fornecedor values('{}', '{}')"

    # Retorna uma lista com um objeto de cada departamento do banco de dados:
    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        fornecedores = []
        for line in result:
            fornecedores.append(Fornecedor().fromTupla(line))
        return fornecedores
    
    def insertFornecedor(self, fornecedor):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(fornecedor.getCnpj(), fornecedor.getNome()))
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
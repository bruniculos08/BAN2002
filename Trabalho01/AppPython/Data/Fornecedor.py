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
    __sqlInsert = None
    __sqlDelete = None
    __sqlUpdate = None
    __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from fornecedor"
        self.__sqlInsert = "insert into fornecedor values('{}', '{}')"
        self.__sqlDelete = "delete from fornecedor"
        self.__sqlUpdate = "update fornecedor set"
        self.__columns = ["cnpj", "nome"]

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
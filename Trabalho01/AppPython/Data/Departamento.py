from Model import *

class Departamento():

    __codDept = None
    __tipo = None

    def __init__(self):
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
    __sqlDelete = None
    __sqlUpdate = None
    __columns = None
    __sqlSelectCurrCodDept = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from departamento"
        self.__sqlSelectNewCodDept = "select nextval('dept_cod')"
        self.__sqlInsert = "insert into departamento values({}, '{}')"
        self.__sqlDelete = "delete from departamento"
        self.__sqlUpdate = "update departamento set"
        self.__sqlSelectCurrCodDept = "select currval('dept_cod')"
        self.__columns = ["cod_dept", "tipo"]

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
    
    def __selectNewCodDept(self) -> int:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectNewCodDept)
        result = cursor.fetchone()
        return result[0]
    
    def selectCurrCodDept(self):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectCurrCodDept)
        result = cursor.fetchone()
        return result[0]
    
    def insertDepartamento(self, departamento):
        codDept = self.__selectNewCodDept()
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(codDept, departamento.getTipo()))
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
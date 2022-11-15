from Model import *

class ComponenteNecessario():

    __nome = None
    __codDept = None

    def __init__(self):
        self.__nome = ""
        self.__codDept = -1

    def nome(self, nome):
        self.__nome = nome
        return self
    
    def getNome(self):
        return self.__nome
    
    def codDept(self ,codDept):
        self.__codDept = codDept
        return self
    
    def getCodDept(self):
        return self.__codDept
    
    def fromTupla(self, tupla):
        self.__nome = tupla[0]
        self.__codDept = tupla[1]
        return self
    
    def __repr__(self):
        return u'{}:{}'.format(self.__nome, self.__codDept)
    
class ComponenteNecessarioDAO():

    __sqlSelectAll = None
    __sqlInsert = None
    __sqlDelete = None
    __sqlUpdate = None
    __columns = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from componente_necessario"
        self.__sqlInsert = "insert into componente_necessario values('{}', {})"
        self.__sqlDelete = "delete from componente_necessario"
        self.__sqlUpdate = "update componente_necessario set"
        self.__columns = ["cod_dept", "nome_componente", "quantidade"]

    # Retorna uma lista com um objeto de cada componente_necessario do banco de dados:
    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        componentesNecessarios = []
        for line in result:
            componentesNecessarios.append(ComponenteNecessario().fromTupla(line))
        return componentesNecessarios
    
    def insertComponenteNecessario(self, componenteNecessario):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(componenteNecessario.getNome(), componenteNecessario.getCodDept()))
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
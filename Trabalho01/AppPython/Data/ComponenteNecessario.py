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
    
    def __init__(self):
        self.__sqlSelectAll = "select * from componente_necessario"
        self.__sqlInsert = "insert into componente_necessario values('{}', {})"

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
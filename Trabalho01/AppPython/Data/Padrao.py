from Model import *
from Data.Padrao import *

# Para herdar métodos delete e update:
class PadraoDAO():

    __sqlDelete = None
    __sqlUpdate = None
    __columns = None

    def __init__(self, sqlDelete, sqlUpdate, campos):
        self.__sqlDelete = sqlDelete
        self.__sqlUpdate = sqlUpdate
        self.__columns = campos

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
                string = string + " " + "and" + " " + campo + " = " + str(dado)
            else:
                string = string + " " + campo + " = " + str(dado)

        # Se não há condicional:
        if string == "":
            cursor.execute(self.__sqlDelete) 
        else:
            cursor.execute(self.__sqlDelete + " " + "where" + string)

        con.commit()

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
                stringSet = stringSet + ","  + " " + campo + " = " + str(dado)
            else:
                stringSet = stringSet + " " + campo + " = " + str(dado)

        # Montando stringWhere:
        for campo, dado in zip(campos, dadosWhere):
            if dado == '' or dado == '\'\'':
                continue
            if len(stringWhere) > 0:
                stringWhere = stringWhere + " " + "and" + " " + campo + " = " + str(dado)
            else:
                stringWhere = stringWhere + " " + campo + " = " + str(dado)

        # Se não há condicional:
        if stringWhere == "":
            cursor.execute(self.__sqlUpdate + " " + stringSet) 
        else:
            cursor.execute(self.__sqlUpdate + stringSet + " " + "where" + stringWhere)

        con.commit()
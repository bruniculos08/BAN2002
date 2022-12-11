from pymongo import MongoClient
from Data.Padrao import *

class ComponenteNecessarioDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["id_dept", "nome", "quantidade"]
        super(ComponenteNecessarioDAO, self).__init__(self.__mongoDBFields, "Personalização", "componente_necessario")
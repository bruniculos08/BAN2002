from pymongo import MongoClient
from Data.Padrao import *

class DepartamentoDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["_id", "tipo"]
        super(DepartamentoDAO, self).__init__(self.__mongoDBFields, "Personalização", "departamento")
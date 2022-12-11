from pymongo import MongoClient
from Data.Padrao import *

class ForneceDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["_id", "nome_componente", "cnpj"]
        super(ForneceDAO, self).__init__(self.__mongoDBFields, "Personalização", "fornece")
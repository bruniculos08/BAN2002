from pymongo import MongoClient
from Data.Padrao import *

class ComponenteDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["_id", "nome", "tipo", "valor_compra", "quantidade_min", "quantidade", "cnpj_principal"]
        super(ComponenteDAO, self).__init__(self.__mongoDBFields, "Personalização", "componente")
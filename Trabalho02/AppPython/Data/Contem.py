from pymongo import MongoClient
from Data.Padrao import *

class ContemDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["_id", "nome_componente", "id_pedido", "quantidade"]
        super(ContemDAO, self).__init__(self.__mongoDBFields, "Personalização", "contem")
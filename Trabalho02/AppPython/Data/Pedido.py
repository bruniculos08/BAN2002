from pymongo import MongoClient
from Data.Padrao import *

class PedidoDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["_id", "data_criacao", "cnpj", "id_dept"]
        super(PedidoDAO, self).__init__(self.__mongoDBFields, "Personalização", "pedido")
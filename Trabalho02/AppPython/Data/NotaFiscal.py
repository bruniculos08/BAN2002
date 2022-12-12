from pymongo import MongoClient
from Data.Padrao import *

class NotaFiscalDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["_id", "cod_nota", "id_pedido"]
        super(NotaFiscalDAO, self).__init__(self.__mongoDBFields, "Personalização", "nota_fiscal")
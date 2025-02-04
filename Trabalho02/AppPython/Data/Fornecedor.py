from pymongo import MongoClient
from Data.Padrao import *

class FornecedorDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["_id", "cnpj", "nome"]
        super(FornecedorDAO, self).__init__(self.__mongoDBFields, "Personalização", "fornecedor")
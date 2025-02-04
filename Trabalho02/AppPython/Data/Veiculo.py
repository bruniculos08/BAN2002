from pymongo import MongoClient
from Data.Padrao import *

class VeiculoDAO(PadraoDAO):

    __mongoDBFields = None

    def __init__(self):
        self.__mongoDBFields = ["_id", "chassi", "valor_producao", "data_producao", "id_dept", "estagio"]
        super(VeiculoDAO, self).__init__(self.__mongoDBFields, "Personalização", "veiculo")
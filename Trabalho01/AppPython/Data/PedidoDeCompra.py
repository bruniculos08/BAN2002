from Model import *

class PedidoDeCompra():

    __id = None
    __codNota = None
    __cnpj = None
    __valor = None

    def __init__(self):
        self.__id = -1
        self.__cod_nota = ""
        self.__cnpj = ""
        self.__valor = 0

    def id(self, id):
        self.__id = id
        return self
    
    def getId(self):
        return self.__id

    def codNota(self, codNota):
        self.__codNota = codNota
        return self
    
    def getCodNota(self):
        return self.__codNota

    def cnpj(self, cnpj):
        self.__cnpj = cnpj
        return self

    def get(self):    


# create table pedido_de_compra(
#     id integer not null,
#     cod_nota integer not null,
#     cnpj character varying(14) not null,
#     valor numeric not null,
#     primary key (id),
#     FOREIGN key(cnpj) references fornecedor (cnpj)
# );
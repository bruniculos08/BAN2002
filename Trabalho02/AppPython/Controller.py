# Camada de interface com usuário; 
# Camada de negócios, com a lógica da aplicação (na qual se encontra); e
# Camada de dados, com funcionalidade de armazenamento e recuperação.

from tkinter import *
from Model import *
from Data.Departamento import *
from Data.Veiculo import *
from Data.Fornecedor import *
from Data.Pedido import *
from Data.Componente import *
from Data.ComponenteNecessario import *
from Data.Contem import *
from Data.NotaFiscal import *
from Data.Fornece import *
from Data.NumPedidos import *
from Data.NumCarros import *
from Data.Despesa import *
from Data.Receita import *

class Controller():

    def __init__(self):
        pass

    def view(self, view):
        pass

    def printSucess(self):
        pass

    def printError(self):
        pass

    def printQuery(self, query, campos):
        pass

    def clearAndGetData(self):
        pass
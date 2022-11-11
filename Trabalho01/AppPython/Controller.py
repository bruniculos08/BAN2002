# Camada de interface com usuário; 
# Camada de negócios, com a lógica da aplicação (na qual se encontra); e
# Camada de dados, com funcionalidade de armazenamento e recuperação.

from tkinter import *
from Data.Departamento import *
from Data.Veiculo import *

class Controller():

    __view = None
    __departamentoDAO = None
    __veiculoDAO = None

    def __init__(self):
        self.__view = None
        self.__departamentoDAO = DepartamentoDAO()
        self.__veiculoDAO = VeiculoDAO()

    def view(self, view):
        self.__view = view
        return self

    def setInserirDepartamento(self):
        self.__view    

    def inserirDepartamento(self):
        # Nesta função devemos setar na view a quantidade de campos esperar pela entrada para receber os dados.
        dados = self.__view.getCamposDeInsercao()
        self.__view.setCamposDeInsercao(0, self)
        pass
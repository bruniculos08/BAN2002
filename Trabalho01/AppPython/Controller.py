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

    # Esta função criar os campos de inserção de acordo com a quantidade de atributos da entidade "Departamento":
    def setInserirDepartamento(self):
        campos = ["Código de departamento:", "Tipo do departamento:"]
        self.__view.criarCamposDeInsercao(2, campos)
        self.__view.criarBotaoDepartamento()

    # Esta função pega os dados do campo de inserção e insere na tabela de departamento do banco de dados:
    def inserirDepartamento(self):
        dados = self.__view.getCamposDeInsercao()
        self.__view.criarCamposDeInsercao(0)
        newDepartamento = Departamento().fromTupla(dados)
        self.__departamentoDAO.insertDepartamento(newDepartamento)

    # Esta função criar os campos de inserção de acordo com a quantidade de atributos da entidade "Veiculo":
    def setInserirVeiculo(self):
        campos = ["Chassi:", "Manual automatico(boolean):", "Ar condicionado(boolean):", "Vidro com travas(boolean):", "Código de departamento:"]
        self.__view.criarCamposDeInsercao(5, campos)
        self.__view.criarBotaoVeiculo()

    # Esta função pega os dados do campo de inserção e insere na tabela de veiculo do banco de dados:
    def inserirVeiculo(self):
        dados = self.__view.getCamposDeInsercao()
        self.__view.criarCamposDeInsercao(0)
        newVeiculo = Veiculo().fromTupla(dados)
        self.__veiculoDAO.insertVeiculo(newVeiculo)


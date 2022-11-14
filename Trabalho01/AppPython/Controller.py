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

class Controller():

    __view = None
    __departamentoDAO = None
    __veiculoDAO = None
    __fornecedorDAO = None
    __pedidoDAO = None
    __componenteDAO = None
    __componenteNecessarioDAO = None
    __contemDAO = None
    __notaFiscalDAO = None
    __forneceDAO = None
    __model = None
    __noticesSizes = None
    

    def __init__(self):
        self.__view = None
        self.__departamentoDAO = DepartamentoDAO()
        self.__veiculoDAO = VeiculoDAO()
        self.__fornecedorDAO = FornecedorDAO()
        self.__pedidoDAO = PedidoDAO()
        self.__componenteDAO = ComponenteDAO()
        self.__componenteNecessarioDAO = ComponenteNecessarioDAO()
        self.__contemDAO = ContemDAO()
        self.__notaFiscalDAO = NotaFiscalDAO()
        self.__forneceDAO = ForneceDAO()
        self.__noticesSizes = 0
        

    def view(self, view):
        self.__view = view
        return self
    
    def printSucess(self):
        self.__model = Connection()
        notices = self.__model.notices()
        if(len(notices) > self.__noticesSizes):
            self.__view.setCampoDeExibicao(notices[-1])
        else:
            self.__view.setCampoDeExibicao("Operação realizada com sucesso!")
        self.__noticesSizes = len(notices)

    def printError(self):
        self.__model = Connection()
        notices = self.__model.notices()
        if(len(notices) > self.__noticesSizes):
            self.__view.setCampoDeExibicao(notices[-1])
        else:
            self.__view.setCampoDeExibicao("Operação não realizada!")
            self.__model.rollback()
            self.__model.commit()
        self.__noticesSizes = len(notices)

    def printQuery(self, query, campos):
        # Limpando o campo de texto:
        self.__view.clearCampoDeExibicao()

        # Imprimindo o nome dos atributos no campo de texto:
        self.__view.addCampoDeExibicao("Atributos: ")
        for word in campos[0:-1]:
            self.__view.addCampoDeExibicao(word + ', ')
        self.__view.addCampoDeExibicao(campos[-1] + '.\n\n')

        # Imprimindo as linhas resultantes da query:
        for item in query:
            row = list(map(str, item.__repr__().split(":")))
            for word in row[0:-1]:
                self.__view.addCampoDeExibicao(word + '\t|\t')
            self.__view.addCampoDeExibicao(row[-1] + '\n')

    def clearAndGetData(self):
        dados = self.__view.getCamposDeInsercao()
        self.__view.criarCamposDeInsercao(0)
        return dados
        
    # Esta função criar os campos de inserção de acordo com a quantidade de atributos da entidade "Departamento":
    def setInserirDepartamento(self):
        # Como o codDept é gerado automaticamente (por sequência, basta inserir o tipo):
        campos = ["Tipo do departamento:"]
        self.__view.criarCamposDeInsercao(1, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirDepartamento())
        self.__view.criarBotao(botao)

    # Esta função pega os dados do campo de inserção e insere na tabela de departamento do banco de dados:
    def inserirDepartamento(self):
        dados = [-1] + self.clearAndGetData()
        newDepartamento = Departamento().fromTupla(dados)
        try:
            self.__departamentoDAO.insertDepartamento(newDepartamento)
            text = f"Departamento adicionando com codDept = {self.__departamentoDAO.selectCurrCodDept()}!"
            self.__view.setCampoDeExibicao(text)
        except:
            self.printError()

    # Esta função criar os campos de inserção de acordo com a quantidade de atributos da entidade "Veiculo":
    def setInserirVeiculo(self):
        campos = ["Chassi:", "Manual automatico(boolean):", "Ar condicionado(boolean):", "Vidro com travas(boolean):", "Código de departamento:"]
        self.__view.criarCamposDeInsercao(5, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirVeiculo())
        self.__view.criarBotao(botao)

    # Esta função pega os dados do campo de inserção e insere na tabela de veiculo do banco de dados:
    def inserirVeiculo(self):
        dados = self.clearAndGetData()
        newVeiculo = Veiculo().fromTupla(dados)
        try:
            self.__veiculoDAO.insertVeiculo(newVeiculo)
            self.printSucess()
        except:
            self.printError()
            
    def setInserirFornecedor(self):
        campos = ["CNPJ:", "Nome:"]
        self.__view.criarCamposDeInsercao(2, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirFornecedor())
        self.__view.criarBotao(botao)

    def inserirFornecedor(self):
        dados = self.clearAndGetData()
        newFornecedor = Fornecedor().fromTupla(dados)
        try:
            self.__fornecedorDAO.insertFornecedor(newFornecedor)
            self.printSucess()
        except:
            self.printError()
            
    def setInserirPedido(self):
        campos = ["Valor:", "CNPJ:", "Código do Departamento:"]
        self.__view.criarCamposDeInsercao(3, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirPedido())
        self.__view.criarBotao(botao)

    def inserirPedido(self):
        dados = [-1] + self.clearAndGetData()
        newPedido = Pedido().fromTupla(dados)
        try:
            self.__pedidoDAO.insertPedido(newPedido)
            self.printSucess()
        except:
            self.printError()

    def setInserirComponente(self):
        campos = ["Nome:", "Tipo:", "Quantidade Mínima:", "Quantidade:", "CNPJ Principal:"]
        self.__view.criarCamposDeInsercao(5, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirComponente())
        self.__view.criarBotao(botao)

    def inserirComponente(self):
        dados = self.clearAndGetData()
        newComponente = Componente().fromTupla(dados)
        try:
            self.__componenteDAO.insertComponente(newComponente)
            self.printSucess()
        except:
            self.printError()

    def verComponente(self):
        campos = ["Nome", "Tipo", "Quantidade Mínima", "Quantidade", "CNPJ Principal"]
        text = self.__componenteDAO.selectAll()
        self.printQuery(text, campos)
            
    def setInserirComponenteNecessario(self):
        campos = ["Código do Departamento:", "Nome do Componente:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(3, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirComponenteNecessario())
        self.__view.criarBotao(botao)

    def inserirComponenteNecessario(self):
        dados = self.clearAndGetData()
        newComponenteNecessario = ComponenteNecessario().fromTupla(dados)
        try:
            self.__componenteNecessarioDAO.insertComponenteNecessario(newComponenteNecessario)
            self.printSucess()
        except:
            self.printError()

    def verComponenteNecessario(self):
        text = self.__componenteNecessarioDAO.selectAll()
        self.printQuery(text)
            
    def setInserirContem(self):
        campos = ["Nome do Componente:", "Id do pedido:"]
        self.__view.criarCamposDeInsercao(2, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirContem())
        self.__view.criarBotao(botao)

    def inserirContem(self):
        dados = self.clearAndGetData()
        newContem = Contem().fromTupla(dados)
        try:
            self.__contemDAO.insertContem(newContem)
            self.printSucess()
        except:
            self.printError()

    def verContem(self):
        text = self.__contemDAO.selectAll()
        self.printQuery(text)
            
    def setInserirNotaFiscal(self):
        campos = ["Código da nota:", "Id do pedido:"]
        self.__view.criarCamposDeInsercao(2, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirNotaFiscal())
        self.__view.criarBotao(botao)

    def inserirNotaFiscal(self):
        dados = self.clearAndGetData()
        newNotaFiscal = NotaFiscal().fromTupla(dados)
        try:
            self.__notaFiscalDAO.insertNotaFiscal(newNotaFiscal)
            self.printSucess()
        except:
            self.printError()

    def verNotasFiscais(self):
        text = self.__notaFiscalDAO.selectAll()
        self.printQuery(text)
            
    def setInserirFornece(self):
        campos = ["Nome do Componente:", "CNPJ:"]
        self.__view.criarCamposDeInsercao(2, campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirFornece())
        self.__view.criarBotao(botao)

    def inserirFornece(self):
        dados = self.clearAndGetData()
        newFornece = Fornece().fromTupla(dados)
        try:
            self.__forneceDAO.insertFornece(newFornece)
            self.printSucess()
        except:
            self.printError()
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
    __numPedidosDAO = None
    __numCarrosDAO = None
    __despesaDAO = None
    __receitaDAO = None
    __model = None
    __noticesSize = None
    

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
        self.__numPedidosDAO = NumPedidosDAO()
        self.__numCarrosDAO = NumCarrosDAO()
        self.__despesaDAO = DespesaDAO()
        self.__receitaDAO = ReceitaDAO()
        self.__noticesSize = 0

    def view(self, view):
        self.__view = view
        return self
    
    def printSucess(self):
        self.__model = Connection()
        notices = self.__model.notices()
        if(len(notices) > self.__noticesSize):
            self.__view.setCampoDeExibicao("Operação realizada com sucesso!\n")
            for i in range(self.__noticesSize-1, len(notices)-1):
                self.__view.addCampoDeExibicao(f"Notificação {i+2 - self.__noticesSize}: {notices[i+1][9:]}")
        else:
            self.__view.setCampoDeExibicao("Operação realizada com sucesso!\n")
        self.__noticesSize = len(notices)

    def printError(self):
        self.__model = Connection()
        notices = self.__model.notices()
        if self.__model.error() != None: 
            self.__view.setCampoDeExibicao("Operação não realizada pois parâmetros inseridos são inválidos.\n\n" 
            + "Erro no banco de dados:\n" + self.__model.error()
            )
        else:
            self.__view.setCampoDeExibicao("Operação não realizada pois parâmetros inseridos são inválidos.\n\n")
        self.__model.rollback()
        self.__model.commit()
        self.__noticesSize = len(notices)

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
        self.__view.criarCamposDeInsercao()
        return dados
    
    # Esta função criar os campos de inserção de acordo com a quantidade de atributos da entidade "Departamento" para...
    # ... a operação de 'insert':
    def setInserirDepartamento(self):
        # Como o codDept é gerado automaticamente (por sequência, basta inserir o tipo):
        campos = ["Tipo do departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirDepartamento())
        self.__view.criarBotoes(botao)

    # Esta função pega os dados do campo de inserção e insere na tabela de departamento do banco de dados:
    def inserirDepartamento(self):
        try:
            dados = [-1] + self.clearAndGetData()
            newDepartamento = Departamento().fromTupla(dados)
            self.__departamentoDAO.insertDepartamento(newDepartamento)
            text = f"Departamento adicionando com codDept = {self.__departamentoDAO.selectCurrCodDept()}!"
            self.__view.setCampoDeExibicao(text)
        except:
            self.printError()

    # Esta função criar os campos de inserção de acordo com a quantidade de atributos da entidade "Departamento" para...
    # ... a operação de 'delete':
    def setDeletarDepartamento(self):
        campos = ["Código do departamento:", "Tipo do departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarDepartamento())
        self.__view.criarBotoes(botao)
            
    # Esta função pega os dados do campo de inserção e deleta na tabela de departamento do banco de dados os itens cujos...
    # ... atributos são iguais aos colocados nos respectivos campos:
    def deletarDepartamento(self):
        try:
            dados = self.clearAndGetData()
            if dados[0] != '': dados[0] = int(dados[0])
            dados[1] = '\'' + dados[1] + '\''
            self.__departamentoDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()
        
    def setPrimarioAtualizarDepartamento(self):
        campos = ["Novo tipo do departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarDepartamento())
        self.__view.criarBotoes(botao)

    def setSecundarioAtualizarDepartamento(self):
        try:
            dadosSet = [''] + self.clearAndGetData()
            dadosSet[1] = '\'' + dadosSet[1] + '\''
            campos = ["Código do departamento:", "Antigo tipo do departamento:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarDepartamento(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()
        
    def atualizarDepartamento(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            if dadosWhere[0] != '': dadosWhere[0] = int(dadosWhere[0])
            dadosWhere[1] = '\'' + dadosWhere[1] + '\''
            self.__departamentoDAO.update(dadosSet, dadosWhere)
            self.printSucess()
        except:
            self.printError()

    # Esta função executa o comando 'select all' sobre a tabela 'departamento':
    def verDepartamento(self):
        campos = ["Código do departamento", "Tipo do departamento"]
        text = self.__departamentoDAO.selectAll()
        self.printQuery(text, campos)

    def setInserirVeiculo(self):
        campos = ["Chassi:", "Valor de produção:", "Código de departamento:"] # quando inserido estágio = "início"
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirVeiculo())
        self.__view.criarBotoes(botao)

    def inserirVeiculo(self):
        try:
            dados = self.clearAndGetData()
            dados = [dados[0]] + [dados[1]] + ["0001-01-01"] + [dados[2]] + ['']
            dados[1] = float(dados[1])
            dados[3] = int(dados[3])
            newVeiculo = Veiculo().fromTupla(dados)
            self.__veiculoDAO.insertVeiculo(newVeiculo)
            self.printSucess()
        except:
            self.printError()

    def setDeletarVeiculo(self):
        campos = ["Chassi:", "Valor de produção:", "Data de produção(YYYY-MM-DD):", "Código de departamento:", "Estágio:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarVeiculo())
        self.__view.criarBotoes(botao)
        
    def deletarVeiculo(self):
        try:
            dados = self.clearAndGetData()
            dados[0] = '\'' + dados[0] + '\''
            if(dados[1] != ''): dados[1] = float(dados[1])
            dados[2] = '\'' + dados[2] + '\''
            if(dados[3] != ''): dados[3] = int(dados[3])
            dados[4] = '\'' + dados[4] + '\''
            self.__veiculoDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarVeiculo(self):
        campos = ["Novo chassi:", "Novo valor de produção:", "Novo código de departamento:", "Novo Estágio:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarVeiculo())
        self.__view.criarBotoes(botao)

    def setSecundarioAtualizarVeiculo(self):
        try:
            dadosSet = self.clearAndGetData()
            dadosSet[0] = '\'' + dadosSet[0] + '\''
            if(dadosSet[1] != ''): dadosSet[1] = float(dadosSet[1])
            if(dadosSet[2] != ''): dadosSet[2] = int(dadosSet[2])
            dadosSet[3] = '\'' + dadosSet[3] + '\''
            dadosSet = [dadosSet[0]] + [dadosSet[1]] + [''] + [dadosSet[2]] + [dadosSet[3]]
            campos = ["Antigo chassi:", "Antigo valor de produção:", "Antiga data de produção(YYYY-MM-DD):", "Antigo código de departamento:", "Antigo estágio:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarVeiculo(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()
        
    def atualizarVeiculo(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            dadosWhere[0] = '\'' + dadosWhere[0] + '\''
            if(dadosWhere[1] != ''): dadosWhere[1] = float(dadosWhere[1])
            dadosWhere[2] = '\'' + dadosWhere[2] + '\''
            if(dadosWhere[3] != ''): dadosWhere[3] = int(dadosWhere[3])
            dadosWhere[4] = '\'' + dadosWhere[4] + '\''
            self.__veiculoDAO.update(dadosSet, dadosWhere)
            self.printSucess()
        except:
            self.printError()

    def verVeiculo(self):
        campos = ["Chassi", "Valor de produção", "Data de produção(YYYY-MM-DD)", "Código de departamento", "Estágio"]
        text = self.__veiculoDAO.selectAll()
        self.printQuery(text, campos)
            
    def setInserirFornecedor(self):
        campos = ["CNPJ:", "Nome:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirFornecedor())
        self.__view.criarBotoes(botao)

    def inserirFornecedor(self):
        try:
            dados = self.clearAndGetData()
            newFornecedor = Fornecedor().fromTupla(dados)
            self.__fornecedorDAO.insertFornecedor(newFornecedor)
            self.printSucess()
        except:
            self.printError()

    def setDeletarFornecedor(self):
        campos = ["CNPJ:", "Nome:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarFornecedor())
        self.__view.criarBotoes(botao)

    def deletarFornecedor(self):
        try:
            dados = self.clearAndGetData()
            dados[0] = '\'' + dados[0] + '\''
            dados[1] = '\'' + dados[1] + '\''
            self.__fornecedorDAO.delete(dados)
            self.printSucess()
        except:
            self.printError() 
    
    def setPrimarioAtualizarFornecedor(self):
        campos = ["Novo CNPJ:", "Novo nome:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarFornecedor())
        self.__view.criarBotoes(botao)
        
    def setSecundarioAtualizarFornecedor(self):
        try:
            dadosSet = self.clearAndGetData()
            dadosSet[0] = '\'' + dadosSet[0] + '\''
            dadosSet[1] = '\'' + dadosSet[1] + '\''
            campos = ["Antigo CNPJ:", "Antigo nome:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarFornecedor(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()

    def atualizarFornecedor(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            dadosWhere[0] = '\'' + dadosWhere[0] + '\''
            dadosWhere[1] = '\'' + dadosWhere[1] + '\''
            self.__fornecedorDAO.update(dadosSet, dadosWhere)
            self.printSucess() 
        except:
            self.printError()

    def verFornecedor(self):
        campos = ["CNPJ", "Nome"]
        text = self.__fornecedorDAO.selectAll()
        self.printQuery(text, campos)
            
    def setInserirPedido(self):
        campos = ["CNPJ:", "Código do Departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirPedido())
        self.__view.criarBotoes(botao)

    def inserirPedido(self):
        try:
            dados = [-1] + ["0001-01-01"] + self.clearAndGetData()
            dados[3] = int(dados[3])
            newPedido = Pedido().fromTupla(dados)
            self.__pedidoDAO.insertPedido(newPedido)
            self.printSucess()
        except:
            self.printError()

    def setDeletarPedido(self):    
        campos = ["Id do pedido:", "Data de criação(YYYY-MM-DD):", "CNPJ:", "Código do Departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarPedido())
        self.__view.criarBotoes(botao)

    def deletarPedido(self):
        try:
            dados = self.clearAndGetData()
            if dados[0] != '': dados[0] = int(dados[0])
            dados[1] = '\'' + dados[1] + '\''
            dados[2] = '\'' + dados[2] + '\''
            if(dados[3] != ''): dados[3] = int(dados[3])
            self.__pedidoDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarPedido(self):
        campos = ["Novo CNPJ:", "Novo código do departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarPedido())
        self.__view.criarBotoes(botao)
        
    def setSecundarioAtualizarPedido(self):
        try:
            dadosSet = [''] + [''] + self.clearAndGetData()
            dadosSet[2] = '\'' + dadosSet[2] + '\''
            if(dadosSet[3] != ''): dadosSet[3] = int(dadosSet[3])
            campos = ["Antigo id do pedido:", "Antiga data de criação(YYYY-MM-DD):", "Antigo CNPJ:", "Antigo código do departamento:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarPedido(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()
            
    def atualizarPedido(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            if dadosWhere[0] != '': dadosWhere[0] = int(dadosWhere[0])
            dadosWhere[1] = '\'' + dadosWhere[1] + '\''
            dadosWhere[2] = '\'' + dadosWhere[2] + '\''
            if(dadosWhere[3] != ''): dadosWhere[3] = int(dadosWhere[3])
            self.__pedidoDAO.update(dadosSet, dadosWhere)
            self.printSucess()
        except:
            self.printError()

    def verPedido(self):
        campos = ["Id do pedido", "Data de criação(YYYY-MM-DD)", "CNPJ", "Código do Departamento"]
        text = self.__pedidoDAO.selectAll()
        self.printQuery(text, campos)

    def setInserirComponente(self):
        campos = ["Nome:", "Tipo:", "Valor de compra:", "Quantidade Mínima:", "CNPJ Principal:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirComponente())
        self.__view.criarBotoes(botao)

    def inserirComponente(self):
        try:
            dados = self.clearAndGetData()
            dados = dados[0:4] + [0] + dados[4:5]
            dados[2] = float(dados[2])
            dados[3] = int(dados[3])
            newComponente = Componente().fromTupla(dados)
            self.__componenteDAO.insertComponente(newComponente)
            self.printSucess()
        except:
            self.printError()

    def setDeletarComponente(self):
        campos = ["Nome:", "Tipo:", "Valor de compra:", "Quantidade Mínima:", "Quantidade:", "CNPJ Principal:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarComponente())
        self.__view.criarBotoes(botao)      
    
    def deletarComponente(self):
        try:
            dados = self.clearAndGetData()
            dados[0] = '\'' + dados[0] + '\''
            dados[1] = '\'' + dados[1] + '\''
            if (dados[2] != ''): dados[2] = int(dados[2])
            if (dados[3] != ''): dados[3] = int(dados[3])
            if (dados[4] != ''): dados[4] = int(dados[4])
            dados[5] = '\'' + dados[5] + '\''
            self.__componenteDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarComponente(self):
        campos = ["Novo nome:", "Novo tipo:", "Novo valor de compra:", "Nova quantidade mínima:", "Novo CNPJ principal:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarComponente())
        self.__view.criarBotoes(botao)

    def setSecundarioAtualizarComponente(self):
        try:
            dadosSet = self.clearAndGetData()
            dadosSet = dadosSet[0:4] + [''] + dadosSet[4:5]
            dadosSet[0] = '\'' + dadosSet[0] + '\''
            dadosSet[1] = '\'' + dadosSet[1] + '\''
            if (dadosSet[2] != ''): dadosSet[2] = int(dadosSet[2])
            if (dadosSet[3] != ''): dadosSet[3] = int(dadosSet[3])
            dadosSet[5] = '\'' + dadosSet[5] + '\''
            campos = ["Antigo nome:", "Antigo tipo:", "Antigo valor de compra:", "Antigo quantidade mínima:", "Antigo quantidade:", "Antigo CNPJ principal:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarComponente(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()
            
    def atualizarComponente(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            dadosWhere[0] = '\'' + dadosWhere[0] + '\''
            dadosWhere[1] = '\'' + dadosWhere[1] + '\''
            if (dadosWhere[2] != ''): dadosWhere[2] = int(dadosWhere[2])
            if (dadosWhere[3] != ''): dadosWhere[3] = int(dadosWhere[3])
            if (dadosWhere[4] != ''): dadosWhere[4] = int(dadosWhere[4])
            dadosWhere[5] = '\'' + dadosWhere[5] + '\''
            self.__componenteDAO.update(dadosSet, dadosWhere)
            self.printSucess()
        except:
            self.printError()

    def verComponente(self):
        campos = ["Nome", "Tipo", "Valor de compra", "Quantidade Mínima", "Quantidade", "CNPJ Principal"]
        text = self.__componenteDAO.selectAll()
        self.printQuery(text, campos)
            
    def setInserirComponenteNecessario(self):
        campos = ["Código do Departamento:", "Nome do Componente:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirComponenteNecessario())
        self.__view.criarBotoes(botao)

    def inserirComponenteNecessario(self):
        try:
            dados = self.clearAndGetData()
            dados[0] = int(dados[0])
            dados[2] = int(dados[2])
            newComponenteNecessario = ComponenteNecessario().fromTupla(dados)
            self.__componenteNecessarioDAO.insertComponenteNecessario(newComponenteNecessario)
            self.printSucess()
        except:
            self.printError()

    def setDeletarComponenteNecessario(self):
        campos = ["Código do departamento:", "Nome do componente:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarComponenteNecessario())
        self.__view.criarBotoes(botao)
    
    def deletarComponenteNecessario(self):
        try:
            dados = self.clearAndGetData()
            if dados[0] != '': dados[0] = int(dados[0])
            dados[1] = '\'' + dados[1] + '\''
            if(dados[2] != ''): dados[2] = int(dados[2])
            self.__componenteNecessarioDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarComponenteNecessario(self):
        campos = ["Novo código do departamento:", "Novo nome do componente:", "Nova quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarComponenteNecessario())
        self.__view.criarBotoes(botao)
        
    def setSecundarioAtualizarComponenteNecessario(self):
        try:
            dadosSet = self.clearAndGetData()
            if dadosSet[0] != '': dadosSet[0] = int(dadosSet[0])
            dadosSet[1] = '\'' + dadosSet[1] + '\''
            if(dadosSet[2] != ''): dadosSet[2] = int(dadosSet[2])
            campos = ["Antigo código do departamento:", "Antigo nome do componente:", "Antiga quantidade:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarComponenteNecessario(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()

    def atualizarComponenteNecessario(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            if dadosWhere[0] != '': dadosWhere[0] = int(dadosWhere[0])
            dadosWhere[1] = '\'' + dadosWhere[1] + '\''
            if(dadosWhere[2] != ''): dadosWhere[2] = int(dadosWhere[2])
            self.__componenteNecessarioDAO.update(dadosSet, dadosWhere)
            self.printSucess()
        except:
            self.printError()

    def verComponenteNecessario(self):
        campos = ["Código do Departamento", "Nome do Componente", "Quantidade"]
        text = self.__componenteNecessarioDAO.selectAll()
        self.printQuery(text, campos)
            
    def setInserirContem(self):
        campos = ["Nome do componente:", "Id do pedido:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirContem())
        self.__view.criarBotoes(botao)

    def inserirContem(self):
        try:
            dados = self.clearAndGetData()
            dados[1] = int(dados[1])
            dados[2] = int(dados[2])
            newContem = Contem().fromTupla(dados)
            self.__contemDAO.insertContem(newContem)
            self.printSucess()
        except:
            self.printError()
    
    def setDeletarContem(self):
        campos = ["Nome do componente:", "Id do pedido:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarContem())
        self.__view.criarBotoes(botao)

    def deletarContem(self):
        try:
            dados = self.clearAndGetData()
            dados[0] = '\'' + dados[0] + '\''
            if(dados[1] != ''): dados[1] = int(dados[1])
            if(dados[2] != ''): dados[2] = int(dados[2])
            self.__contemDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarContem(self):
        campos = ["Novo nome do componente:", "Novo id do pedido:", "Nova quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarContem())
        self.__view.criarBotoes(botao)
        
    def setSecundarioAtualizarContem(self):
        try:
            dadosSet = self.clearAndGetData()
            dadosSet[0] = '\'' + dadosSet[0] + '\''
            if(dadosSet[1] != ''): dadosSet[1] = int(dadosSet[1])
            if(dadosSet[2] != ''): dadosSet[2] = int(dadosSet[2])
            campos = ["Antigo nome do componente:", "Antigo id do pedido:", "Antiga quantidade:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarContem(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()
        
    def atualizarContem(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            dadosWhere[0] = '\'' + dadosWhere[0] + '\''
            if(dadosWhere[1] != ''): dadosWhere[1] = int(dadosWhere[1])
            if(dadosWhere[2] != ''): dadosWhere[2] = int(dadosWhere[2])
            self.__contemDAO.update(dadosSet, dadosWhere)
            self.printSucess()
        except:
            self.printError()

    def verContem(self):
        campos = ["Nome do Componente", "Id do pedido", "Quantidade"]
        text = self.__contemDAO.selectAll()
        self.printQuery(text, campos)
            
    def setInserirNotaFiscal(self):
        campos = ["Código da nota:", "Id do pedido:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirNotaFiscal())
        self.__view.criarBotoes(botao)

    def inserirNotaFiscal(self):
        try:
            dados = self.clearAndGetData()
            dados[1] = int(dados[1])
            newNotaFiscal = NotaFiscal().fromTupla(dados)
            self.__notaFiscalDAO.insertNotaFiscal(newNotaFiscal)
            self.printSucess()
        except:
            self.printError()

    def setDeletarNotaFiscal(self):
        campos = ["Código da nota:", "Id do pedido:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarNotaFiscal())
        self.__view.criarBotoes(botao)
            
    def deletarNotaFiscal(self):
        try:
            dados = self.clearAndGetData()
            dados[0] = '\'' + dados[0] + '\''
            if(dados[1] != ''): dados[1] = int(dados[1])
            self.__notaFiscalDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarNotaFiscal(self):
        campos = ["Novo código da nota:", "Novo id do pedido:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarNotaFiscal())
        self.__view.criarBotoes(botao)

    def setSecundarioAtualizarNotaFiscal(self):
        try:
            dadosSet = self.clearAndGetData()
            dadosSet[0] = '\'' + dadosSet[0] + '\''
            if(dadosSet[1] != ''): dadosSet[1] = int(dadosSet[1])
            campos = ["Antigo código da nota:", "Antigo id do pedido:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarNotaFiscal(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()
            
    def atualizarNotaFiscal(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            dadosWhere[0] = '\'' + dadosWhere[0] + '\''
            if(dadosWhere[1] != ''): dadosWhere[1] = int(dadosWhere[1])
            self.__notaFiscalDAO.update(dadosSet, dadosWhere)
            self.printSucess()
        except:
            self.printError()

    def verNotaFiscal(self):
        campos = ["Código da nota", "Id do pedido"]
        text = self.__notaFiscalDAO.selectAll()
        self.printQuery(text, campos)
            
    def setInserirFornece(self):
        campos = ["Nome do Componente:", "CNPJ:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirFornece())
        self.__view.criarBotoes(botao)

    def inserirFornece(self):
        try:
            dados = self.clearAndGetData()
            newFornece = Fornece().fromTupla(dados)
            self.__forneceDAO.insertFornece(newFornece)
            self.printSucess()
        except:
            self.printError()

    def setDeletarFornece(self):
        campos = ["Nome do Componente:", "CNPJ:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarFornece())
        self.__view.criarBotoes(botao)

    def deletarFornece(self):
        try:
            dados = self.clearAndGetData()
            dados[0] = '\'' + dados[0] + '\''
            dados[1] = '\'' + dados[1] + '\''
            self.__forneceDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarFornece(self):
        campos = ["Novo nome do componente:", "Novo CNPJ:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarFornece())
        self.__view.criarBotoes(botao)
    
    def setSecundarioAtualizarFornece(self):
        try:
            dadosSet = self.clearAndGetData()
            dadosSet[0] = '\'' + dadosSet[0] + '\''
            dadosSet[1] = '\'' + dadosSet[1] + '\''
            campos = ["Antigo nome do componente:", "Antigo CNPJ:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarFornece(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()
            
    def atualizarFornece(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            dadosWhere[0] = '\'' + dadosWhere[0] + '\''
            dadosWhere[1] = '\'' + dadosWhere[1] + '\''
            self.__forneceDAO.update(dadosSet, dadosWhere)
            self.printSucess()
        except:
            self.printError()

    def verFornece(self):
        campos = ["Nome do Componente", "CNPJ"]
        text = self.__forneceDAO.selectAll()
        self.printQuery(text, campos)

    def verNumPedidos(self):
        campos = ["Id do departamento", "Número de pedidos"]
        text = self.__numPedidosDAO.selectAll()
        self.printQuery(text,campos)

    def verNumCarros(self):
        campos = ["Id do departamento", "Número de veículos"]
        text = self.__numCarrosDAO.selectAll()
        self.printQuery(text,campos)

    def verDespesa(self):
        campos = ["Valor", "Mês", "Ano"]
        text = self.__despesaDAO.selectAll()
        self.printQuery(text,campos)

    def verReceita(self):
        campos = ["Valor", "Mês", "Ano"]
        text = self.__receitaDAO.selectAll()
        self.printQuery(text,campos)
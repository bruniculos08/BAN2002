# Camada de interface com usuário; 
# Camada de negócios, com a lógica da aplicação (na qual se encontra); e
# Camada de dados, com funcionalidade de armazenamento e recuperação.

from tkinter import *
from bson import ObjectId
from Model import *
from Data.Departamento import *
# from Data.Veiculo import *
# from Data.Fornecedor import *
# from Data.Pedido import *
# from Data.Componente import *
from Data.ComponenteNecessario import *
# from Data.Contem import *
# from Data.NotaFiscal import *
# from Data.Fornece import *
# from Data.NumPedidos import *
# from Data.NumCarros import *
# from Data.Despesa import *
# from Data.Receita import *

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
        self.__componenteNecessarioDAO = ComponenteNecessarioDAO()

    def view(self, view):
        self.__view = view
        return self

    def printSucess(self):
        pass

    def printError(self):
        self.__view.clearCampoDeExibicao()
        self.__view.addCampoDeExibicao("Ocorreu algum erro!")

    def printText(self, text):
        self.__view.clearCampoDeExibicao()
        self.__view.addCampoDeExibicao(text)

    def ConstructDict(self, key_field, value_field):
        dictionary = {}
        for field, value in zip(key_field, value_field):
            if value != "":
                dictionary[field] = value  
        return dictionary

    def checkReference(self, refered_database, refered_collection, fields, references) -> bool:
        self.__model = Connection()
        collection = self.__model.getCollection(refered_database, refered_collection)
        dictionary = self.ConstructDict(fields, references)
        result = collection.find_one(dictionary)
        if result != None:
            return True
        return False 
        
    def deleteRefered(self, refered_database, refered_collection, field, reference):
        pass

    def update(self, refered_database, refered_collection, field, reference):
        pass

    def printQuery(self, query, campos):
        # Limpando o campo de texto:
        self.__view.clearCampoDeExibicao()

        # Imprimindo o nome dos atributos no campo de texto:
        self.__view.addCampoDeExibicao("Atributos: ")
        for word in campos[0:-1]:
            self.__view.addCampoDeExibicao(word + ', ')
        self.__view.addCampoDeExibicao(campos[-1] + '.\n\n')

        # Imprimindo as linhas resultantes da query:
        for row in query:
            keys = list(row.keys())
            for key in keys[0:-1]:
                self.__view.addCampoDeExibicao(str(row[key]) + '\t|\t')
            self.__view.addCampoDeExibicao(str(row[keys[-1]]) + '\n\n')

    def clearAndGetData(self):
        dados = self.__view.getCamposDeInsercao()
        self.__view.criarCamposDeInsercao()
        return dados

    def setInserirDepartamento(self):
        # Como o codDept é gerado automaticamente (por sequência, basta inserir o tipo):
        campos = ["Tipo do departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirDepartamento())
        self.__view.criarBotoes(botao)

    # Esta função pega os dados do campo de inserção e insere na tabela de departamento do banco de dados:
    def inserirDepartamento(self):
        try:
            dados = [""] + self.clearAndGetData() + [[]]
            print(dados)
            self.__departamentoDAO.insert(dados)
        except:
             self.printError()

    # Esta função criar os campos de inserção de acordo com a quantidade de atributos da entidade "Departamento" para...
    # ... a operação de 'delete':
    def setDeletarDepartamento(self):
        campos = ["Id do departamento:", "Tipo do departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarDepartamento())
        self.__view.criarBotoes(botao)
            
    # Esta função pega os dados do campo de inserção e deleta na tabela de departamento do banco de dados os itens cujos...
    # ... atributos são iguais aos colocados nos respectivos campos:
    def deletarDepartamento(self):
        try:
            dados = self.clearAndGetData()
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
            dadosSet = [''] + self.clearAndGetData() + ['']
            campos = ["Id do departamento:", "Antigo tipo do departamento:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarDepartamento(dadosSet))
            self.__view.criarBotoes(botao)
        except:
            self.printError()
        
    def atualizarDepartamento(self, dadosSet):
        try:
            dadosCond = self.clearAndGetData()
            if dadosCond[0] != "":
                dadosCond[0] = ObjectId(dadosCond[0])
            self.__departamentoDAO.update(dadosSet, dadosCond, "$set")
            self.printSucess()
        except:
            self.printError()

    # Esta função executa o comando 'select all' sobre a tabela 'departamento':
    def verDepartamento(self):
        campos = ["Id do departamento", "Tipo do departamento"]
        text = self.__departamentoDAO.findAll()
        self.printQuery(text, campos)

    def setInserirComponenteNecessario(self):
        campos = ["Id do Departamento:", "Nome do Componente:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirComponenteNecessario())
        self.__view.criarBotoes(botao)

    def inserirComponenteNecessario(self):
        try:
            data = self.clearAndGetData()
            data[0] = ObjectId(data[0])
            data[2] = int(data[2])
            # Aqui é feita a verificação das "chaves estrangeiras":
            if(self.checkReference("Personalização", "departamento", ["_id", "tipo"], [data[0], "producao"])
            and self.checkReference("Personalização", "componente", ["nome"], [data[1]])):
                self.__componenteNecessarioDAO.insert(data)
                self.printSucess()
            else:
                self.printText("Referência incorreta!") 
        except:
            self.printError()

    def setPrimarioAtualizarComponenteNecessario(self):
        campos = ["Novo id do departamento:", "Novo nome do componente:", "Nova quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarComponenteNecessario())
        self.__view.criarBotoes(botao)
        
    def setSecundarioAtualizarComponenteNecessario(self):
        try:
            dadosSet = self.clearAndGetData()
            if(dadosSet[0] != ''): dadosSet[0] = ObjectId(dadosSet[0])
            if(dadosSet[2] != ''): dadosSet[2] = int(dadosSet[2])

            bool_check_01 = (self.checkReference("Personalização", "departamento", ["_id", "tipo"], [dadosSet[0], "producao"]) or dadosSet[0] == '')
            bool_check_02 = (self.checkReference("Personalização", "componente", ["nome"], [dadosSet[1]] or dadosSet[1] == ''))
            
            if (bool_check_01 and bool_check_02):
                campos = ["Antigo código do departamento:", "Antigo nome do componente:", "Antiga quantidade:"]
                self.__view.criarCamposDeInsercao(campos)
                botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarComponenteNecessario(dadosSet))
                self.__view.criarBotoes(botao)
            else:
                self.printText("Referência incorreta!") 
        except:
            self.printError()

    def atualizarComponenteNecessario(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            if dadosWhere[0] != '': dadosWhere[0] = ObjectId(dadosWhere[0])
            if(dadosWhere[2] != ''): dadosWhere[2] = int(dadosWhere[2])
            self.__componenteNecessarioDAO.update(dadosSet, dadosWhere, "$set")
            self.printSucess()
        except:
            self.printError()

    def verComponenteNecessario(self):
        campos = ["Id do Departamento", "Nome do Componente", "Quantidade"]
        text = self.__componenteNecessarioDAO.project([0, 1, 1, 1])
        self.printQuery(text, campos)
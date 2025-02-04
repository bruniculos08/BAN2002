# Camada de interface com usuário; 
# Camada de negócios, com a lógica da aplicação (na qual se encontra); e
# Camada de dados, com funcionalidade de armazenamento e recuperação.
import datetime
from tkinter import *
from bson import ObjectId
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
        self.__componenteDAO = ComponenteDAO()
        self.__pedidoDAO = PedidoDAO()
        self.__contemDAO = ContemDAO()
        self.__forneceDAO = ForneceDAO()
        self.__fornecedorDAO = FornecedorDAO()
        self.__veiculoDAO = VeiculoDAO()
        self.__notaFiscalDAO = NotaFiscalDAO()

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

    def searchForReferences(self, refered_database, refered_collection, field, field_refered, result):
        self.__model = Connection()
        for row in result:
            value = row[field]
            if(self.checkReference(refered_database, refered_collection, [field_refered], [value])):
                return True
        return False

    def deleteRefered(self, refered_database, refered_collection, field, field_refered, result):
        self.__model = Connection()
        collection = self.__model.getCollection(refered_database, refered_collection)
        for document in list(result):
            value = document[field]
            dictionaryCond = {field_refered: value}
            collection.delete_many(dictionaryCond)

    def updateRefered(self, refered_database, refered_collection, field, reference):
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
            result = self.__departamentoDAO.delete(dados)
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
            dadosSet = [""] + self.clearAndGetData()
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

    # Esta função executa o comando 'find' sobre a coleção 'departamento':
    def verDepartamento(self):
        campos = ["Id do departamento", "Tipo do departamento"]
        text = self.__departamentoDAO.findAll()
        self.printQuery(text, campos)

    def setInserirComponente(self):
            campos = ["Nome:", "Tipo:", "Valor de compra:", "Quantidade Mínima:", "CNPJ Principal:"]
            self.__view.criarCamposDeInsercao(campos)
            botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirComponente())
            self.__view.criarBotoes(botao)

    def inserirComponente(self):
        try:
            data = self.clearAndGetData()
            data = [""] + data[0:4] + [0] + data[4:5]
            data[3] = float(data[3])
            data[4] = int(data[4])
            
            bool_check_01 = self.checkReference("Personalização", "fornecedor", ["cnpj"], [data[6]])
            bool_check_02 = not(self.checkReference("Personalização", "componente", ["nome"], data[1]))

            if(bool_check_01 and bool_check_02):
                self.__componenteDAO.insert(data)
                self.printSucess()
            else:
                self.printText("Referência incorreta ou item já existente!")
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
            dadosSet = [""] + dadosSet[0:4] + [""] + dadosSet[4:5]
            if(dadosSet[3] != ''): dadosSet[3] = int(dadosSet[3])
            if(dadosSet[4] != ''): dadosSet[4] = int(dadosSet[4])

            bool_check_01 = self.checkReference("Personalização", "fornecedor", ["cnpj"], [dadosSet[6]]) or (dadosSet[6] == "") 
            bool_check_02 = self.checkReference("Personalização", "componente", ["nome"], [dadosSet[1]]) or (dadosSet[1] == "")

            if(bool_check_01 and bool_check_02):
                campos = ["Antigo nome:", "Antigo tipo:", "Antigo valor de compra:", "Antigo quantidade mínima:", "Antiga quantidade:", "Antigo CNPJ principal:"]
                self.__view.criarCamposDeInsercao(campos)
                botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarComponente(dadosSet))
                self.__view.criarBotoes(botao)
            else:
                self.printText("Referência incorreta ou item já existente!")
        except:
            self.printError()
            
    def atualizarComponente(self, dadosSet):
        try:
            dadosWhere = [""] + self.clearAndGetData()
            if (dadosWhere[3] != ''): dadosWhere[3] = int(dadosWhere[3])
            if (dadosWhere[4] != ''): dadosWhere[4] = int(dadosWhere[4])
            if (dadosWhere[5] != ''): dadosWhere[5] = int(dadosWhere[2])
            self.__componenteDAO.update(dadosSet, dadosWhere)
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
            data = self.clearAndGetData()
            if (data[2] != ''): data[2] = int(data[2])
            if (data[3] != ''): data[3] = int(data[3])
            if (data[4] != ''): data[4] = int(data[4])
            data = [""] + data
            self.__componenteDAO.delete(data)
            self.printSucess()
        except:
            self.printError()

    def verComponente(self):
        campos = ["Nome", "Tipo", "Valor de compra", "Quantidade Mínima", "Quantidade", "CNPJ Principal"]
        text = self.__componenteDAO.project([0, 1, 1, 1, 1, 1, 1])
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
            data = [""] + data
            
            # Aqui é feita a verificação das "chaves estrangeiras":
            if(self.checkReference("Personalização", "departamento", ["_id", "tipo"], [data[1], "producao"])
            and self.checkReference("Personalização", "componente", ["nome"], [data[2]])):
                self.__componenteNecessarioDAO.insert(data)
                self.printSucess()
            else:
                self.printText("Referência incorreta!") 
        except:
            self.printError()

    def setDeletarComponenteNecessario(self):
        campos = ["Id do departamento:", "Nome do componente:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarComponenteNecessario())
        self.__view.criarBotoes(botao)
    
    def deletarComponenteNecessario(self):
        try:
            dataCond = self.clearAndGetData()
            if dataCond[0] != '': dataCond[0] = ObjectId(dataCond[0])
            if(dataCond[2] != ''): dataCond[2] = int(dataCond[2])
            dataCond = [""] + dataCond
            self.__componenteNecessarioDAO.delete(dataCond)
            self.printSucess()
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
            dadosSet = [""] + dadosSet

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
            dadosWhere = [""] + dadosWhere

            self.__componenteNecessarioDAO.update(dadosSet, dadosWhere, "$set")
            self.printSucess()
        except:
            self.printError()

    def verComponenteNecessario(self):
        campos = ["Id do Departamento", "Nome do Componente", "Quantidade"]
        text = self.__componenteNecessarioDAO.project([0, 1, 1, 1])
        self.printQuery(text, campos)

    def setInserirPedido(self):
        campos = ["CNPJ:", "Id do Departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirPedido())
        self.__view.criarBotoes(botao)

    def inserirPedido(self):
        try:
            dados = [""] + [str(datetime.datetime.today().date())] + self.clearAndGetData()
            dados[3] = ObjectId(dados[3])

            bool_check_01 = self.checkReference("Personalização", "departamento", ["_id", "tipo"], [dados[3], "compra"])
            bool_check_02 = self.checkReference("Personalização", "fornecedor", ["cnpj"], [dados[2]])

            if(bool_check_01 and bool_check_02):    
                self.__pedidoDAO.insert(dados)
                self.printSucess()
            else:
                self.printText("Referência incorreta!") 
        except:
            self.printError()

    def setDeletarPedido(self):    
        campos = ["Id do pedido:", "Data de criação(YYYY-MM-DD):", "CNPJ:", "Id do Departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarPedido())
        self.__view.criarBotoes(botao)

    def deletarPedido(self):
        try:
            dados = self.clearAndGetData()
            if dados[0] != '': dados[0] = ObjectId(dados[0])
            if(dados[3] != ''): dados[3] = ObjectId(dados[3])
            self.__pedidoDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarPedido(self):
        campos = ["Novo CNPJ:", "Novo id do departamento:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarPedido())
        self.__view.criarBotoes(botao)
        
    def setSecundarioAtualizarPedido(self):
        try:
            dadosSet = [""] + [""] + self.clearAndGetData()
            if(dadosSet[3] != ''): dadosSet[3] = ObjectId(dadosSet[3])

            bool_check_01 = self.checkReference("Personalização", "departamento", ["_id", "tipo"], [dadosSet[3], "compra"])
            bool_check_02 = self.checkReference("Personalização", "fornecedor", ["cnpj"], [dadosSet[2]])

            if(bool_check_01 and bool_check_02):
                campos = ["Id do pedido:", "Data de criação(YYYY-MM-DD):", "Antigo CNPJ:", "Antigo id do departamento:"]
                self.__view.criarCamposDeInsercao(campos)
                botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarPedido(dadosSet))
                self.__view.criarBotoes(botao)
            else:
                self.printText("Referência incorreta!")
        except:
            self.printError()
            
    def atualizarPedido(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            if dadosWhere[0] != '': dadosWhere[0] = ObjectId(dadosWhere[0])
            if(dadosWhere[3] != ''): dadosWhere[3] = ObjectId(dadosWhere[3])
            self.__pedidoDAO.update(dadosSet, dadosWhere, "$set")
            self.printSucess()
        except:
            self.printError()

    def verPedido(self):
        campos = ["Id do pedido", "Data de criação(YYYY-MM-DD)", "CNPJ", "Id do Departamento"]
        text = self.__pedidoDAO.findAll()
        self.printQuery(text, campos)

    def setInserirContem(self):
        campos = ["Nome do componente:", "Id do pedido:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirContem())
        self.__view.criarBotoes(botao)

    def inserirContem(self):
        try:
            dados = [""] + self.clearAndGetData()
            dados[2] = ObjectId(dados[2])
            dados[3] = int(dados[3])

            bool_check_01 = self.checkReference("Personalização", "componente", ["nome"], [dados[1]])
            bool_check_02 = self.checkReference("Personalização", "pedido", ["_id"], [dados[2]])
            bool_check_03 = self.checkReference("Personalização", "contem", ["nome_componente", "id_pedido"], [dados[1], dados[2]])

            if(bool_check_03):
                dataCond = [""] + dados[1:3] + [""]
                dataSet = [""] + [""] + [""] + [dados[3]]
                self.__contemDAO.update(dataSet, dataCond, "$inc")
            elif(bool_check_01 and bool_check_02):
                self.__contemDAO.insert(dados)
                self.printSucess()
            else:
                self.printText("Referência incorreta!")
        except:
            self.printError()

    def setDeletarContem(self):
        campos = ["Nome do componente:", "Id do pedido:", "Quantidade:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarContem())
        self.__view.criarBotoes(botao)

    def deletarContem(self):
        try:
            dados = [""] + self.clearAndGetData()
            dados[2] = ObjectId(dados[2])
            dados[3] = int(dados[3])
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
            dadosSet = [""] + self.clearAndGetData()
            if(dadosSet[2] != ''): dadosSet[2] = ObjectId(dadosSet[2])
            if(dadosSet[3] != ""): dadosSet[3] = int(dadosSet[3])

            bool_check_01 = (self.checkReference("Personalização", "componente", ["nome"], [dadosSet[1]]) or dadosSet[1] == "")
            bool_check_02 = (self.checkReference("Personalização", "pedido", ["_id"], [dadosSet[2]]) or dadosSet[2] == "")

            if(bool_check_01 and bool_check_02):
                campos = ["Antigo nome do componente:", "Antigo id do pedido:", "Antiga quantidade:"]
                self.__view.criarCamposDeInsercao(campos)
                botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarContem(dadosSet))
                self.__view.criarBotoes(botao)
            else:
                self.printText("Referência incorreta!")
        except:
            self.printError()
        
    def atualizarContem(self, dadosSet):
        try:
            dadosWhere = [""] + self.clearAndGetData()
            if(dadosWhere[2] != ''): dadosWhere[2] = ObjectId(dadosWhere[2])
            if(dadosWhere[3] != ""): dadosWhere[3] = int(dadosWhere[3])

            self.__contemDAO.update(dadosSet, dadosWhere, "$set")
            self.printSucess()
        except:
            self.printError()

    def verContem(self):
        campos = ["Nome do Componente", "Id do pedido", "Quantidade"]
        text = self.__contemDAO.project([0, 1, 1, 1])
        self.printQuery(text, campos)

    def setInserirFornece(self):
        campos = ["Nome do Componente:", "CNPJ:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirFornece())
        self.__view.criarBotoes(botao)

    def inserirFornece(self):
        try:
            dados = [""] + self.clearAndGetData()

            bool_check_01 = not (self.checkReference("Personalização", "fornece", ["nome_componente", "cnpj"], [dados[1], dados[2]]))
            bool_check_02 = self.checkReference("Personalização", "fornecedor", ["cnpj"], [dados[2]])
            bool_check_03 = self.checkReference("Personalização", "componente", ["nome"], [dados[1]])

            if(bool_check_01 and bool_check_02 and bool_check_03):
                self.__forneceDAO.insert(dados)
                self.printSucess()
            else:
                self.printText("Referência incorreta ou item já existente!")
        except:
            self.printError()

    def setDeletarFornece(self):
        campos = ["Nome do componente:", "CNPJ:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarFornece())
        self.__view.criarBotoes(botao)

    def deletarFornece(self):
        try:
            dados = [""] + self.clearAndGetData()
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
            dadosSet = [""] + self.clearAndGetData()

            bool_check_01 = not(self.checkReference("Personalização", "fornece", ["nome_componente", "cnpj"], [dadosSet[1], dadosSet[2]]))
            bool_check_02 = self.checkReference("Personalização", "fornecedor", ["cnpj"], [dadosSet[2]])
            bool_check_03 = self.checkReference("Personalização", "componente", ["nome"], [dadosSet[1]])

            if(bool_check_01 and bool_check_02 and bool_check_03):
                campos = ["Antigo nome do componente:", "Antigo CNPJ:"]
                self.__view.criarCamposDeInsercao(campos)
                botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarFornece(dadosSet))
                self.__view.criarBotoes(botao)
            else:
                self.printText("Referência incorreta ou item já existente!")
        except:
            self.printError()
            
    def atualizarFornece(self, dadosSet):
        try:
            dadosWhere = [""] + self.clearAndGetData()
            self.__forneceDAO.update(dadosSet, dadosWhere, "$set")
            self.printSucess()
        except:
            self.printError()

    def verFornece(self):
        campos = ["Nome do Componente", "CNPJ"]
        text = self.__forneceDAO.project([0, 1, 1])
        self.printQuery(text, campos)

    def setInserirFornecedor(self):
        campos = ["CNPJ:", "Nome:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirFornecedor())
        self.__view.criarBotoes(botao)

    def inserirFornecedor(self):
        try:
            dados = [""] + self.clearAndGetData()

            bool_check_01 = not (self.checkReference("Personalização", "fornecedor", ["nome", "cnpj"], [dados[1], dados[2]]))
            bool_check_02 = not (self.checkReference("Personalização", "fornecedor", ["nome"], [dados[1]]))
            bool_check_03 = not (self.checkReference("Personalização", "fornecedor", ["cnpj"], [dados[2]]))

            if(bool_check_01 and bool_check_02 and bool_check_03):
                self.__fornecedorDAO.insert(dados)
                self.printSucess()
            else:
                self.printText("Item já existente (ou cujo um dos campos é igual de um item já existente)!")
        except:
            self.printError()

    def setDeletarFornecedor(self):
        campos = ["CNPJ:", "Nome:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarFornecedor())
        self.__view.criarBotoes(botao)

    def deletarFornecedor(self):
        try:
            dados = [""] + self.clearAndGetData()
            result = self.__fornecedorDAO.findAll(dados)

            bool_check_01 = not(self.searchForReferences("Personalização", "componente", "cnpj", "cnpj_principal", result))
            bool_check_02 = not(self.searchForReferences("Personalização", "pedido", "cnpj", "cnpj", result))

            if(bool_check_01 and bool_check_02):
                self.deleteRefered("Personalização", "fornece", "cnpj", "cnpj", self.__fornecedorDAO.findAll(dados))
                self.__fornecedorDAO.delete(dados)
                self.printSucess()
            else:
                self.printText("O documento não pode ser deletado pois é referenciado em outra tabela que não pode ser deletada em cascata!")
        except:
            self.printError() 

    def setPrimarioAtualizarFornecedor(self):
        campos = ["Novo CNPJ:", "Novo nome:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarFornecedor())
        self.__view.criarBotoes(botao)
        
    def setSecundarioAtualizarFornecedor(self):
        try:
            dadosSet = [""] + self.clearAndGetData()

            bool_check_01 = not (self.checkReference("Personalização", "fornecedor", ["cnpj"], [dadosSet[1]]) and dadosSet[1] != "")
            bool_check_02 = not (self.checkReference("Personalização", "fornecedor", ["nome"], [dadosSet[2]]) and dadosSet[2] != "")

            if(bool_check_01 and bool_check_02):
                campos = ["Antigo CNPJ:", "Antigo nome:"]
                self.__view.criarCamposDeInsercao(campos)
                botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarFornecedor(dadosSet))
                self.__view.criarBotoes(botao)
            else:
                self.printText("Item já existente (ou cujo um dos campos é igual de um item já existente)!")
        except:
            self.printError()

    def atualizarFornecedor(self, dadosSet):
        try:
            dadosWhere = [""] + self.clearAndGetData()
            self.__fornecedorDAO.update(dadosSet, dadosWhere, "$set")
            self.printSucess() 
        except:
            self.printError()

    def verFornecedor(self):
        campos = ["CNPJ", "Nome"]
        text = self.__fornecedorDAO.project([0, 1, 1])
        self.printQuery(text, campos)

    def setInserirVeiculo(self):
        campos = ["Chassi:", "Valor de produção:", "Id de departamento:"] # quando inserido estágio = "início"
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirVeiculo())
        self.__view.criarBotoes(botao)

    def inserirVeiculo(self):
        try:
            dados = self.clearAndGetData()
            dados = [""] + [dados[0]] + [dados[1]] + [str(datetime.datetime.today().date())] + [dados[2]] + ["inicio"]
            dados[2] = float(dados[2])
            dados[4] = ObjectId(dados[4])

            bool_check_01 = self.checkReference("Personalização", "departamento", ["_id", "tipo"], [dados[4], "producao"])
            bool_check_02 = not (self.checkReference("Personalização", "veiculo", ["chassi"], [dados[1]]))

            if(bool_check_01 and bool_check_02):
                self.__veiculoDAO.insert(dados)
                self.printSucess()
            else:
                self.printText("Referência incorreta ou chassi inválido (ou repetido)!")
        except:
            self.printError()

    def setDeletarVeiculo(self):
        campos = ["Chassi:", "Valor de produção:", "Data de produção(YYYY-MM-DD):", "Id de departamento:", "Estágio:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarVeiculo())
        self.__view.criarBotoes(botao)
        
    def deletarVeiculo(self):
        try:
            dados = [""] + self.clearAndGetData()
            if(dados[2] != ""): dados[2] = float(dados[2])
            if(dados[4] != ""): dados[4] = ObjectId(dados[4])
            self.__veiculoDAO.delete(dados)
            self.printSucess()
        except:
            self.printError()

    def setPrimarioAtualizarVeiculo(self):
        campos = ["Novo chassi:", "Novo valor de produção:", "Novo id de departamento:", "Novo Estágio:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.setSecundarioAtualizarVeiculo())
        self.__view.criarBotoes(botao)

    def setSecundarioAtualizarVeiculo(self):
        try:
            dadosSet = self.clearAndGetData()
            dadosSet = [""] + [dadosSet[0]] + [dadosSet[1]] + [""] + [dadosSet[2]] + [dadosSet[3]]
            if(dadosSet[2] != ""): dadosSet[2] = float(dadosSet[2])
            if(dadosSet[3] != ""): dadosSet[3] = ObjectId(dadosSet[4])

            bool_check_01 = not(self.checkReference("Personalização", "veiculo", ["chassi"], [dadosSet[1]]))
            bool_check_02 = self.checkReference("Personalização", "departamento", ["_id", "tipo"], [dadosSet[4], "producao"])

            if(bool_check_01 and bool_check_02):
                campos = ["Id do veículo:", "Antigo chassi:", "Antigo valor de produção:", "Antiga data de produção(YYYY-MM-DD):", "Antigo id de departamento:", "Antigo estágio:"]
                self.__view.criarCamposDeInsercao(campos)
                botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarVeiculo(dadosSet))
                self.__view.criarBotoes(botao)
            else:
                self.printText("Referência incorreta ou chassi inválido (ou repetido)!")
        except:
            self.printError()
        
    def atualizarVeiculo(self, dadosSet):
        try:
            dadosWhere = self.clearAndGetData()
            if(dadosWhere[2] != ""): dadosWhere[2] = float(dadosWhere[2])
            if(dadosWhere[4] != ""): dadosWhere[4] = ObjectId(dadosWhere[4])

            self.__veiculoDAO.update(dadosSet, dadosWhere, "$set")
            self.printSucess()
        except:
            self.printError()

    def verVeiculo(self):
        campos = ["Chassi", "Valor de produção", "Data de produção(YYYY-MM-DD)", "Código de departamento", "Estágio"]
        text = self.__veiculoDAO.project([0, 1, 1, 1, 1, 1])
        self.printQuery(text, campos)

    def setInserirNotaFiscal(self):
        campos = ["Código da nota:", "Id do pedido:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.inserirNotaFiscal())
        self.__view.criarBotoes(botao)

    def inserirNotaFiscal(self):
        try:
            dados = [""] + self.clearAndGetData()
            dados[2] = ObjectId(dados[2])

            bool_check_01 = not(self.checkReference("Personalização", "nota_fiscal", ["cod_nota"], [dados[1]]))
            bool_check_02 = self.checkReference("Personalização", "pedido", ["_id"], [dados[2]])

            if(bool_check_01 and bool_check_02):
                self.__notaFiscalDAO.insert(dados)
                self.printSucess()
            else:
                self.printText("Referência incorreta ou código da nota inválido (ou repetido)!")
        except:
            self.printError()

    def setDeletarNotaFiscal(self):
        campos = ["Código da nota:", "Id do pedido:"]
        self.__view.criarCamposDeInsercao(campos)
        botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.deletarNotaFiscal())
        self.__view.criarBotoes(botao)
            
    def deletarNotaFiscal(self):
        try:
            dados = [""] + self.clearAndGetData()
            if(dados[2] != ''): dados[2] = ObjectId(dados[2])
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
            dadosSet = [""] + self.clearAndGetData()
            if(dadosSet[2] != ''): dadosSet[2] = ObjectId(dadosSet[2])

            bool_check_01 = ((self.checkReference("Personalização", "pedido", ["_id"], [dadosSet[2]])) or (dadosSet[2] == ""))
            bool_check_02 = (not(self.checkReference("Personalização", "nota_fiscal", ["cod_nota"], [dadosSet[1]]))) or (dadosSet[1] == "")

            if(bool_check_01 and bool_check_02):
                campos = ["Antigo código da nota:", "Antigo id do pedido:"]
                self.__view.criarCamposDeInsercao(campos)
                botao = Button(self.__view.getFieldBoxFrame(), text = "Enviar dados", state = 'normal', command = lambda : self.atualizarNotaFiscal(dadosSet))
                self.__view.criarBotoes(botao)
            else:
                self.printText("Referência incorreta ou código da nota inválido (ou repetido)!")
        except:
            self.printError()
            
    def atualizarNotaFiscal(self, dadosSet):
        try:
            dadosWhere = [""] + self.clearAndGetData()
            if(dadosWhere[2] != ''): dadosWhere[2] = ObjectId(dadosWhere[2])
            self.__notaFiscalDAO.update(dadosSet, dadosWhere, "$set")
            self.printSucess()
        except:
            self.printError()
        
    def verNotaFiscal(self):
        campos = ["Código da nota", "Id do pedido"]
        text = self.__notaFiscalDAO.project([0, 1, 1])
        self.printQuery(text, campos)
# Camada de interface com usuário (na qual se encontra);
# Camada de negócios, com a lógica da aplicação; e
# Camada de dados, com funcionalidade de armazenamento e recuperação.

from Model import *
from Controller import *
from tkinter import *
from PIL import ImageTk, Image

# Aqui ficarão as classes de interface:
class View():
    # Objeto da classe principal do menu:
    __tela = Tk()
    # Objeto da classe de frame que será usado para as caixas de entrada:
    __fieldBoxFrame = None
    # Como poderá haver mais de uma caixa de entrada devemos ter um vetor para acessá-las:
    __fieldBoxes = None
    # Objeto da classe da caixa texto, onde serão exibidos os resultados:
    __textBox = None
    # Controller que fará a comunicação com o banco de dados:
    __controller = None

    def __init__(self):
        self.__controller = Controller().view(self)
        self.colocarImagem()
        self.createTextBox()
        self.criarBotoesDeAba()
        self.criarCamposDeInsercao()
        self.setCampoDeExibicao(" ")
        self.ajustarTela()

    def run(self):
        self.__tela.mainloop()

    def getFieldBoxFrame(self):
        return self.__fieldBoxFrame

    def ajustarTela(self):
        self.__tela.geometry("1280x720")
        self.__tela.minsize(width=1280, height=720)
        self.__tela.maxsize(width=1280, height=720)
        self.__tela.title("Personalização de veículos")
        return

    def colocarImagem(self):
        # Criando frame para colocar a label contendo a imagem:
        frame = Frame(self.__tela, width=450, height=240)
        frame.pack()
        frame.place(anchor="center", relx=0.5, rely=0.5)

        # O problema que estava ocorrendo antes era devido ao item imagem não estar acessível ao resto da...
        # ... classe (o coletor de lixo apaga tal variável se esta for declarada sem o 'self.' ou sem 'global'):
        imagePath = "C:\\Users\\bruni\\OneDrive\Documentos\\GitHub\\BAN2002\Trabalho01\Arquivos Gerais\\Imagem de Menu.gif"
        self.imagem_de_menu = ImageTk.PhotoImage(Image.open(imagePath).resize((1280,720), Image.ANTIALIAS))
        # Explicações para o problema em: 
        # https://stackoverflow.com/questions/16424091/why-does-tkinter-image-not-show-up-if-created-in-a-function

        # Criando label para colocar a imagem:
        label_para_imagem = Label(frame, image = self.imagem_de_menu)
        label_para_imagem.pack()
        return
        
    def criarBotoesDeAba(self):

        def botaoFuncionando(string):
            text = "Este botão (" + string + ") está funcionando."
            self.setCampoDeExibicao(text)

        # Criando lista de botões de aba (comands para uma cascade)
            
        # Botão para opções relacionadas a departamentos:
        listaDeBotoesDepartamento = Menu(self.__tela, tearoff=0)
        listaDeBotoesDepartamento.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirDepartamento())
        listaDeBotoesDepartamento.add_command(label = "Ver todos", command = lambda : self.__controller.verDepartamento())
        listaDeBotoesDepartamento.add_command(label = "Remover", command = lambda : self.__controller.setDeletarDepartamento())
        listaDeBotoesDepartamento.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarDepartamento())
        
        # Botão para opções relacionadas a fornecedores:
        listaDeBotoesFornecedor = Menu(self.__tela, tearoff=0)
        listaDeBotoesFornecedor.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirFornecedor())
        listaDeBotoesFornecedor.add_command(label = "Ver todos", command = lambda : self.__controller.verFornecedor())
        listaDeBotoesFornecedor.add_command(label = "Remover", command = lambda : self.__controller.setDeletarFornecedor())
        listaDeBotoesFornecedor.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarFornecedor())

        # Botão para opções relacionadas à veículos:
        listaDeBotoesVeiculo = Menu(self.__tela, tearoff=0)
        listaDeBotoesVeiculo.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirVeiculo())
        listaDeBotoesVeiculo.add_command(label = "Ver todos", command = lambda : self.__controller.verVeiculo())
        listaDeBotoesVeiculo.add_command(label = "Ver veículos por departamento", command = lambda : self.__controller.verNumCarros())
        listaDeBotoesVeiculo.add_command(label = "Remover", command = lambda : self.__controller.setDeletarVeiculo())
        listaDeBotoesVeiculo.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarVeiculo())
        
        # Botão para opções relacionadas à pedidos:
        listaDeBotoesPedido = Menu(self.__tela, tearoff=0)
        listaDeBotoesPedido.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirPedido())
        listaDeBotoesPedido.add_command(label = "Ver todos", command = lambda : self.__controller.verPedido())
        listaDeBotoesPedido.add_command(label = "Ver pedidos por departamento", command = lambda : self.__controller.verNumPedidos())
        listaDeBotoesPedido.add_command(label = "Remover", command = lambda : self.__controller.setDeletarPedido())
        listaDeBotoesPedido.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarPedido())

        # Botão para opções relacionadas à componentes:
        listaDeBotoesComponente = Menu(self.__tela, tearoff=0)
        listaDeBotoesComponente.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirComponente())
        listaDeBotoesComponente.add_command(label = "Ver todos", command = lambda : self.__controller.verComponente())
        listaDeBotoesComponente.add_command(label = "Remover", command = lambda : self.__controller.setDeletarComponente())
        listaDeBotoesComponente.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarComponente())

        # Botão para opções relacionadas à componentes necessario:
        listaDeBotoesComponenteNecessario = Menu(self.__tela, tearoff=0)
        listaDeBotoesComponenteNecessario.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirComponenteNecessario())
        listaDeBotoesComponenteNecessario.add_command(label = "Ver todos", command = lambda : self.__controller.verComponenteNecessario())
        listaDeBotoesComponenteNecessario.add_command(label = "Remover", command = lambda : self.__controller.setDeletarComponenteNecessario())
        listaDeBotoesComponenteNecessario.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarComponenteNecessario())
        
        # Botão para opções relacionadas à contem:
        listaDeBotoesContem = Menu(self.__tela, tearoff=0)
        listaDeBotoesContem.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirContem())
        listaDeBotoesContem.add_command(label = "Ver todos", command = lambda : self.__controller.verContem())
        listaDeBotoesContem.add_command(label = "Remover", command = lambda : self.__controller.setDeletarContem())
        listaDeBotoesContem.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarContem())

        # Botão para opções relacionadas à nota fiscal:
        listaDeBotoesNotaFiscal = Menu(self.__tela, tearoff=0)
        listaDeBotoesNotaFiscal.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirNotaFiscal())
        listaDeBotoesNotaFiscal.add_command(label = "Ver todos", command = lambda : self.__controller.verNotaFiscal())
        listaDeBotoesNotaFiscal.add_command(label = "Remover", command = lambda : self.__controller.setDeletarNotaFiscal())
        listaDeBotoesNotaFiscal.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarNotaFiscal())

        # Botão para opções relacionadas a fornece:
        listaDeBotoesFornece = Menu(self.__tela, tearoff=0)
        listaDeBotoesFornece.add_command(label = "Adicionar", command = lambda : self.__controller.setInserirFornece())
        listaDeBotoesFornece.add_command(label = "Ver todos", command = lambda : self.__controller.verFornece())
        listaDeBotoesFornece.add_command(label = "Remover", command = lambda : self.__controller.setDeletarFornece())
        listaDeBotoesFornece.add_command(label = "Atualizar", command = lambda : self.__controller.setPrimarioAtualizarFornece())

        # Botão para opções relacionadas ao orçamento:
        listaDeBotoesOrcamento = Menu(self.__tela, tearoff=0)
        listaDeBotoesOrcamento.add_command(label = "Ver despesas mensais", command = lambda : self.__controller.verDespesa())
        listaDeBotoesOrcamento.add_command(label = "Ver receitas mensais", command = lambda : self.__controller.verReceita())
        
        # Criando barra superior de botões de aba:
        listaDelistaDeBotoes = Menu(self.__tela)
        listaDelistaDeBotoes.add_cascade(label = "Departamentos", menu = listaDeBotoesDepartamento)
        listaDelistaDeBotoes.add_cascade(label = "Fornecedores", menu = listaDeBotoesFornecedor)
        listaDelistaDeBotoes.add_cascade(label = "Veículos", menu = listaDeBotoesVeiculo)
        listaDelistaDeBotoes.add_cascade(label = "Pedidos", menu = listaDeBotoesPedido)
        listaDelistaDeBotoes.add_cascade(label = "Componentes", menu = listaDeBotoesComponente)
        listaDelistaDeBotoes.add_cascade(label = "Componentes Requisitados", menu = listaDeBotoesComponenteNecessario)
        listaDelistaDeBotoes.add_cascade(label = "Componente(s) por pedido", menu = listaDeBotoesContem)
        listaDelistaDeBotoes.add_cascade(label = "Fornecedor por componente", menu = listaDeBotoesFornece)
        listaDelistaDeBotoes.add_cascade(label = "Nota Fiscal", menu = listaDeBotoesNotaFiscal)
        listaDelistaDeBotoes.add_cascade(label = "Orçamento", menu = listaDeBotoesOrcamento)

        # Adicionando a lista de listas de botões criados à tela:
        self.__tela.config(menu = listaDelistaDeBotoes)
    
    # Abrir campo de inserção:
    def setOnCampoDeInsercao(self, string):
        # Verificando se o frame foi criado:
        if self.fieldBox != None:
            return
        # Criando frame para colocar a fieldBox:
        fieldBoxFrameColor = 'purple'
        fieldBoxFrame = Frame(self.__tela, bd = 2, width=400, height=80, bg = fieldBoxFrameColor, relief=SOLID)
        fieldBoxFrame.pack()
        fieldBoxFrame.place(anchor="center", relx=0.2, rely=0.50)
        # Criando label para colocar fieldBox:
        fieldBoxLabel = Label(fieldBoxFrame, text = string, bg = fieldBoxFrameColor, font =("Courier", 12))
        fieldBoxLabel.place(anchor="n", relx=0.5, rely=0.05)
        # Criando a fieldBox:
        self.fieldBox = Entry(fieldBoxFrame, width=61, borderwidth=2, bg = 'white', relief=SOLID)
        self.fieldBox.place(anchor="center", relx=0.5, rely=0.5)

    def criarCamposDeInsercao(self, campos = []):
        quantidade = len(campos)
        self.setCampoDeExibicao(" ")
        if self.__fieldBoxFrame != None: 
            self.__fieldBoxFrame.destroy()
        if quantidade == 0:
            return
        # Ajustando o frame onde serão colocadas os campos de entrada:
        self.__fieldBoxFrame = Frame(self.__tela, bd = 2, width=400, height=(46.5)*quantidade + 50, bg = "purple", relief=SOLID)
        self.__fieldBoxFrame.pack()
        self.__fieldBoxFrame.place(anchor="center", relx=0.2, rely=0.50)
        self.__fieldBoxes = []
        # Adicionando campos de entradas:
        for i in range(0, 2*quantidade, 2):
            fieldBoxLabel = Label(self.__fieldBoxFrame, text = f"{campos[int(i/2)]}", height = 2, width = 40, bg = 'purple', font = ("Courier", 11, "bold"))
            fieldBoxLabel.pack()
            fieldBoxLabel.place(anchor="n", x=200, y=23*i + 0.1)

            fieldBox = Entry(self.__fieldBoxFrame, width=50, borderwidth=2, bg = 'white', relief=SOLID)
            fieldBox.place(anchor="n", x=200, y=23*(i+1.1) + 0.1)
            self.__fieldBoxes.append(fieldBox)

    def criarBotoes(self, botao):
        # Criando botão de envio dos dados:
        self.__tela.update()
        botao.pack()
        botao.place(anchor = "n", x = 250, y = self.__fieldBoxFrame.winfo_height() - 35) 
        cancel = Button(self.getFieldBoxFrame(), text = "Cancelar", state = 'normal', command = lambda : self.criarCamposDeInsercao())
        cancel.pack()
        cancel.place(anchor="n", x = 150, y = self.__fieldBoxFrame.winfo_height() - 35)
    
    def getCamposDeInsercao(self):
        if self.__fieldBoxes == None:
            return []
        dados = []
        for field in self.__fieldBoxes:
            item = field.get()
            dados.append(item)
        return dados

    def deletarCamposDeInsercao(self):
        self.__fieldBoxFrame.destroy()
        for field in self.__fieldBoxes:
            field.destroy()

    # Fechar campo de inserção:
    def setOffCampoDeInsercao(self):
        if self.__fieldBoxFrame == None:
            return
        self.deletarCamposDeInsercao()
        self.__fieldBoxFrame.destroy()
        self.__fieldBoxFrame = None

    def createTextBox(self):
        # Criando os objetos:
        self.__textBox = Text(self.__tela, height=30, width=80, borderwidth=2, relief="solid")
        self.__textBox.config(font =("Courier", 10, "bold"))
        label = Label(self.__tela, text = "Resultado", width=50, bg = "grey", borderwidth=2, relief="solid")
        label.config(font = ("Courier", 10, "bold"))
        # Packs e places do label:
        label.pack()
        label.place(anchor="center", relx=0.7, rely=0.1)
        # Packs e places da textBox:
        self.__textBox.pack()
        self.__textBox.place(anchor="n", relx=0.7, rely=0.14)
        self.__textBox.config(state=DISABLED)
        return

    def setCampoDeExibicao(self, string):
        self.__textBox.config(state=NORMAL)
        self.__textBox.delete('1.0', END)
        self.__textBox.insert(END, string)
        self.__textBox.config(state=DISABLED)

    def clearCampoDeExibicao(self):
        self.__textBox.config(state=NORMAL)
        self.__textBox.delete('1.0', END)
        self.__textBox.config(state=DISABLED)

    def addCampoDeExibicao(self, string):
        self.__textBox.config(state=NORMAL)
        self.__textBox.insert(END, string)
        self.__textBox.config(state=DISABLED)
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

    def __init__(self):
        self.colocarImagem()
        self.criarBotoesDeAba()
        self.criarCamposDeInsercao(2, None)
        self.createTextBox()
        self.setCampoDeExibicao("Texto...")
        self.ajustarTela()
        return

    def run(self):
        self.__tela.mainloop()
        return

    def ajustarTela(self):
        self.__tela.geometry("1280x720")
        self.__tela.minsize(width=1280, height=720)
        self.__tela.maxsize(width=1280, height=720)
        self.__tela.title("Fábrica de veículos")
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
        listaDeBotoesDepartamento.add_command(label = "Adicionar departamento", command = lambda : botaoFuncionando("adicionar departamento comum"))
        listaDeBotoesDepartamento.add_command(label = "Adicionar comprador", command = lambda : botaoFuncionando("adicionar departamento de compras"))
        
        # Botão para opções relacionadas à veículos:
        listaDeBotoesVeiculo = Menu(self.__tela, tearoff=0)
        listaDeBotoesVeiculo.add_command(label = "Adicionar", command = lambda : botaoFuncionando("adicionar veículo"))
        listaDeBotoesVeiculo.add_command(label = "Remover", command = lambda : botaoFuncionando("remover veículo"))
        
        # Botão para opções relacionadas à pedidos:
        listaDeBotoesPedido = Menu(self.__tela, tearoff=0)
        listaDeBotoesPedido.add_command(label = "Adicionar", command = lambda : botaoFuncionando("adicionar pedido de compra"))
        listaDeBotoesPedido.add_command(label = "Ver lista", command = lambda : botaoFuncionando("ver lista de pedidos"))
        listaDeBotoesPedido.add_command(label = "Remover", command = lambda : botaoFuncionando("Remover pedido de compra"))

        # Botão para opções relacionadas à componentes:
        listaDeBotoesComponente = Menu(self.__tela, tearoff=0)
        listaDeBotoesComponente.add_command(label = "Adicionar", command = lambda : botaoFuncionando("adicionar componente"))
        listaDeBotoesComponente.add_command(label = "Remover", command = lambda : botaoFuncionando("remover componente"))
        
        # Criando barra superior de botões de aba:
        listaDelistaDeBotoes = Menu(self.__tela)
        listaDelistaDeBotoes.add_cascade(label = "Departamentos", menu = listaDeBotoesDepartamento)
        listaDelistaDeBotoes.add_cascade(label = "Veículos", menu = listaDeBotoesVeiculo)
        listaDelistaDeBotoes.add_cascade(label = "Pedidos", menu = listaDeBotoesPedido)
        listaDelistaDeBotoes.add_cascade(label = "Componentes", menu = listaDeBotoesComponente)

        # Adicionando a lista de listas de botões criados à tela:
        self.__tela.config(menu = listaDelistaDeBotoes)
        return
    
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
        return

    def criarCamposDeInsercao(self, quantidade = 0, controller = Controller().view(__tela)):
        if(quantidade == 0):
            return
        
        # Ajustando o frame onde serão colocadas os campos de entrada:
        self.__fieldBoxFrame = Frame(self.__tela, bd = 2, width=400, height=(46.5)*quantidade + 50, bg = "purple", relief=SOLID)
        self.__fieldBoxFrame.pack()
        self.__fieldBoxFrame.place(anchor="center", relx=0.2, rely=0.50)
        self.__fieldBoxes = []

        # Criando botão de envio dos dados:
        enviar = Button(self.__fieldBoxFrame, text = "Enviar dados", state = 'normal', command = lambda : controller.inserirDepartamento())
        enviar.pack()
        enviar.place(anchor="n", x = 200, y = (46.5)*quantidade + 15)

        # Adicionando campos de entradas:
        for i in range(0, 2*quantidade, 2):
            fieldBoxLabel = Label(self.__fieldBoxFrame, text = f"Campo {int(i/2)+1}:", height = 2, width = 10, bg = 'purple', font =("Courier", 10))
            fieldBoxLabel.pack()
            fieldBoxLabel.place(anchor="n", x=200, y=23*i + 0.1)

            fieldBox = Entry(self.__fieldBoxFrame, width=50, borderwidth=2, bg = 'white', relief=SOLID)
            fieldBox.place(anchor="n", x=200, y=23*(i+1.1) + 0.1)
            self.__fieldBoxes.append(fieldBox)
        return
    
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
        return

    # Fechar campo de inserção:
    def setOffCampoDeInsercao(self):
        if self.fieldBox == None:
            return
        self.fieldBox.destroy()
        self.fieldBox = None
        return

    def createTextBox(self):
        # Criando os objetos:
        self.__textBox = Text(self.__tela, height=40, width=100, borderwidth=4, relief="solid")
        self.__textBox.config(font =("Courier", 8))
        label = Label(self.__tela, text = "Resultado", width=50, bg = "grey", borderwidth=6.4, relief="solid")
        label.config(font =("Courier", 12))

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
        return    
# Camada de interface com usuário (na qual se encontra);
# Camada de negócios, com a lógica da aplicação; e
# Camada de dados, com funcionalidade de armazenamento e recuperação.

from Logic import *
from tkinter import *
from PIL import ImageTk, Image

# Aqui ficarão as classes de interface:
class MenuPrincipal():
    tela = Tk()

    def __init__(self):
        self.colocarImagem()
        self.criarBotoesDeAba()
        self.ajustarTela()
        self.tela.mainloop()
    
    def ajustarTela(self):
        self.tela.geometry("900x480")
        self.tela.minsize(width=900, height=480)
        self.tela.maxsize(width=900, height=480)
        self.tela.title("Fábrica de veículos")

    def colocarImagem(self):
        frame = Frame(self.tela, width=450, height=240)
        frame.pack()
        frame.place(anchor="center", relx=0.5, rely=0.5)
        # O problema que estava ocorrendo antes era devido ao item imagem não estar acessível ao resto da...
        # ... classe (o coletor de lixo apaga tal variável se esta for declarada sem o 'self.' ou sem 'global'):
        self.imagem_de_menu = ImageTk.PhotoImage(Image.open("Arquivos Gerais\\Imagem de Menu.gif").resize((900,480), Image.ANTIALIAS))
        label_para_imagem = Label(frame, image = self.imagem_de_menu)
        label_para_imagem.pack()
        # Explicações para o problema em: 
        # https://stackoverflow.com/questions/16424091/why-does-tkinter-image-not-show-up-if-created-in-a-function
        
    def criarBotoesDeAba(self):

        def botaoFuncionando(string):
            print(f"Este botão ({string}) está funcionando")

        # Criando lista de botões de aba (comands para uma cascade)
            
        # Botão para opções relacionadas a departamentos:
        listaDeBotoesDepartamento = Menu(self.tela, tearoff=0)
        listaDeBotoesDepartamento.add_command(label = "Adicionar departamento", command = lambda : botaoFuncionando("adicionar departamento comum"))
        listaDeBotoesDepartamento.add_command(label = "Adicionar comprador", command = lambda : botaoFuncionando("adicionar departamento de compras"))
        
        # Botão para opções relacionadas à veículos:
        listaDeBotoesVeiculo = Menu(self.tela, tearoff=0)
        listaDeBotoesVeiculo.add_command(label = "Adicionar", command = lambda : botaoFuncionando("adicionar veículo"))
        listaDeBotoesVeiculo.add_command(label = "Remover", command = lambda : botaoFuncionando("remover veículo"))
        
        # Botão para opções relacionadas à pedidos:
        listaDeBotoesPedido = Menu(self.tela, tearoff=0)
        listaDeBotoesPedido.add_command(label = "Adicionar", command = lambda : botaoFuncionando("adicionar pedido de compra"))
        listaDeBotoesPedido.add_command(label = "Ver lista", command = lambda : botaoFuncionando("ver lista de pedidos"))
        listaDeBotoesPedido.add_command(label = "Remover", command = lambda : botaoFuncionando("Remover pedido de compra"))

        # Botão para opções relacionadas à componentes:
        listaDeBotoesComponente = Menu(self.tela, tearoff=0)
        listaDeBotoesComponente.add_command(label = "Adicionar", command = lambda : botaoFuncionando("adicionar componente"))
        listaDeBotoesComponente.add_command(label = "Remover", command = lambda : botaoFuncionando("remover componente"))
        
        # Criando barra superior de botões de aba:
        listaDelistaDeBotoes = Menu(self.tela)
        listaDelistaDeBotoes.add_cascade(label = "Departamentos", menu = listaDeBotoesDepartamento)
        listaDelistaDeBotoes.add_cascade(label = "Veículos", menu = listaDeBotoesVeiculo)
        listaDelistaDeBotoes.add_cascade(label = "Pedidos", menu = listaDeBotoesPedido)
        listaDelistaDeBotoes.add_cascade(label = "Componentes", menu = listaDeBotoesComponente)

        # Adicionando a lista de listas de botões criados à tela:
        self.tela.config(menu = listaDelistaDeBotoes)
    
    # Abrir campo de inserção ou fechar:
    def setCampoDeInserção(self, state):
        field = Entry()
        pass
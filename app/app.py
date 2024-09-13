from utils.utils import Utils
from models.usuario import Usuario
from models.produto import Produto

class App:

    def __init__(self,database): # Recebe um objeto database
        self.database = database

    def menu_inicial(self):
        
        #REESCREVA-ME 53928352992532368236836283629806234908-860843q689042780-962789072468902674890674987246987642-8962-902678-2647-04267-9024  37163468703
        while True:
            self.__tela_inicial()
            escolha = input("Selecione uma opção: ")
            match(escolha):
                case("1"):
                    self.cadastro_usuario()
                    continue
                case("2"):
                    if self.login() == False:
                        continue
                    else:
                        break
                case("3"):
                    Utils.limpar_tela()
                    exit()
                case _:
                    print("Escolha inválida")
                    continue
    
    def cadastro_usuario(self): # limpa tela, cria uma instancia e executa o cadastro
        Utils.limpar_tela()

        usuario = Usuario(self.database)
        usuario.cadastro()

    def login(self): # TODO EU ACHO
        Utils.limpar_tela()
        
        usuario = Usuario(self.database)
        
        if usuario.login() == False:
            return False
        else:
            self.__menu_restaurante(usuario)
        
    def __menu_restaurante(self,usuario): # obvio REESCREMAGVJK IJKIEJ+)IE$WT)_t4ep´4236bb4 6,m643bq8   9-34u65m-0
        
        while True: 
            self.__painel(usuario)
            escolha = input("Selecione uma opção: ")
            
            match(escolha):
                case("1"):
                    self.cadastro_produto(usuario)
                    continue
                case("2"):
                    self.apagar_produto(usuario)
                    continue
                case("3"):
                    self.alterar_comissao(usuario)
                    continue
                case("4"):
                    self.logout(usuario)
                    break
                case _:
                    print("Escolha inválida")
                    continue
    
    def __tela_inicial(self):
        Utils.limpar_tela()

        print("ANDROID FOOD O FOOD MAIS ANDROID DOS FOODS DO ANDROID")
        print("1 -- Cadastrar")
        print("2 -- Login")
        print("3 -- Sair")
    
    def __painel(self,usuario):
        Utils.limpar_tela()
        print(f"Bem Vindo {usuario.restaurante}!")
        self.__produto_tabela()
        print("1 -- Cadastrar produto")
        print("2 -- Apagar produto")
        print("3 -- Alterar comissão")
        print("4 -- Logout")
                
    def __produto_tabela(self):
        Produto.tabela_produto()
    
    def cadastro_produto(self,usuario):
        Utils.limpar_tela()
        
        produto = Produto(self.database,usuario)
        produto.cadastrar()
    
    def apagar_produto(self):
        Utils.limpar_tela()
        
        produto = Produto(self.database)
        produto.apagar()
    
    def alterar_comissao(self,usuario):
        Utils.limpar_tela()
        
        usuario.alterar_comissao()
    
    def logout(self,usuario): # Deleta o objeto usuario e volta pro menu incial
        del usuario
        self.menu_inicial()
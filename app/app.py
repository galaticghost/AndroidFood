from utils.utils import Utils
from models.usuario import Usuario
from models.produto import Produto

class App:

    def __init__(self,database): # Recebe um objeto database
        self.database = database

    def menu_inicial(self): # A função que da início ao programa
        
        while True: # loop para as opções
            self.__tela_inicial() # Mostra o nome do programa e as opções
            escolha = input("Selecione uma opção: ")
            match(escolha):
                case("1"):
                    self.cadastro_usuario() # cadastro
                    continue
                case("2"):
                    if self.login() == False: # login | Caso o email e a senha estiverem errados ele volta para o inicio
                        continue
                    else:
                        break # caso o contrário ele finaliza o loop
                case("3"):
                    Utils.limpar_tela() # Opção para finalizar o programa
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
        
    def __menu_restaurante(self,usuario): # Tela principal com as opções do restaurante
        
        while True: #loop para o input
            self.__painel(usuario) # Tela com as opções e a tabela dos produtos
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
    
    def __tela_inicial(self): #tela para o menu inicial
        Utils.limpar_tela()

        print("ANDROID FOOD O FOOD MAIS ANDROID DOS FOODS DO ANDROID")
        print("1 -- Cadastrar")
        print("2 -- Login")
        print("3 -- Sair")
    
    def __painel(self,usuario):
        Utils.limpar_tela()
        print(f"Bem Vindo {usuario.restaurante}!")
        usuario.tabela_produto() # função que retorna todos os produtos do restaurante
        print("1 -- Cadastrar produto")
        print("2 -- Apagar produto")
        print("3 -- Alterar comissão")
        print("4 -- Logout")
    
    def cadastro_produto(self,usuario): #limpa a tela, cria uma instância do produto produto e chama o método cadastrar
        Utils.limpar_tela()
        
        produto = Produto(self.database,usuario)
        produto.cadastrar()
    
    def apagar_produto(self,usuario):  #limpa a tela, cria uma instância do produto e chama o método apagar
        Utils.limpar_tela() # Não funcional
        
        produto = Produto(self.database,usuario)
        produto.apagar(usuario)
    
    def alterar_comissao(self,usuario):  #limpa a tela, e chama o método alterar comissão
        Utils.limpar_tela()
        
        usuario.alterar_comissao()
    
    def logout(self,usuario): # Deleta o objeto usuario e volta pro menu incial
        del usuario
        self.menu_inicial()
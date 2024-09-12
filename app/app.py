from utils.utils import Utils
from models.usuario import Usuario

class App:

    def __init__(self,database): # Recebe um objeto database
        self.database = database

    def menu_inicial(self):
        Utils.limpar_tela()

        print("ANDROID FOOD O FOOD MAIS ANDROID DOS FOODS DO ANDROID")
        print("1 -- Cadastrar")
        print("2 -- Login")
        
        #Enquanto o usuário não escolher corretamente, o loop se repete
        while True:
            escolha = input("Selecione uma opção: ")
            match(escolha):
                case("1"):
                    self.cadastro_usuario()
                    break
                case("2"):
                    self.login()
                    break
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
        
        usuario.login()
        
        self.__menu_restaurante(usuario)
        
    def __menu_restaurante(self,usuario): # obvio
        self.__painel(usuario)
        
        while True: 
            escolha = input("Selecione uma opção: ")
            
            match(escolha):
                case("1"):
                    self.cadastro_produto()
                    continue
                case("2"):
                    self.apagar_produto()
                    continue
                case("3"):
                    self.alterar_comissao()
                    continue
                case("4"):
                    self.logout(usuario)
                    break
                case _:
                    print("Escolha inválida")
                    continue
    
    def __painel(self,usuario):
        Utils.limpar_tela()
        print(f"Bem Vindo {usuario.restaurante}!")
        self.__produto_tabela()
        print("1 -- Cadastrar produto")
        print("2 -- Apagar produto")
        print("3 -- Alterar comissão")
        print("4 -- Logout")
                
    def __produto_tabela(self):
        pass
    
    def cadastro_produto(self):
        pass
    
    def apagar_produto(self):
        pass
    
    def alterar_comissao(self):
        pass
    
    def logout(self,usuario):
        del usuario
        self.menu_inicial()
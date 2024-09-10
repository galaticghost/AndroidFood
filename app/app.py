from utils.utils import Utils
from models.usuario import Usuario

class App:

    def __init__(self,database): #Recebe um objeto database
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
                    self.cadastro()
                    break
                case("2"):
                    self.login()
                    break
                case _:
                    print("Escolha inválida")
                    continue
    
    def cadastro(self): # FAZER
        Utils.limpar_tela()

        usuario = Usuario(self.database)
        usuario.cadastro()

    def login(self): # TODO EU ACHO
        Utils.limpar_tela()
        
        usuario = Usuario(self.database)
        
        usuario.login()
        
        self.__painel()
        
    def __painel(): # obvio
        pass
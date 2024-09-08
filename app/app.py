from utils.utils import Utils
from models.usuario import Usuario

class App:

    def __init__(self,database):
        self.database = database

    def menu_inicial(self):
        Utils.limpar_tela()

        print("ANDROID FOOD O FOOD MAIS ANDROID DOS FOODS DO ANDROID")
        print("1 -- Cadastrar")
        print("2 -- Login")
        
        #Enquanto o usuário não escolher as TODO
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
    
    def cadastro(self):
        Utils.limpar_tela()

        usuario = Usuario()
        usuario.cadastro()

    def login(self):
        pass
    
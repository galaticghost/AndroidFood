from utils.utils import Utils
from models.usuario import Usuario

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
                    self.cadastro_produto()
                    continue
                case("2"):
                    self.apagar_produto()
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
    
    def alterar_comissao(self,usuario):
        Utils.limpar_tela()
        print(f"O valor atual da comissão é {usuario.comissao}")
        while True:

            comissao = int(input("Digite o novo valor: ")) # ve ai se da pra fazer input melhor
            
            if comissao <= 0:
                print("Valor Inválido!")
                continue
            else:
                self.database.executar('UPDATE usuario SET comissao = ? WHERE pk_usuario = ? ',(comissao,usuario.pk))
                usuario.comissao = comissao
                break
    
    def logout(self,usuario):
        del usuario
        self.menu_inicial()
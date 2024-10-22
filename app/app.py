from utils.utils import Utils
from models.restaurante import Restaurante
from models.produto import Produto
from models.usuario import Usuario
import time

class App:

    def __init__(self,database): # Recebe um objeto database
        self.database = database

    def __str__(self):
        return f"É o app"

    def menu_inicial_restaurante(self): # A função que da início ao programa
        
        while True: # loop para as opções
            self.__tela_inicial() # Mostra o nome do programa e as opções
            escolha = input("Selecione uma opção: ")
            match(escolha):
                case("1"):
                    self.cadastro_restaurante() # cadastro
                    continue
                case("2"):
                    if self.login_restaurante() == False: # login | Caso o email e a senha estiverem errados ele volta para o inicio
                        continue
                    else:
                        break # caso o contrário ele finaliza o loop
                case("3"):
                    self.database.conexao.close()
                    Utils.limpar_tela() # Opção para finalizar o programa
                    exit()
                case _:
                    print("Escolha inválida")
                    time.sleep(2)
                    continue
    
    def cadastro_restaurante(self): # limpa tela, cria uma instancia e executa o cadastro
        Utils.limpar_tela()

        restaurante = Restaurante(self.database)
        restaurante.cadastro()
        del restaurante

    def login_restaurante(self): # Limpa tela e faz login
        Utils.limpar_tela()
        
        restaurante = Restaurante(self.database)
        
        if restaurante.login() == False: #checa pra ver se o restaurante (senha e email na mesma linha) existe no banco
            return False
        else:
            self.__menu_restaurante(restaurante)
        
    def __menu_restaurante(self,restaurante): # Tela principal com as opções do restaurante
        
        while True: #loop para o input
            self.__painel_restaurante(restaurante) # Tela com as opções e a tabela dos produtos
            escolha = input("Selecione uma opção: ")
            match(escolha):
                case("1"):
                    self.cadastro_produto(restaurante)
                    continue
                case("2"):
                    self.apagar_produto(restaurante)
                    continue
                case("3"):
                    self.alterar_comissao(restaurante)
                    continue
                case("4"):
                    self.logout(restaurante)
                    break
                case _:
                    print("Escolha inválida")
                    time.sleep(2)
                    continue
    
    def __tela_inicial(self): #tela para o menu inicial
        Utils.limpar_tela()

        print("ANDROID FOOD O FOOD MAIS ANDROID DOS FOODS DO ANDROID")
        print("1 -- Cadastrar")
        print("2 -- Login")
        print("3 -- Sair")
    
    def __painel_restaurante(self,restaurante):
        Utils.limpar_tela()
        print(f"Bem-vindo {restaurante.restaurante}!")
        print(f"Seu ultimo acesso foi em {restaurante.acesso}")
        restaurante.tabela_produto() # função que retorna todos os produtos do restaurante
        restaurante.quantidade_produto() # função que retorna a quantidade dos produtos cadastrados
        print(f"O valor da comissão é {restaurante.comissao}")
        print("1 -- Cadastrar produto")
        print("2 -- Apagar produto")
        print("3 -- Alterar comissão")
        print("4 -- Logout")
    
    def cadastro_produto(self,restaurante): #limpa a tela, cria uma instância do produto e chama o método cadastrar
        Utils.limpar_tela()
        
        produto = Produto(self.database,restaurante)
        produto.cadastrar()
        restaurante.update_tem_produto("cadastrar")
    
    def apagar_produto(self,restaurante):  #limpa a tela, cria uma instância do produto e chama o método apagar
        Utils.limpar_tela()
        
        produto = Produto(self.database,restaurante)
        produto.apagar(restaurante)
        restaurante.update_tem_produto("apagar")
    
    def alterar_comissao(self,restaurante):  #limpa a tela, e chama o método alterar comissão
        Utils.limpar_tela()
        
        restaurante.alterar_comissao()
    
    def logout(self,restaurante): # Deleta o objeto restaurante e volta pro menu incial
        del restaurante
        self.menu_inicial_restaurante()
        
    def menu_inicial_usuario(self):
        while True:
            self.__tela_inicial()
            escolha = input("Selecione uma opção: ")
            match(escolha):
                case("1"):
                    self.cadastro_usuario() # cadastro
                    continue
                case("2"):
                    if self.login_usuario() == False: # login | Caso o email e a senha estiverem errados ele volta para o inicio
                        continue
                    else:
                        break # caso o contrário ele finaliza o loop
                case("3"):
                    self.database.conexao.close()
                    Utils.limpar_tela() # Opção para finalizar o programa
                    exit()
                case _:
                    print("Escolha inválida")
                    time.sleep(2)
                    continue

    def cadastro_usuario(self): # limpa tela, cria uma instancia e executa o cadastro
        Utils.limpar_tela()

        usuario = Usuario(self.database)
        usuario.cadastro()
        del usuario
    
    def login_usuario(self):
        Utils.limpar_tela()

        usuario = Usuario(self.database)
        
        if usuario.login() == False: #checa pra ver se o usuario (senha e email na mesma linha) existe no banco
            return False
        else:
            self.__menu_usuario(usuario)

    def __menu_usuario(self,usuario):
        restaurante_id = []
        restaurantes = self.database.consulta_restaurante_lista() # Só recebe restaurantes com produtos

        while True:
            restaurante_id = self.__painel_usuario(usuario,restaurantes,restaurante_id)

            escolha = input("Digite a sua escolha: ")

            if escolha == "0":
                self.__logout_usuario(usuario)
                break
            elif escolha.upper() == "H":
                self.__historico(usuario)
                continue
            try:
                if int(escolha) in restaurante_id: # Se a escolha for um dos ids na lista dos restaurantes
                    self.__catalogo(escolha,usuario)
                    continue
                else:
                    print("Escolha inválida")
                    time.sleep(2)
                    continue
            except:
                    print("Escolha inválida")
                    time.sleep(2)
                    continue

    def __painel_usuario(self,usuario,restaurantes,restaurante_id): # Mostra os restaurantes e as opções
        Utils.limpar_tela()

        if restaurantes == False: # Caso não tenha nenhum restaurante com produtos no banco de dados
            print("Por enquanto nosso app não possui restaurantes")
            time.sleep(4)
            self.__logout_usuario(usuario) # Logout
        else:
            destaques = 0 
            print(f'|{"ID":^6s}|{"Nome":^60s}|')
            for restaurante in restaurantes: # Printa os restaurantes e puxa os ids para uma lista
                time.sleep(0.09)
                if destaques < 3: # Printa os três restaurantes com a maior comissão com uma cor diferente
                    print(f'|\033[35m{str(restaurante[0]):^6s}\033[0m|\033[35m{restaurante[1]:^60s}\033[0m|')
                    restaurante_id.append(restaurante[0])
                    destaques += 1 # adiciona no contador
                else:
                    print(f'|\033[94m{str(restaurante[0]):^6s}\033[0m|\033[94m{restaurante[1]:^60s}\033[0m|')
                    restaurante_id.append(restaurante[0])        
            
            time.sleep(0.09)
            print(f"\nSeu ultimo acesso foi em {usuario.acesso}")
            print("\nDigite o \033[94mid\033[0m do restaurante que deseja ver")
            print("\nCaso deseje ver o histórico das compras digite H")
            print("Caso deseje sair digite 0\n")
            return restaurante_id # Retorna a lista
            
    def __catalogo(self,pk,usuario): # Mostra o catálogo de comidas do restaurante
        restaurante = Restaurante(self.database,pk) # Cria uma instância de restaurante

        while True:
            Utils.limpar_tela()
            result = restaurante.tabela_produto() # Recebe e printa os produtos
            pks = [tupla[0] for tupla in result] # Inseri as pks dos produtos em uma lista
            print("Digite A para abandonar a compra")
            print("Digite F para finalizar a compra")
            
            if not usuario.list: # se o carrinho estiver vazio
                print("Carrinho vazio")
            else:
                print("Carrinho:")
                for produto in usuario.list: # para cada produto no carrinho se printa ele
                    print(f"ID: {produto.pk} | Nome: {produto.nome} | Preço: R${produto.preco * produto.quantidade:.2f} | Quantidade: {produto.quantidade}")

            escolha = input("Digite a sua escolha: ")
            
            if escolha.upper() == "A": # Limpa a lista e encerra o método
                usuario.list = []
                break

            elif escolha.upper() == "F": # Finaliza a aplicação
                if not usuario.list: # Se o carrinho estiver vazio
                    print("Você não cadastrou nenhum produto no carrinho")
                    time.sleep(3)
                    continue

                usuario.venda(pk) # Insere no banco a venda
                usuario.pedido_concluido(pk) # Printa os detalhes dela
                break
            
            try: # Try para evitar ValueErro
                if int(escolha) in pks:
                    while True:
                        try:
                            quantidade = int(input("Digite a quantidade: "))
                            break
                        except:
                            print("Quantidade inválida")
                            continue
                    produto = Produto(self.database,pk) 
                    produto.set_produto(pk,escolha,quantidade) # Adiciona os atributos do produto
                    usuario.lista(produto) # Adiciona (ou remove) o produto do carrinho
                    continue
                else:
                    print("Escolha inválida")
                    time.sleep(2)
                    continue
            except:
                print("Escolha inválida")
                time.sleep(2)
                continue

    def __historico(self,usuario): # Mostra o histórico do usuário
        Utils.limpar_tela()
        historico = self.database.consulta_venda(usuario.pk) # consulta as compras do usuario
        if len(historico) == 0: # Caso não haja nenhuma compra
            print("Seu histórico está vazio")
            input("Pressione <<ENTER>> para voltar para a tela dos restaurantes")
        else:
            usuario.historico(historico) # Chama o método historico do usuario
        
    def __logout_usuario(self,usuario): # Logout do usuario
        del usuario
        self.menu_inicial_usuario()
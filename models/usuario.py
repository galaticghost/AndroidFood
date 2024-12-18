import hashlib
import time
from utils.utils import Utils

class Usuario():
    
    def __init__(self,database): # Recebe a database e já declara a lista
        self.database = database
        self.__list = []
        
    def __str__(self):
        return f"{self.pk},{self.nome},{self.email},{self.senha}"
        
    def cadastro(self):
        
        self.nome = Utils.verifica_nome_completo()
        self.email = Utils.verifica_email(self.database)
        self.senha = Utils.verifica_senha()

        self.database.executar("INSERT INTO usuario(nome_usuario,email_usuario,senha_usuario) VALUES (?,?,?)",(self.nome,self.email,self.senha))

    def login(self):
        
        self.email = input("Digite o seu email: ").lower().strip() # Recebe o email 
        self.senha = input("Digite a sua senha: ") # e a senha
        self.senha = hashlib.md5(self.senha.encode()) # Depois ela é criptografada
        self.senha = self.senha.hexdigest() # E convertida em str

        if (self.database.consulta_login("usuario",self.email,self.senha) == False or self.database.consulta_admin(self.email,self.senha) == 1): #consulta no banco se o login existe
            print("Usuário inválido")
            time.sleep(2)
            return False
        else:
            result = self.database.consulta_usuario(self.email,self.senha) # lista com os atributos novos
            self.database.executar("UPDATE usuario SET ultima_atualizacao = datetime('now','localtime') WHERE email_usuario = ? AND senha_usuario = ?",(self.email,self.senha)) # atualiza a data do ultimo login

            self.pk = result[0]
            self.nome = result[1]
            self.acesso = result[2]
            return True

    def lista(self,produto): # gerencia a lista do cliente
        for item in self.list:
            if item.pk == produto.pk: # Se o produto estiver já cadastrado na lista
                if produto.quantidade <= 0: # E se a quantidade for zero (ou menor)
                    self.list.remove(item) # Ele remove o item e termina a iteração
                    return None
                self.list.remove(item) # Remove o produto e quebra a iteração
                break
        self.list.append(produto) # Adiciona o novo produto (ou atualiza)

    def venda(self,restaurante_pk): # Insira a venda no banco de dados
        valor_total = 0 
        for produto in self.list: # Para cada produto na lista
            total = (produto.preco * produto.quantidade)
            valor_total += total # adquire o valor e soma ao valor total
        self.database.executar("INSERT INTO venda(valor,pk_usuario,pk_restaurante) VALUES (?,?,?)",(valor_total,self.pk,restaurante_pk)) # Insere no banco de dados a venda
         
        result = self.database.consulta_pk_venda(self.pk) # Depois consulta a chave primária da venda
        pk_venda = result[0]

        for produto in self.list: # E gera uma relação venda-produto e insere no banco de dados no banco de dados  
            self.database.executar("INSERT INTO venda_produto(pk_venda,pk_produto,quantidade,valor_total) VALUES (?,?,?,?)",(pk_venda,produto.pk,produto.quantidade,produto.preco * produto.quantidade))

    def pedido_concluido(self,pk): # Tela de pedido concluido (nome,valor,quantidade e valor total da compra)
        Utils.limpar_tela()
        valor_total = 0 # Declara a variavel
        nome = self.database.consulta_restaurante_nome(pk) # Consulta o nome do restaurante
        print(f"Restaurante: {nome[0]}")
        print(f" {"_" * 81} ")
        print(f"|{" "* 81}|")
        print(f'|\033[38;2;58;105;198m{"Nome":^60s}\033[0m|\033[38;2;81;146;31m{"Valor":^9s}\033[0m|\033[38;2;186;25;203m{"Quantidade"}\033[0m|') # Printa as palavras "Nome" "Valor" e "Quantidade " com suas cores
        for produto in self.list: # Loop for para cada produto individual da lista
            print(f'|\033[38;2;58;105;198m{produto.nome:<60s}\033[0m|\033[38;2;81;146;31mR$ {produto.preco:<6.2f}\033[0m|\033[38;2;186;25;203m{produto.quantidade:<10d}\033[0m|')
            valor_total += (produto.preco * produto.quantidade) # Adiciona o valor do produto vezes a quantidade ao valor total
            time.sleep(0.09)
        print(f"|{"_" * 81}|")
        print(f"\nValor total: \033[38;2;81;146;31mR${valor_total:.2f}\033[0m\n") # printa o valor total
        
        input('Pressione <<ENTER>> para voltar para a tela dos restaurantes ') # Para finalizar é so apertar ente
        self.list = [] # Esvazia a lista
        return None
    
    def historico(self,historico): # Tela do histórico de compras
        index = 0 # Declara o index
        while True: # loop da função ocorre até o fim dela
            venda = historico[index] # a venda recebe a tupla do historico no index

            Utils.limpar_tela()
            
            restaurante = self.database.consulta_restaurante_nome(venda[3]) # Consulta o nome do restaurante da venda
            print(f"\033[31m{restaurante[0]:^111s}\033[0m\n")

            produtos = self.database.consulta_venda_produtos(venda[0]) # consulta os produtos da venda
            print(f" "+"_" * 100+" ")
            print(f"|"+" " * 100+"|")
            print(f'|\033[36m{"Nome":^60s}\033[0m|\033[32m{"Preço individual":^16s}\033[0m|\033[35m{"Quantidade":^10s}\033[0m|\033[94m{"Preço total":^11s}\033[0m|')
            for produto in produtos: # para cada produto em produto
                print(f'|\033[36m{produto[2]:<60s}\033[0m|\033[32m{produto[3]:<16.2f}\033[0m|\033[35m{produto[0]:<10d}\033[0m|\033[94mR$:{produto[1]:<8.2f}\033[0m|')
                time.sleep(0.08)
            print(f"|"+"_" * 100+"|")
            print(f"Valor total da compra: R${venda[1]:.2f} ")
            print(f"Data: {venda[2]}")
            
            print("\nA -- Anterior")
            print("P -- Próxima")
            print("Pressione <<ENTER>> para voltar para a tela dos restaurantes \n")
            while True:
                escolha = input("Digite a sua escolha: ")

                if escolha.upper() == "A": #Diminui o index em um
                    index -= 1
                    if index < 0: # caso o index tiver valor negativo
                        index = 0 # index vira 0
                    break
                elif escolha.upper() == "P": #Aumenta o index
                    index += 1
                    if index == len(historico): # Caso index seja do tamanho do histórico
                        index -= 1 # index subtrai um
                    break
                elif escolha == "": #Caso a escolha for apenas o enter a função termina
                    return None
                else:
                    continue

    @property #getters e setters
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self,dado : str):
        self.__nome = dado.title()

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self,dado : str):
        self.__email = dado.lower()

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, dado: str):
        self.__senha = dado

    @property
    def list(self):
        return self.__list
    
    @list.setter
    def list(self,dado):
        self.__list = dado
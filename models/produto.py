import re

class Produto:
    
    def __init__(self,database,restaurante): # recebe a Database e a chave primária do usuario(AKA restaurante)
        self.database = database
        self.restaurante = restaurante.pk
        
    def cadastrar(self): # cadastro do produto
        while True: # loop para o input
            self.nome = input("Digite o nome do produto: ")
            
            if len(self.nome) < 5:
                print("O nome do produto deve ter mais de 4 letras")
                continue
            elif re.search('[0-9]!@#$%ˆ&()_:.;\'\"\\/=_+-',self.nome) == True: # Qualquer coisa que não for A-Z ou a-z não passa
                print("Caractere inválido")
                continue
            else:
                break
            
        while True:
            self.preco = float(input("Digite o preço do produto: ")) # Resolve isso arthur
            
            if self.preco <= 0:
                print("O preço do produto deve ser maior do que 0")
                continue
            else:
                break
            
        sql = 'INSERT INTO produto(nome_produto,preco,pk_restaurante) VALUES (?,?,?);'
        tupla = (self.nome,self.preco,self.restaurante)
        self.database.executar(sql,tupla)
        
    def apagar(self,usuario): # Apaga o produto
        usuario.tabela_produto()
        

    @property #getters e setters
    def restaurante(self):
        return self.__restaurante
    
    @restaurante.setter
    def restaurante(self,dado : int):
        self.__restaurante = dado

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self,dado : str):
        self.__nome = dado
    
    @property
    def preco(self):
        return self.__preco
    
    @preco.setter
    def preco(self,dado : float):
        self.__preco = dado
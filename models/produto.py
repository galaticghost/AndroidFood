from utils.utils import Utils
import re
import time

class Produto:
    
    def __init__(self,database,restaurante): # recebe a Database e a chave primária do usuario(AKA restaurante)
        self.database = database
        self.restaurante = restaurante.pk
        
    def cadastrar(self): # cadastro do produto
        while True: # loop para o input
            self.nome = input("Digite o nome do produto: ") # Nome
            
            if len(self.nome) < 5:
                print("O nome do produto deve ter mais de 4 letras")
                continue
            elif len(self.nome) > 50:
                print("O nome do produto não pode ter mais de 50 caracteres")
                continue
            elif re.search('[^a-zA-Z ]',self.nome) == None: # Qualquer coisa que não for A-Z, a-z ou espaço não passa
                break
            else:
                print("Caractere inválido")
                continue
            
        while True: 
            try:
                self.preco = float(input("Digite o preço do produto: ")) #Preço do produto
            
                if self.preco <= 0:
                    print("O preço do produto deve ser maior do que 0")
                    continue
                else:
                    break
            except:
                print("O valor digitado não é um número")
                continue
            
        sql = 'INSERT INTO produto(nome_produto,preco,pk_restaurante) VALUES (?,?,?);' # Envia os dados para a database
        tupla = (self.nome,self.preco,self.restaurante)
        self.database.executar(sql,tupla)
        
    def apagar(self,usuario): # Apaga o produto
        if usuario.tabela_produto() == False:
            Utils.limpar_tela()
            print("Nenhum produto cadastrado!")
            time.sleep(2)
            return None
        
        while True:
            try:
                escolha = int(input("Digite o ID do produto que deseja apagar: "))
                if self.database.consulta_produto_restaurante(escolha,self.restaurante) == False: # verifica se o produto selecionado faz parte do restaurante
                    print(f"O produto com o ID {escolha} não existe")
                    continue
                else:
                    break
            except:
                print("Digite um número")
                continue
        
        self.database.executar('DELETE FROM produto WHERE pk_produto = ?',(escolha,)) # deleta o produto

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
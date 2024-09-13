import re

class Produto:
    
    def __init__(self,database,restaurante):
        self.database = database
        self.restaurante = restaurante.pk
        
    def cadastrar(self):
        while True:
            self.nome = input("Digite o nome do produto: ")
            
            if len(self.nome) < 5:
                print("O nome do produto deve ter mais de 4 letras")
                continue
            elif re.search('[0-9]!@#$%ˆ&()_:.;\'\"\\/=_+-',self.nome) == True:
                print("Caractere inválido")
                continue
            else:
                break
            
        while True:
            self.preco = float(input("Digite o preço do produto: "))
            
            if self.preco <= 0:
                print("O preço do produto deve ser maior do que 0")
                continue
            else:
                break
            
        sql = 'INSERT INTO produto(nome_produto,preco,pk_restaurante) VALUES (?,?,?);'
        tupla = (self.nome,self.preco,self.restaurante)
        self.database.executar(sql,tupla)
        
    def apagar():
        pass
    
    @classmethod
    def tabela_produto(self):
        result = self.database.consulta_produto(self.restaurante)
        if result == None:
            print("Nenhum produto cadastrado!")
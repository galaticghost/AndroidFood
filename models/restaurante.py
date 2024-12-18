import re
import hashlib
import time
from utils.utils import Utils

class Restaurante:
    
    def __init__(self,database,pk = None): # o restaurante recebe uma instancia de Database
        self.database = database
        self.pk = pk
    
    def cadastro(self):
        self.restaurante = Utils.verifica_restaurante_nome()
        
        self.comissao = Utils.verifica_comissao(self.database)

        self.email = Utils.verifica_email(self.database)
        
        self.senha = Utils.verifica_senha()
                
        sql = f'INSERT INTO restaurante(restaurante,comissao,email_restaurante,senha_restaurante) VALUES (?,?,?,?);'
        tupla = (self.restaurante,self.comissao,self.email,self.senha)   
        self.database.executar(sql,tupla)

    def login(self):
        
        self.email = input("Digite o seu email: ").lower().strip()
        self.senha = input("Digite a sua senha: ")
        self.senha = hashlib.md5(self.senha.encode())
        self.senha = self.senha.hexdigest()

        if self.database.consulta_login("restaurante",self.email,self.senha) == False: #consulta no banco se o login existe
            print("Usuário inválido")
            time.sleep(2)
            return False
        else:
            result = self.database.consulta_restaurante(self.email,self.senha) # lista com os atributos novos
            self.database.executar("UPDATE restaurante SET ultima_atualizacao = datetime('now','localtime') WHERE email_restaurante = ? AND senha_restaurante = ?",(self.email,self.senha)) # atualiza a data do ultimo login
            
            self.pk = result[0]
            self.restaurante = result[1]
            self.comissao = result[2]
            self.acesso = result[3]
            
            return True
    
    def alterar_comissao(self): # altera o valor da comissao
        print(f"O valor atual da comissão é {self.comissao}")
        while True: # loop para input
            try: # try e except para evitar erros grotescos(valueError)
                comissao = int(input("Digite o novo valor: "))
            
                if comissao < 0 or comissao > 100:
                    print("Valor Inválido!")
                    continue
                else:
                    self.database.executar('UPDATE restaurante SET comissao = ? WHERE pk_restaurante = ? ',(comissao,self.pk)) # manda pra database
                    self.comissao = comissao # atualiza o atributo
                    break
            except:
                print("O valor digitado não é um número")
                continue
    
    def tabela_produto(self): # Mostra os produtos
        result = self.database.consulta_produto(self.pk) # Retorna os produtos
        if not result: # caso result esteja vazia
            print("Nenhum produto cadastrado!")
            return False
        else:
            print (f'|\033[31m{"ID":^6s}\033[0m|\033[36m{"Nome":^60s}\033[0m|\033[32m{"Preço":^10s}\033[0m') # printa id nome e preço
            for tupla in result: # para cada tupla 
                print (f'|\033[31m{tupla[0]:^6d}\033[0m|\033[36m{tupla[1]:<60s}\033[0m| \033[32mR$:{tupla[2]:<6.2f}\033[0m')
            return result
    
    def quantidade_produto(self): # mostra a quantidades de produtos cadastrados no banco na chave do restaurante
        quantidade_produtos = self.database.quantidade_produto(self.pk)
        print(f"Quantidade de produtos: {quantidade_produtos[0]}")
        
    def update_tem_produto(self,condicao): # Atualiza a coluna tem produtos
        if condicao == "cadastrar": # 1
            self.database.executar("UPDATE restaurante SET tem_produtos = ? WHERE pk_restaurante = ?",(1,self.pk))
            return None
        elif condicao == "apagar": # 0
            result = self.database.quantidade_produto(self.pk) # ve se tem produtos
            if result[0] is 0:
                self.database.executar("UPDATE restaurante SET tem_produtos = ? WHERE pk_restaurante = ?",(0,self.pk))
            return None
    
    @property # getters e setters
    def restaurante(self):
        return self.__restaurante
    
    @restaurante.setter
    def restaurante(self,dado: str):
        self.__restaurante = dado
        
    @property
    def comissao(self):
        return self.__comissao
    
    @comissao.setter
    def comissao(self,dado: int):
        self.__comissao = dado
        
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self,dado: str):
        dado = dado.lower()
        self.__email = dado
        
    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self,dado: str):
        self.__senha = dado
    
    @property
    def pk(self):
        return self.__pk
    
    @pk.setter
    def pk(self, dado: int):
        self.__pk = dado
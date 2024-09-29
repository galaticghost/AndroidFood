import re
import hashlib
import time

class Usuario:
    
    def __init__(self,database): # o usuario recebe uma instancia de Database
        self.database = database
    
    def cadastro(self):
        while True:
            self.restaurante = input("Digite o nome do seu restaurante: ").strip() # nome do restaurante
            
            if len(self.restaurante) <= 10:
                print("O nome do restaurante deve ter mais de 10 caracteres")
                continue
            
            elif len(self.restaurante) > 100:
                print("O nome do restaurante não deve ter mais de 100 caracteres")
            
            else:
                break

        while True:
            try: # try e except para evitar valueError
                comissao = self.database.consulta_comissao() # consulta a comissão
                if comissao: 
                    print(f"A maior comissão é {comissao[0]}")  # se tiver comissão ele printa isso na tela
                self.comissao = int(input("Digite o valor da comissão: ")) #Feitoria!
                if self.comissao < 0:
                    print("O valor da comissão deve ser igual ou maior que 0")
                    continue
                elif self.comissao > 100:
                    print("O valor da comissão não pode ser maior que 100")
                    continue
                else:
                    break
            except:
                print("O valor digitado não é um número")

        while True: # recebe e converte o email para lowercase
            self.email = input("Digite o seu email: ").lower().strip()

            if re.search(r"[\w]+@[\w]+[.][a-z]",self.email) == None: # verifica se o email é um email
                print("O email digitado não é valído")
                continue
            
            elif len(self.email) > 200:
                print("O email não deve ter mais que 200 caracteres")
                continue
            
            if self.database.consulta_coluna("email_usuario","usuario","email_usuario",self.email) == True: # verifica se o email ja existe na database
                print("O email já consta no banco de dados")
                continue
            else:
                break
                
        while True:
            self.senha = input("Digite a sua senha: ")
            # Checagem de senha
            if len(self.senha) < 5:
                print("Sua senha tem menos de 5 caracteres")
                continue
            
            elif len(self.senha) > 100:
                print("A senha não pode ter mais de 100 caracteres")
                continue
            
            elif re.search(r"[A-Z]",self.senha) == None:
                print("Sua senha não possui uma letra maiúscula")
                continue
            
            elif re.search(r"[a-z]",self.senha) == None:
                print("Sua senha não possui uma letra minúscula")
                continue
            
            elif re.search(r"[0-9]",self.senha) == None:
                print("Sua senha não possui nenhum número")
                continue
            #Se passar pelos testes
            else:
                self.senha = hashlib.md5(self.senha.encode())
                self.senha = self.senha.hexdigest()
                break
        
        sql = f'INSERT INTO usuario(restaurante,comissao,email_usuario,senha_usuario) VALUES (?,?,?,?);'
        tupla = (self.restaurante,self.comissao,self.email,self.senha)   
        self.database.executar(sql,tupla)

    def login(self):
        
        self.email = input("Digite o seu email: ").lower().strip()
        self.senha = input("Digite a sua senha: ")
        self.senha = hashlib.md5(self.senha.encode())
        self.senha = self.senha.hexdigest()

        if self.database.consulta_login(self.email,self.senha) == False: #consulta no banco se o login existe
            print("Usuário inválido")
            time.sleep(2)
            return False
        else:
            self.database.executar("UPDATE usuario SET ultima_atualizacao = datetime('now','localtime') WHERE email_usuario = ? AND senha_usuario = ?",(self.email,self.senha)) # atualiza a data do ultimo login
            result = self.database.consulta_usuario(self.email,self.senha) # lista com os atributos novos
            
            self.pk = result[0]
            self.restaurante = result[1]
            self.comissao = result[2]
            
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
                    self.database.executar('UPDATE usuario SET comissao = ? WHERE pk_usuario = ? ',(comissao,self.pk)) # manda pra database
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
            print (f"{"ID":^6s}|{"Nome":^60s}|{"Preço":^10s}") # printa id nome e preço
            for tupla in result: # para cada tupla 
                print (f"{tupla[0]:<6d}|{tupla[1]:<60s}| R$ {tupla[2]:<6.2f}")
            return True
    
    def quantidade_produto(self): # mostra a quantidades de produtos cadastrados no banco na chave do restaurante
        quantidade_produtos = self.database.quantidade_produto(self.pk)
        print(f"Quantidade de produtos: {quantidade_produtos[0]}")
    
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
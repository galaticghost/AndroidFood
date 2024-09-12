import re

class Usuario:
    
    def __init__(self,database):
        self.database = database
    
    def cadastro(self):
        while True:
            self.restaurante = input("Digite o nome do seu restaurante: ")
            if len(self.restaurante) <= 10:
                print("O nome do restaurante deve ter mais de 10 caracteres")
                continue
            else:
                break

        while True:
            self.comissao = int(input("Digite o valor da comissão: ")) #dá um jeito de melhorar isso aqui
            if self.comissao < 0:
                print("O valor da comissão deve ser igual ou maior que 0")
                continue
            else:
                break

        while True: # recebe e converte o email para lowercase
            self.email = input("Digite o seu email: ").lower()

            if re.search("[\w,]@[\w,].[a-z]",self.email) == None: # verifica se o email é um email
                print("O email digitado não é valído")
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
            
            elif re.search("[A-Z]",self.senha) == None:
                print("Sua senha não possui uma letra maiúscula")
                continue
            
            elif re.search("[a-z]",self.senha) == None:
                print("Sua senha não possui uma letra minúscula")
                continue
            
            elif re.search("[0-9]",self.senha) == None:
                print("Sua senha não possui nenhum número")
                continue
            #Se passar pelos testes
            else:
                 # Eu queria criptografar com hash mas nao deu
                break
        
        sql = f'INSERT INTO usuario(restaurante,comissao,email_usuario,senha_usuario) VALUES (?,?,?,?);'
        tupla = (self.restaurante,self.comissao,self.email,self.senha)   
        self.database.executar(sql,tupla)

    def login(self):
        
        self.email = input("Digite o seu email: ").lower()
        self.senha = input("Digite a sua senha: ")

        if self.database.consulta_login(self.email,self.senha) == False: #
            print("Usuário inválido")
            return False
        else:
            self.database.executar("UPDATE usuario SET ultima_atualizacao = datetime('now','localtime') WHERE email_usuario = ? AND senha_usuario = ?",(self.email,self.senha))
            result = self.database.consulta_usuario(self.email,self.senha)
            self.pk = result[0]
            self.restaurante = result[1]
            self.comissao = result[2]
            return True
    
    @property
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
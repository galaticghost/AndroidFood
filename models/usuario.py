import re

class Usuario:
    
    def __init__(self,database):
        self.database = database
    
    def cadastro(self):
        while True:
            self.__restaurante = input("Digite o nome do seu restaurante: ")
            if len(self.__restaurante) <= 10:
                print("O nome do restaurante deve ter mais de 10 letras")
                continue
            else:
                break

        while True:
            self.__comissao = int(input("Digite o valor da comissão: "))
            if self.__comissao < 0:
                print("O valor da comissão deve ser igual ou maior que 0")
                continue
            else:
                break

        while True:
            self.__email = input("Digite o seu email: ")
            self.__email.lower()
            
            if re.search("[\w]@[\w].[a-z]",self.__email):
                print("O email digitado não é valído")
                continue
            
            if self.database.consulta_coluna(self.__email) == True : # Aqui vai ter a checagem do email na database
                print("O email já consta no banco de dados")
                continue
            else:
                break
                
        while True:
            self.__senha = input("Digite a sua senha")
            # Checagem de senha
            if len(self.__senha) < 5:
                print("Sua senha tem menos de 5 caracteres")
                continue
            
            elif re.search("[A-Z]",self.__senha) == None:
                print("Sua senha não possui uma letra maiúscula")
                continue
            
            elif re.search("[a-z]",self.__senha) == None:
                print("Sua senha não possui uma letra minúscula")
                continue
            
            elif re.search("[0-9]",self.__senha) == None:
                print("Sua senha não possui nenhum número")
                continue
            #Se passar pelos testes
            else:
                self.__senha = hash(self.__senha) # Ela é criptografada
                break

    def login(self):
        self.__email = input("Digite o seu email: ")
        self.__senha = input("Digite a sua senha: ")
        
        if self.database.consulta_usuario() == False: # FAZER
            pass
        
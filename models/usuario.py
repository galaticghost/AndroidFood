import re

class Usuario:
    
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
            
            if 2 == 2:# Aqui vai ter a checagem do email na database
                print("O email já consta no banco de dados")
                continue
            else:
                break

        while True:
            self.__senha = input("Digite a sua senha")

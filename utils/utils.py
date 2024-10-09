import os
import re
import hashlib
from database.database import Database

class Utils():

    @staticmethod
    def limpar_tela(): # limpa tela
        os.system('cls' if os.name == 'nt' else 'clear')
        
    @staticmethod
    def verifica_restaurante_nome():
        while True:
            restaurante = input("Digite o nome do seu restaurante: ").strip() # nome do restaurante
            
            if len(restaurante) <= 10:
                print("O nome do restaurante deve ter mais de 10 caracteres")
                continue
            
            elif len(restaurante) > 100:
                print("O nome do restaurante não deve ter mais de 100 caracteres")
                continue
            else:
                return restaurante
            
    @staticmethod
    def verifica_comissao(database):
        while True:
            comissao = database.consulta_comissao() # consulta a comissão
            if comissao: 
                print(f"A maior comissão é {comissao[0]}")  # se tiver comissão ele printa isso na tela
                
            try: # try e except para evitar valueError
                comissao = int(input("Digite o valor da comissão: ")) #Feitoria!
                if comissao < 0:
                    print("O valor da comissão deve ser igual ou maior que 0")
                    continue
                elif comissao > 100:
                    print("O valor da comissão não pode ser maior que 100")
                    continue
                else:
                    return comissao
            except:
                print("O valor digitado não é um número")
                
    @staticmethod
    def verifica_email(database):
        while True: # recebe e converte o email para lowercase
            email = input("Digite o seu email: ").lower().strip()

            if re.search(r"[\w]+@[\w]+[.][a-z]",email) == None: # verifica se o email é um email
                print("O email digitado não é valído")
                continue
            
            elif len(email) > 200:
                print("O email não deve ter mais que 200 caracteres")
                continue
            
            if database.consulta_coluna("email_restaurante","restaurante","email_restaurante",email) == True: # verifica se o email ja existe na database
                print("O email já consta no banco de dados")
                continue
            else:
                return email
            
    @staticmethod
    def verifica_senha():
        while True:
            senha = input("Digite a sua senha: ")
            # Checagem de senha
            if len(senha) < 5:
                print("Sua senha tem menos de 5 caracteres")
                continue
            
            elif len(senha) > 100:
                print("A senha não pode ter mais de 100 caracteres")
                continue
            
            elif re.search(r"[A-Z]",senha) == None:
                print("Sua senha não possui uma letra maiúscula")
                continue
            
            elif re.search(r"[a-z]",senha) == None:
                print("Sua senha não possui uma letra minúscula")
                continue
            
            elif re.search(r"[0-9]",senha) == None:
                print("Sua senha não possui nenhum número")
                continue
            #Se passar pelos testes
            else:
                senha = hashlib.md5(senha.encode())
                senha = senha.hexdigest()
                return senha        
    
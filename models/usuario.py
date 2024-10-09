import hashlib
import time
from utils.utils import Utils

class Usuario():
    
    def __init__(self,database):
        self.database = database
        
    def cadastro(self):
        
        self.nome = Utils.verifica_nome_completo()
        self.email = Utils.verifica_email(self.database)
        self.senha = Utils.verifica_senha()

        self.database.executar("INSERT INTO usuario(nome_usuario,email_usuario,senha_usuario) VALUES (?,?,?)",(self.nome,self.email,self.senha))

    def login(self):
        
        self.email = input("Digite o seu email: ").lower().strip()
        self.senha = input("Digite a sua senha: ")
        self.senha = hashlib.md5(self.senha.encode())
        self.senha = self.senha.hexdigest()

        if self.database.consulta_login("usuario",self.email,self.senha) == False: #consulta no banco se o login existe
            print("Usuário inválido")
            time.sleep(2)
            return False
        else:
            self.database.executar("UPDATE usuario SET ultima_atualizacao = datetime('now','localtime') WHERE email_usuario = ? AND senha_usuario = ?",(self.email,self.senha)) # atualiza a data do ultimo login
            result = self.database.consulta_usuario(self.email,self.senha) # lista com os atributos novos
            
            self.pk = result[0]
            self.nome = result[1]
            
            return True

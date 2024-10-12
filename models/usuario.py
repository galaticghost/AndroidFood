import hashlib
import time
from utils.utils import Utils

class Usuario():
    
    def __init__(self,database):
        self.database = database
        self.__list = []
        
    def __str__(self):
        return f"{self.pk},{self.nome},{self.email},{self.senha}"
        
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

    def lista(self,produto):
        for item in self.list:
            if item.pk == produto.pk:
                if produto.quantidade == 0:
                    self.list.remove(item)
                    return None
                self.list.remove(item)
                break
        self.list.append(produto)

    def venda(self):
        valor_total = 0
        for produto in self.list:
            total = (produto.preco * produto.quantidade)
            valor_total += total
        self.database.executar("INSERT INTO venda(valor,pk_usuario) VALUES (?,?)",(valor_total,self.pk))
        
        result = self.database.consulta_pk_venda(self.pk)
        pk_venda = result[0]

        for produto in self.list:
            self.database.executar("INSERT INTO venda_produto(pk_venda,pk_produto,quantidade,valor_total) VALUES (?,?,?,?)",(pk_venda,produto.pk,produto.quantidade,produto.preco * produto.quantidade))

    def pedido_concluido(self):
        pass

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self,dado : str):
        self.__nome = dado.title()

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self,dado : str):
        self.__email = dado.lower()

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, dado: str):
        self.__senha = dado

    @property
    def list(self):
        return self.__list
    
    @list.setter
    def list(self,dado):
        self.__list = dado
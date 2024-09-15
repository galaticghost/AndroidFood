import sqlite3

class Database:
    
    def __init__(self): # Recebe uma conexao
        self.conexao = sqlite3.connect("androidfood.db")

    def consulta_login(self,email,senha): # chegagem para o login
        sql = 'SELECT email_usuario,senha_usuario FROM usuario WHERE email_usuario = ? AND senha_usuario = ?;' # comando sql
        result = self.conexao.execute(sql,(email,senha)) # result recebe os resultados da query
        if result.fetchone() == None: # EU ODEIO ESSE FETCHONE. Caso result esteje vazio ele retorna falso 
            return False
        else:
            return True
        
    def consulta_usuario(self,email,senha): # consulta do login
        sql = 'SELECT * FROM usuario WHERE email_usuario = ? AND senha_usuario = ?'
        result = self.conexao.execute(sql,(email,senha))
        return result.fetchone()
    
    def consulta_produto(self,restaurante): # consulta do produto
        sql = 'SELECT pk_produto,nome_produto,preco FROM produto WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(restaurante,))
        return result.fetchall()
    
    def consulta_coluna(self,coluna,tabela,coluna_comparador,item): # eu aprendi parametros do sql por meio desse codigo. eu odeio esse codigo
        sql = f'SELECT {coluna} FROM {tabela} WHERE {coluna_comparador} = ?;' # comando sql
        result = self.conexao.execute(sql,(item,)) # result recebe os resultados da query
        if result.fetchone() == None:
            return False
        else:
            return True

    def executar(self,sql,tupla): # É só um execute com commit
        self.conexao.execute(sql,tupla)
        self.conexao.commit()
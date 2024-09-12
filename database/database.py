import sqlite3

class Database:
    
    def __init__(self):
        self.conexao = sqlite3.connect("androidfood.db")

    def consulta_login(self,email,senha): # chegagem para o login
        sql = 'SELECT email_usuario,senha_usuario FROM usuario WHERE email_usuario = ? AND senha_usuario = ?;'
        result = self.conexao.execute(sql,(email,senha))
        if result.fetchone() == None: # EU ODEIO ESSE FETCHONE 
            return False
        else:
            return True
        
    def consulta_usuario(self,email,senha):
        sql = 'SELECT * FROM usuario WHERE email_usuario = ? AND senha_usuario = ?'
        result = self.conexao.execute(sql,(email,senha))
        return result.fetchone()
    
    def consulta_coluna(self,coluna,tabela,coluna_comparador,item): # eu aprendi parametros do sql por meio desse codigo. eu odeio esse codigo
        sql = f'SELECT {coluna} FROM {tabela} WHERE {coluna_comparador} = ?;'
        result = self.conexao.execute(sql,(item,))
        if result.fetchone() == None:
            return False
        else:
            return True

    def executar(self,sql,tupla):
        self.conexao.execute(sql,tupla)
        self.conexao.commit()
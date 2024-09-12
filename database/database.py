import sqlite3

class Database:
    
    def __init__(self):
        self.conexao = sqlite3.connect("androidfood.db")

    def consulta_usuario(self,email,senha): # chegagem para o login
        sql = 'SELECT email_restaurante,senha_restaurante FROM restaurante WHERE email_restaurante = ? AND senha_restaurante = ?;'
        result = self.conexao.execute(sql,(email,senha))
        if result.fetchone() == None: # EU ODEIO ESSE FETCHONE 
            return False
        else:
            return True
        
    def consulta_completa(self,email,senha):
        sql = 'SELECT * FROM restaurante WHERE email_restaurante = ? AND senha_restaurante = ?'
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
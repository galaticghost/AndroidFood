import sqlite3

class Database:
    
    def __init__(self):
        self.conexao = sqlite3.connect("androidfood.db")

    def consulta_usuario(self,email,senha):
        pass
    
    def consulta_coluna(self,coluna,tabela,coluna_comparador,item): # eu aprendi parametros por meio desse codigo. eu odeio esse codigo
        sql = f'SELECT {coluna} FROM {tabela} WHERE {coluna_comparador} = ?;'
        result = self.conexao.execute(sql,(item,))
        if result.fetchone() == None:
            return False
        else:
            return True

    def inserir(self,nome,comissao,email,senha):
        sql = f'INSERT INTO restaurante(pk_restaurante,nome_restaurante,comissao,email_restaurante,senha_restaurante) VALUES (2,?,?,?,?);'
        self.conexao.execute(sql,(nome,comissao,email,senha))
        self.conexao.commit()

    def deletar(self):
        pass

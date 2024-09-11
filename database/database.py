import sqlite3

class Database:
    
    def __init__(self):
        self.conexao = sqlite3.connect("androidfood.db")

    def consulta_usuario(self,email,senha):
        pass
    
    def consulta_coluna(self,coluna,tabela):
        sql = "SELECT nome_restaurante FROM restaurante;"
        result = self.conexao.execute(sql)
        return result
        
    def inserir(self):
        pass
    
    def deletar(self):
        pass
    
xina = Database()
print(xina.consulta_coluna("nome_restaurante","restaurante"))
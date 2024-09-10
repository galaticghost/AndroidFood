import sqlite3

class Database:
    
    def __init__(self):
        self.conexao = sqlite3.connect("androidfood.db")

    def consulta_usuario(self,email): # Nota pra si mesmo: ARHTUR SEU FILHO DA PUTA, VOCE NAO COLOCOU LIMITE NO VARCHAR ENTAO PELO AMOR DE DEUS ALTERA ESSA PORRA
        pass
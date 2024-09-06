import sqlite3

class Conexao():
    
    def __init__(self):
        self._conexao = sqlite3.connect("../androidfood.db")
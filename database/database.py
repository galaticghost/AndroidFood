import sqlite3

class Database:
    
    def __init__(self): # Recebe uma conexão e cria as tabelas se elas não existirem
        self.conexao = sqlite3.connect("androidfood.db")
        self.conexao.execute('''CREATE TABLE IF NOT EXISTS usuario (
                            pk_usuario INTEGER PRIMARY KEY NOT NULL,
                                restaurante VARCHAR(100) NOT NULL,
                                comissao INTEGER CHECK (comissao >= 0) NOT NULL,
                                email_usuario VARCHAR(200) NOT NULL,
                                senha_usuario VARCHAR(100) NOT NULL,
                                criacao DATE DEFAULT (datetime('now', 'localtime')),
                                ultima_atualizacao DATE DEFAULT (datetime('now', 'localtime'))
                        );''')
        self.conexao.execute('''CREATE TABLE IF NOT EXISTS produto (
                        pk_produto INTEGER PRIMARY KEY,
                        nome_produto VARCHAR(100) NOT NULL,
                        preco FLOAT CHECK (preco >= 0.01) NOT NULL,
                        pk_restaurante INTEGER REFERENCES usuario
                    );''')
        self.conexao.commit

    def consulta_comissao(self): # Consulta a maior comissao e retorna ela
        result = self.conexao.execute('SELECT comissao FROM usuario ORDER BY comissao DESC LIMIT 1')
        return result.fetchone()
    
    def consulta_login(self,email,senha): # chegagem para o login
        sql = 'SELECT email_usuario,senha_usuario FROM usuario WHERE email_usuario = ? AND senha_usuario = ?;' # comando sql
        result = self.conexao.execute(sql,(email,senha)) # result recebe os resultados da query
        if result.fetchone() == None: # EU ODEIO ESSE FETCHONE. Caso result esteje vazio ele retorna falso 
            return False
        else:
            return True
        
    def consulta_usuario(self,email,senha): # consulta do login
        sql = 'SELECT pk_usuario,restaurante,comissao,email_usuario,senha_usuario FROM usuario WHERE email_usuario = ? AND senha_usuario = ?'
        result = self.conexao.execute(sql,(email,senha))
        return result.fetchone()
    
    def consulta_produto(self,restaurante): # consulta do produto
        sql = 'SELECT pk_produto,nome_produto,preco FROM produto WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(restaurante,))
        return result.fetchall()
    
    def consulta_produto_restaurante(self,pk_produto,pk_restaurante): # consulta se o produto existe naquele restaurante
        sql = 'SELECT pk_produto FROM produto WHERE pk_produto = ? AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk_produto,pk_restaurante))
        if not result.fetchone():
            return False
        else:
            return True
    
    def consulta_coluna(self,coluna,tabela,coluna_comparador,item): # eu aprendi parametros do sql por meio desse codigo. eu odeio esse codigo
        sql = f'SELECT {coluna} FROM {tabela} WHERE {coluna_comparador} = ?;' # comando sql
        result = self.conexao.execute(sql,(item,)) # result recebe os resultados da query
        if result.fetchone() == None:
            return False
        else:
            return True
    
    def quantidade_produto(self,pk): # retorna a quantidade de produtos (cada linha da tabela) onde a pk for igual a pk do usuario
        sql = f'SELECT COUNT() FROM produto WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()

    def executar(self,sql,tupla): # É só um execute com commit
        self.conexao.execute(sql,tupla)
        self.conexao.commit()
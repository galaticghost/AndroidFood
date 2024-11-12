import sqlite3

class Database:
    
    def __init__(self): # Recebe uma conexão e cria as tabelas se elas não existirem
        self.conexao = sqlite3.connect("androidfood.db")
        self.conexao.execute('''CREATE TABLE IF NOT EXISTS restaurante (
                            pk_restaurante INTEGER PRIMARY KEY NOT NULL,
                                restaurante VARCHAR(100) NOT NULL,
                                comissao INTEGER CHECK (comissao >= 0) NOT NULL,
                                email_restaurante VARCHAR(200) NOT NULL,
                                senha_restaurante VARCHAR(100) NOT NULL,
                                criacao DATE DEFAULT (datetime('now', 'localtime')),
                                ultima_atualizacao DATE DEFAULT (datetime('now', 'localtime')),
                                tem_produtos bool DEFAULT 0
                            );''')
        self.conexao.execute('''CREATE TABLE IF NOT EXISTS produto (
                            pk_produto INTEGER PRIMARY KEY,
                            nome_produto VARCHAR(100) NOT NULL,
                            preco NUMERIC CHECK (preco > 0) NOT NULL,
                            pk_restaurante INTEGER REFERENCES restaurante NOT NULL
                            );''')
        self.conexao.execute('''CREATE TABLE IF NOT EXISTS usuario(
                            pk_usuario INTEGER PRIMARY KEY NOT NULL,
                            nome_usuario VARCHAR(200) NOT NULL,
                            email_usuario VARCHAR(200) NOT NULL,
                            senha_usuario VARCHAR(100) NOT NULL,
                            criacao DATE DEFAULT (datetime('now', 'localtime')),
                            ultima_atualizacao DATE DEFAULT (datetime('now', 'localtime'))
                            );''')
        self.conexao.execute('''CREATE TABLE IF NOT EXISTS venda(
                            pk_venda INTEGER PRIMARY KEY NOT NULL,
                            valor NUMERIC CHECK (valor > 0) NOT NULL,
                            pk_usuario INTEGER REFERENCES usuario NOT NULL,
                            pk_restaurante INTEGER REFERENCES restaurante NOT NULL,
                            criacao DATE DEFAULT(datetime('now', 'localtime')),
                            status VARCHAR(50)
                            );''')
        self.conexao.execute('''CREATE TABLE IF NOT EXISTS venda_produto(
                            pk_venda_produto INTEGER PRIMARY KEY NOT NULL,
                            pk_venda INTEGER REFERENCES venda NOT NULL,
                            pk_produto INTEGER REFERENCES produto NOT NULL,
                            quantidade INTEGER NOT NULL,
                            valor_total NUMERIC CHECK(valor_total > 0) NOT NULL
                            );''')
        self.conexao.commit

    def __str__(self):
        return f"{self.conexao}"

    def consulta_comissao(self): # Consulta a maior comissao e retorna ela
        result = self.conexao.execute('SELECT comissao FROM restaurante ORDER BY comissao DESC LIMIT 1')
        return result.fetchone()
    
    def consulta_login(self,tabela,email,senha): # chegagem para o login
        sql = f'SELECT email_{tabela},senha_{tabela} FROM {tabela} WHERE email_{tabela} = ? AND senha_{tabela} = ?;' # comando sql
        result = self.conexao.execute(sql,(email,senha)) # result recebe os resultados da query
        if result.fetchone() == None: #Caso result esteje vazio ele retorna falso 
            return False
        else:
            return True
        
    def consulta_restaurante_nome(self,pk): # Consulta o nome do restaurante
        sql = 'SELECT restaurante FROM restaurante WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
        
    def consulta_restaurante(self,email,senha): # consulta do login do restaurante
        sql = 'SELECT pk_restaurante,restaurante,comissao,ultima_atualizacao FROM restaurante WHERE email_restaurante = ? AND senha_restaurante = ?'
        result = self.conexao.execute(sql,(email,senha))
        return result.fetchone()
    
    def consulta_usuario(self,email,senha): # consulta do login do usuario
        sql = 'SELECT pk_usuario,nome_usuario,ultima_atualizacao FROM usuario WHERE email_usuario = ? AND senha_usuario = ?'
        result = self.conexao.execute(sql,(email,senha))
        return result.fetchone()
    
    def consulta_produto(self,pk_restaurante): # consulta os produtos de um restaurante
        sql = 'SELECT pk_produto,nome_produto,preco FROM produto WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk_restaurante,))
        return result.fetchall()
    
    def consulta_produto_one(self,pk_restaurante,pk_produto): # consulta um único produto
        sql = 'SELECT nome_produto,preco FROM produto WHERE pk_restaurante = ? AND pk_produto = ?;'
        result = self.conexao.execute(sql,(pk_restaurante,pk_produto))
        return result.fetchone()
    
    def consulta_produto_restaurante(self,pk_produto,pk_restaurante): # consulta se o produto existe naquele restaurante
        sql = 'SELECT pk_produto FROM produto WHERE pk_produto = ? AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk_produto,pk_restaurante))
        if not result.fetchone():
            return False
        else:
            return True
    
    def consulta_coluna(self,coluna,tabela,coluna_comparador,item): # Consulta uma coluna de uma tabela
        sql = f'SELECT {coluna} FROM {tabela} WHERE {coluna_comparador} = ?;' # comando sql
        result = self.conexao.execute(sql,(item,)) # result recebe os resultados da query
        if result.fetchone() == None:
            return False
        else:
            return True
        
    def consulta_pk_venda(self,pk): # Consulta o pk da venda mais recente feita pelo usuario
        sql = 'SELECT pk_venda FROM venda WHERE pk_usuario = ? ORDER BY criacao DESC LIMIT 1;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()

    def consulta_venda(self,pk): # Consulta as compras de um usuario ordenado da ultima a primeira
        sql = f'SELECT pk_venda,valor,criacao,pk_restaurante FROM venda WHERE pk_usuario = ? ORDER BY pk_venda DESC;'
        result = self.conexao.execute(sql,(pk,))
        result = result.fetchall()
        if result is None:
            return False
        else:
            return result
        
    def consulta_venda_produtos(self,pk_venda): # Consulta a relação da venda_produto e os nomes e preços dos produtos relacionados
        sql = f'SELECT venda_produto.quantidade,venda_produto.valor_total,produto.nome_produto,produto.preco FROM venda_produto INNER JOIN produto ON venda_produto.pk_produto = produto.pk_produto WHERE pk_venda = ?'
        result = self.conexao.execute(sql,(pk_venda,))
        return result.fetchall()

    def quantidade_produto(self,pk): # retorna a quantidade de produtos (cada linha da tabela) onde a pk for igual a pk do restaurante
        sql = 'SELECT COUNT() FROM produto WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def consulta_restaurante_lista(self): # retorna a pk e o nome do restaurante que tenham pelo menos um produto cadastrado por ordem decrescente da comissao 
        sql = 'SELECT pk_restaurante,restaurante FROM restaurante WHERE tem_produtos = 1 ORDER BY comissao DESC;'
        result = self.conexao.execute(sql)
        result = result.fetchall()
        if not result:
            return False
        else:
            return result

    def executar(self,sql,tupla): # É só um execute com commit
        self.conexao.execute(sql,tupla)
        self.conexao.commit()
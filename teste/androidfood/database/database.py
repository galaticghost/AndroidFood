import sqlite3

class Database:
    
    def __init__(self): # Recebe uma conexão e cria as tabelas se elas não existirem
        self.conexao = sqlite3.connect("androidfood.db",check_same_thread=False)
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
                            status VARCHAR(50) DEFAULT "criado"
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
        
    def consulta_status(self,pk,pk_restaurante):
        sql = f'SELECT status FROM venda WHERE pk_venda = ? AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,pk_restaurante))
        result = result.fetchone()
        match(result[0]):
            case 'aceito':
                return 'aceito'
            case 'criado':
                return 'criado'
            case 'rejeitado':
                return 'rejeitado'
            case 'saiu para a entrega':
                return 'saiu para a entrega'
            case 'entregue':
                return 'entregue'

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
        
    def consulta_pedidos(self,pk_restaurante):
        sql = f'SELECT pk_venda,valor,pk_usuario,criacao,status FROM venda WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk_restaurante,))
        return result.fetchall()
        
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
        
    def consulta_media_gasto(self,pk):
        sql = f'SELECT AVG(valor) FROM venda WHERE pk_restaurante = ? GROUP BY pk_usuario;'
        result = self.conexao.execute(sql,(pk,))
        result = result.fetchall()
        if not result:
            return False
        else:
            return result
        
    def consulta_maior_compra(self,pk):
        sql = f'SELECT pk_venda,MAX(valor),pk_usuario,pk_restaurante,criacao,status FROM venda WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        result = result.fetchall()
        if not result:
            return False
        else:
            return result
        
    def consulta_maior_quantidade(self,pk):
        sql = '''SELECT vp.pk_venda,SUM(quantidade) FROM venda_produto vp 
            INNER JOIN venda v ON v.pk_venda = vp.pk_venda 
            WHERE v.pk_restaurante = ?
            GROUP BY vp.pk_venda ORDER BY SUM(quantidade) DESC'''
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def consulta_maior_comissao(self):
        sql = f'SELECT pk_restaurante,restaurante,MAX(comissao),email_restaurante,senha_restaurante,criacao,ultima_atualizacao,tem_produtos FROM restaurante'
        result = self.conexao.execute(sql)
        return result.fetchone()

    def consulta_menor_comissao(self):
        sql = f'SELECT pk_restaurante,restaurante,MIN(comissao),email_restaurante,senha_restaurante,criacao,ultima_atualizacao,tem_produtos FROM restaurante'
        result = self.conexao.execute(sql)
        return result.fetchone()

    def consulta_mais_pedido(self,pk):
        sql = '''SELECT *,COUNT(pk_produto) FROM venda_produto vp
        INNER JOIN venda v ON v.pk_venda = vp.pk_venda 
        WHERE pk_restaurante = ?
        GROUP BY pk_produto ORDER BY COUNT(pk_produto) DESC LIMIT 1''' # TODO
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def status_criado(self,pk):
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "criado" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def status_aceito(self,pk):
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "aceito" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def status_rejeitado(self,pk):
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "rejeitado" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()

    def status_saiu_entrega(self,pk):
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "saiu para entrega" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def status_entregue(self,pk):
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "entregue" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def consulta_status_venda(self,pk):
        criado = self.status_criado(pk)
        aceito = self.status_aceito(pk)
        rejeitado = self.status_rejeitado(pk)
        saiu_entrega = self.status_saiu_entrega(pk)
        entregue = self.status_entregue(pk)
        
        status = {
            "criado":criado[0],
            "aceito":aceito[0],
            "rejeitado":rejeitado[0],
            "saiu_entrega":saiu_entrega[0],
            "entregue":entregue[0]
            }
        
        return status
    
    def relatorio(self,pk):
        media_gasto = self.consulta_media_gasto(pk)
        maior_compra = self.consulta_maior_compra(pk)
        mais_pedido = self.consulta_mais_pedido(pk)
        maior_quantidade = self.consulta_maior_quantidade(pk)
        status = self.consulta_status_venda(pk)
        
        consultas = {
            "media_gasto":media_gasto[0],
            "maior_compra":maior_compra[0],
            "mais_pedido":mais_pedido[0],
            "maior_quantidade":maior_quantidade[0],
            "criado":status["criado"],
            "aceito":status["aceito"],
            "rejeitado":status["rejeitado"],
            "saiu_entrega":status["saiu_entrega"],
            "entregue":status["entregue"]
        }
        
        return consultas

    def executar(self,sql,tupla): # É só um execute com commit
        self.conexao.execute(sql,tupla)
        self.conexao.commit()
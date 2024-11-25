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
                            ultima_atualizacao DATE DEFAULT (datetime('now', 'localtime')),
                            admin BOOLEAN NOT NULL DEFAULT 0 
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
        if self.check_admin() == False:
            self.conexao.execute("INSERT INTO usuario(nome_usuario,email_usuario,senha_usuario,admin) VALUES ('admin','admin@androidfood.com','274672838a8002344fed81ca1228bf05',1)") # a senha é 123aA, login padrao do admin TODO
        self.conexao.commit

    def __str__(self):
        return f"{self.conexao}"
    
    def check_admin(self):
        sql = f'SELECT 1 FROM usuario WHERE admin = 1;'
        result = self.conexao.execute(sql)
        if result.fetchone() == None:
            return False
        else:
            return True

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
        
    def consulta_admin(self,email,senha):
        sql = f'SELECT admin FROM usuario WHERE email_usuario = ? AND senha_usuario = ?;'
        result = self.conexao.execute(sql,(email,senha))
        result = result.fetchone()
        return result[0]
    
    def consulta_restaurante_produtos(self,pk):
        sql = f'SELECT COUNT(1) FROM venda WHERE pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        if result.fetchone()[0] == 0:
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
        
    def consulta_status(self,pk,pk_restaurante): # Consulta o status do pedido 
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
        
    def consulta_pedidos(self,pk_restaurante): # Consulta os pedidos de um restaurante
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
        
    def consulta_media_gasto(self,pk): # Consulta a média do valor que cada usuario gasta no restaurante
        sql = '''SELECT AVG(valor),u.nome_usuario FROM venda v
                INNER JOIN usuario u ON u.pk_usuario = v.pk_usuario
                WHERE pk_restaurante = ? GROUP BY v.pk_usuario;'''
        result = self.conexao.execute(sql,(pk,))
        result = result.fetchall()
        if not result:
            return False
        else:
            return result
        
    def consulta_maior_compra(self,pk): # Consulta o nome do usuario que fez a maior compra(valor) e o valor de um restaurante específico
        sql = '''SELECT u.nome_usuario,MAX(valor) FROM venda v
                INNER JOIN usuario u ON u.pk_usuario = v.pk_usuario
                WHERE pk_restaurante = ?;'''
        result = self.conexao.execute(sql,(pk,))
        result = result.fetchone()
        if not result:
            return False
        else:
            return result
        
    def consulta_maior_quantidade(self,pk): # Consulta a compra com a maior quantidade de itens
        sql = '''SELECT vp.pk_venda,SUM(quantidade) FROM venda_produto vp 
            INNER JOIN venda v ON v.pk_venda = vp.pk_venda 
            WHERE v.pk_restaurante = ?
            GROUP BY vp.pk_venda ORDER BY SUM(quantidade) DESC LIMIT 1'''
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def consulta_maior_comissao(self): # Consulta o restaurante com a maior comissao
        sql = f'SELECT pk_restaurante,restaurante,MAX(comissao),email_restaurante,senha_restaurante,criacao,ultima_atualizacao,tem_produtos FROM restaurante'
        result = self.conexao.execute(sql)
        return result.fetchone()

    def consulta_menor_comissao(self): # Consulta o restaurante com a menor comissao
        sql = f'SELECT pk_restaurante,restaurante,MIN(comissao),email_restaurante,senha_restaurante,criacao,ultima_atualizacao,tem_produtos FROM restaurante'
        result = self.conexao.execute(sql)
        return result.fetchone()
    
    def consulta_soma_valores(self):
        sql = '''SELECT SUM(valor), r.restaurante FROM venda v
        INNER JOIN restaurante r ON v.pk_restaurante = r.pk_restaurante 
        GROUP BY v.pk_restaurante ORDER BY SUM(valor) DESC'''
        result = self.conexao.execute(sql)
        return result.fetchall()

    def consulta_mais_pedido(self,pk): # Consulta o item mais pedido de um restaurante específico
        sql = '''SELECT p.nome_produto,COUNT(vp.pk_produto) FROM venda_produto vp
        INNER JOIN venda v ON v.pk_venda = vp.pk_venda
        INNER JOIN produto p ON p.pk_produto = vp.pk_produto
        WHERE v.pk_restaurante = ?
        GROUP BY vp.pk_produto ORDER BY COUNT(vp.pk_produto) DESC LIMIT 1'''
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def status_criado(self,pk): # Consulta a quantidade de pedidos com o status "Criado"
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "criado" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def status_aceito(self,pk): # Consulta a quantidade de pedidos com o status "Aceito"
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "aceito" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def status_rejeitado(self,pk): # Consulta a quantidade de pedidos com o status "Rejeitado"
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "rejeitado" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()

    def status_saiu_entrega(self,pk): # Consulta a quantidade de pedidos com o status "Saiu para a entrega"
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "saiu para entrega" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def status_entregue(self,pk): # Consulta a quantidade de pedidos com o status "Entregue"
        sql = f'SELECT COUNT(status) FROM venda v WHERE status = "entregue" AND pk_restaurante = ?;'
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
    
    def consulta_media_meses(self,pk): # TODO
        sql = '''SELECT 
                COUNT(CASE WHEN strftime('%w',criacao) = '0' THEN pk_venda ELSE NULL END) AS 'Domingo',
                COUNT(CASE WHEN strftime('%w',criacao) = '1' THEN pk_venda ELSE NULL END) AS 'Segunda',
                COUNT(CASE WHEN strftime('%w',criacao) = '2' THEN pk_venda ELSE NULL END) AS 'Terça',
                COUNT(CASE WHEN strftime('%w',criacao) = '3' THEN pk_venda ELSE NULL END) AS 'Quarta',
                COUNT(CASE WHEN strftime('%w',criacao) = '4' THEN pk_venda ELSE NULL END) AS 'Quinta',
                COUNT(CASE WHEN strftime('%w',criacao) = '5' THEN pk_venda ELSE NULL END) AS 'Sexta',
                COUNT(CASE WHEN strftime('%w',criacao) = '6' THEN pk_venda ELSE NULL END) AS 'Sábado'
            FROM venda v WHERE pk_restaurante = ?;'''
        result = self.conexao.execute(sql,(pk,))
        return result.fetchone()
            
    def consulta_quantidade_usuario_restaurante(self): # Consulta quantos restaurantes e usuarios estão cadastrados na database"
        sql = f"SELECT (SELECT COUNT(1) FROM restaurante r) AS 'restaurante', (SELECT COUNT(1) FROM usuario u WHERE admin = 0) AS 'Usuario';"
        result = self.conexao.execute(sql)
        return result.fetchone()
    
    def consulta_valor_medio_pedido(self): # Consulta a média do ganhos de cada restaurante
        sql = '''SELECT AVG(valor), r.restaurante FROM venda
                RIGHT JOIN restaurante r  ON venda.pk_restaurante  = r.pk_restaurante 
                GROUP BY r.pk_restaurante;'''
        result = self.conexao.execute(sql)
        result = result.fetchall()
        if not result:
            return False
        return result
    
    def consulta_pedido_mes_restaurante(self): # Consulta a quantidade de pedidos de cada mês de todos os restaurantes
        sql = '''SELECT
        COUNT(CASE WHEN strftime('%m', v.criacao) = '1' THEN 1 ELSE NULL END) AS 'janeiro',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '2' THEN 1 ELSE NULL END) AS 'fevereiro',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '3' THEN 1 ELSE NULL END) AS 'março',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '4' THEN 1 ELSE NULL END) AS 'abril',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '5' THEN 1 ELSE NULL END) AS 'maio',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '6' THEN 1 ELSE NULL END) AS 'junho',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '7' THEN 1 ELSE NULL END) AS 'julho',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '8' THEN 1 ELSE NULL END) AS 'agosto',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '9' THEN 1 ELSE NULL END) AS 'setembro',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '10' THEN 1 ELSE NULL END) AS 'outubro',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '11' THEN 1 ELSE NULL END) AS 'novembro',
        COUNT(CASE WHEN strftime('%m', v.criacao) = '12' THEN 1 ELSE NULL END) AS 'dezembro',
        r.restaurante 
        FROM venda v
        RIGHT JOIN restaurante r ON r.pk_restaurante = v.pk_restaurante 
        GROUP BY r.pk_restaurante ;'''
        result = self.conexao.execute(sql)
        return result.fetchall()
    
    def consulta_restaurantes(self):
        sql = f'SELECT pk_restaurante, restaurante FROM restaurante'
        result = self.conexao.execute(sql)
        if not result:
            return False
        return result.fetchall()
    
    def consulta_pedidos_unico(self): # Consulta usuarios unicos em cada restaurante
        sql = '''SELECT r.restaurante, COUNT(DISTINCT pk_usuario) as 'usuarios' FROM venda v
                RIGHT JOIN restaurante r ON v.pk_restaurante = r.pk_restaurante 
                GROUP BY r.pk_restaurante ;'''
        result = self.conexao.execute(sql)
        result = result.fetchall()
        if not result:
            return False
        return result
    
    def consulta_status_venda(self,pk): # Executa as consultas da venda, cria um dicionario e retorna
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
    
    def relatorio(self,pk): # Executa o relatório para o restaurante
        if self.consulta_restaurante_produtos(pk) == False:
            return {"check":False}
        media_gasto = self.consulta_media_gasto(pk)
        maior_compra = self.consulta_maior_compra(pk)
        mais_pedido = self.consulta_mais_pedido(pk)
        maior_quantidade = self.consulta_maior_quantidade(pk)
        status = self.consulta_status_venda(pk)
        media_meses = self.consulta_media_meses(pk)
        
        consultas = {
            "media_gasto":media_gasto,
            "maior_compra":maior_compra,
            "mais_pedido":mais_pedido,
            "maior_quantidade":maior_quantidade,
            "criado":status["criado"],
            "aceito":status["aceito"],
            "rejeitado":status["rejeitado"],
            "saiu_entrega":status["saiu_entrega"],
            "entregue":status["entregue"],
            "media_meses":media_meses
        }

        return consultas
    
    def relatorio_administrativo(self): # Executa o relatório para o administrador
        quantidade_res_usu = self.consulta_quantidade_usuario_restaurante()
        valor_medio = self.consulta_valor_medio_pedido()
        pedido_mes = self.consulta_pedido_mes_restaurante()
        usuario_unico = self.consulta_pedidos_unico()
        maior_comissao = self.consulta_maior_comissao()
        menor_comissao = self.consulta_menor_comissao()
        valores = self.consulta_soma_valores()
        
        consultas = {
            "res_usu":quantidade_res_usu,
            "valor_medio":valor_medio,
            "pedido_mes":pedido_mes,
            "usuario_unico":usuario_unico,
            "maior_comissao":maior_comissao,
            "menor_comissao":menor_comissao,
            "valores":valores
        }
        
        return consultas

    def executar(self,sql,tupla): # É só um execute com commit
        self.conexao.execute(sql,tupla)
        self.conexao.commit()
SELECT AVG(valor),u.nome_usuario FROM venda v -- Qual a média de gasto de cada pessoa | Modifique o pk_restaurante para mudar os resultados
                INNER JOIN usuario u ON u.pk_usuario = v.pk_usuario
                WHERE pk_restaurante = 3 GROUP BY v.pk_usuario;

SELECT u.nome_usuario,MAX(valor) FROM venda v -- Qual a maior compra(em valor) feita no restaurante? | Modifique o pk_restaurante para mudar os resultados
                INNER JOIN usuario u ON u.pk_usuario = v.pk_usuario
                WHERE pk_restaurante = 3;

SELECT vp.pk_venda,SUM(quantidade) FROM venda_produto vp -- Qual o maior pedido(em quantidade) feita no restaurante | Modifique o pk_restaurante para mudar os resultados
            INNER JOIN venda v ON v.pk_venda = vp.pk_venda 
            WHERE v.pk_restaurante = 3
            GROUP BY vp.pk_venda ORDER BY SUM(quantidade) DESC LIMIT 1;

SELECT p.nome_produto,COUNT(vp.pk_produto) FROM venda_produto vp -- Qual o item mais pedido | Modifique o pk_restaurante para mudar os resultados
        INNER JOIN venda v ON v.pk_venda = vp.pk_venda
        INNER JOIN produto p ON p.pk_produto = vp.pk_produto
        WHERE v.pk_restaurante = 3
        GROUP BY vp.pk_produto ORDER BY COUNT(vp.pk_produto) DESC LIMIT 1;

SELECT COUNT(CASE WHEN status = 'criado' THEN status ELSE NULL END) AS 'Criado', -- Quantos pedidos em cada status? | Modifique o pk_restaurante para mudar os resultados
COUNT(CASE WHEN status = 'aceito' THEN status ELSE NULL END) AS 'Aceito',
COUNT(CASE WHEN status = 'rejeitado' THEN status ELSE NULL END) AS 'Rejeitado',
COUNT(CASE WHEN status = 'saiu para a entrega' THEN status ELSE NULL END) AS 'Saiu para a entrega',
COUNT(CASE WHEN status = 'entregue' THEN status ELSE NULL END) AS 'Entregue'
FROM venda v WHERE  pk_restaurante = 3;


SELECT (SELECT COUNT(1) FROM restaurante r) AS 'restaurante', (SELECT COUNT(1) FROM usuario u WHERE admin = 0) AS 'Usuario'; -- Quantidade de restaurantes e clientes cadastrados

SELECT r.restaurante, COUNT(DISTINCT pk_usuario) as 'usuarios' FROM venda v
                INNER JOIN restaurante r ON v.pk_restaurante = r.pk_restaurante 
                GROUP BY r.pk_restaurante ; --Quantidade de clientes únicos que já fizeram um pedido em cada restaurante

SELECT AVG(valor), r.restaurante FROM venda
                INNER JOIN restaurante r  ON venda.pk_restaurante  = r.pk_restaurante 
                GROUP BY venda.pk_restaurante; -- Ticket médio por restaurante (valor médio de cada pedido)

SELECT
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
    INNER JOIN restaurante r ON r.pk_restaurante = v.pk_restaurante 
    GROUP BY v.pk_restaurante ; --Pivote a quantidade de pedidos de cada restaurante (linhas) e meses (colunas)

-- Tecnicamente o trabalho pedia pela menor e maior comissao do restaurante, mas todos os restuarantes tem uma unica comissao, então os selects a seguir
-- pega o restaurante com a menor comissao e pega o restaurante com a maior comissao

SELECT pk_restaurante,restaurante,MAX(comissao),email_restaurante,senha_restaurante,criacao,ultima_atualizacao,tem_produtos FROM restaurante; -- maior comissao
SELECT pk_restaurante,restaurante,MIN(comissao),email_restaurante,senha_restaurante,criacao,ultima_atualizacao,tem_produtos FROM restaurante; -- menor comissao
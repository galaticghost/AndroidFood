
-- Todos esses dados já estão no banco

INSERT INTO restaurante (pk_restaurante,restaurante,comissao,email_restaurante,senha_restaurante,criacao,ultima_atualizacao,tem_produtos) VALUES
	 (2,'Comidas Chinesas',35,'xijiping@alipay.cn','3a1200279b514ca4409dd8136527046a','2024-11-13 08:44:35','2024-11-13 08:44:44',1),
	 (3,'Caduzinho Foods',32,'cadu@gmail.com','274672838a8002344fed81ca1228bf05','2024-11-13 08:55:00','2024-11-26 08:13:15',1),
	 (4,'Jão Lauro Carnes Veganas',26,'jaolauro@carne.com.br','0ba0dd14265fced34a1202aeced9f02d','2024-11-13 08:56:34','2024-11-13 08:56:43',1),
	 (5,'Restaurante não aguento mais',2,'ca@du.com','8b45d551498d78d0123dd0f635f6d89b','2024-11-13 08:57:52','2024-11-13 08:57:56',1),
	 (6,'Restaurante sem produtos',0,'restaurante@gmail.com','274672838a8002344fed81ca1228bf05','2024-11-13 08:58:37','2024-11-13 08:58:43',0),
	 (7,'Zeca Lanches',69,'zecalanches@gmail.com','274672838a8002344fed81ca1228bf05','2024-11-25 11:01:41','2024-11-25 11:01:48',1),
	 (8,'BurgasBrownie',23,'burgasbrownie@gmail.com','274672838a8002344fed81ca1228bf05','2024-11-25 11:03:16','2024-11-25 11:03:21',1),
	 (9,'Brohas Sushi',43,'brohassushi@gmail.com','3a1200279b514ca4409dd8136527046a','2024-11-25 11:05:57','2024-11-25 11:06:03',1),
	 (10,'Clinica H. Romeu',0,'hromeu@hotmail.com','030ea7a3f57f399ecc51def9f1e44e02','2024-11-25 11:09:56','2024-11-25 11:10:26',1),
	 (11,'Shaxcrimetus SHaslVogus',13,'maranax@infernux.bl','35aa44097c4da581cc04cb7f843ca9c1','2024-11-25 11:12:41','2024-11-25 11:12:50',1);
INSERT INTO restaurante (pk_restaurante,restaurante,comissao,email_restaurante,senha_restaurante,criacao,ultima_atualizacao,tem_produtos) VALUES
	 (12,'Restaurante com muitos produtos',5,'res@pro.co','274672838a8002344fed81ca1228bf05','2024-11-25 11:14:11','2024-11-25 11:14:11',0),
	 (13,'Ratoeira do JE',35,'joaoeduardo@yahoo.com.br','8b9763252f53b9ce24c3dc04c1caacf0','2024-11-26 07:57:11','2024-11-26 07:57:29',1),
	 (14,'Linguiças do Jeremias',45,'jeremias@gmail.com','274672838a8002344fed81ca1228bf05','2024-11-26 07:58:27','2024-11-26 07:58:32',1),
	 (15,'Churrasco do Ricardão',41,'ricardo@hotmail.com','274672838a8002344fed81ca1228bf05','2024-11-26 07:59:31','2024-11-26 07:59:57',1);

     INSERT INTO produto (pk_produto,nome_produto,preco,pk_restaurante) VALUES
	 (1,'Comida mexicana',35,2),
	 (2,'Sopa de gelo',32,2),
	 (3,'Cadu ao sugo',30,3),
	 (4,'Agua com gas',50,3),
	 (5,'agua sem gas',2,3),
	 (6,'Massa com terra',25,3),
	 (7,'A la hora',100,3),
	 (8,'Carne vegana',50,4),
	 (9,'Carne',49,4),
	 (10,'vegana',1,4);
INSERT INTO produto (pk_produto,nome_produto,preco,pk_restaurante) VALUES
	 (11,'Sopa de gelo',40,5),
	 (12,'Pedra com terra',30,5),
	 (13,'Um vírus',10,5),
	 (14,'Molho do Zeca',40,7),
	 (15,'Especial do zeca de dias das mães',24,7),
	 (16,'Podrão',2,7),
	 (17,'agua sem gas',3,7),
	 (18,'cachorro quente',12,7),
	 (19,'batata frita',20,7),
	 (20,'Brownie burguer clássico',10.5,8);
INSERT INTO produto (pk_produto,nome_produto,preco,pk_restaurante) VALUES
	 (21,'Brownie burguer de nutella',12,8),
	 (22,'Brownie burguer de chocolate belga',11,8),
	 (23,'Brownie burguer de doce de leite',11.5,8),
	 (24,'Brownie burguer de paçoca',11.5,8),
	 (25,'Brownie burguer de oreo',11.75,8),
	 (26,'Brownie burguer de ovomaltine',11,8),
	 (27,'Brownie burguer de flocos',11,8),
	 (28,'Brownie burguer de baunilha',10.5,8),
	 (29,'Brownie burguer de morango',11,8),
	 (30,'Brownie burguer de pistache',11,8);
INSERT INTO produto (pk_produto,nome_produto,preco,pk_restaurante) VALUES
	 (31,'Brownie burguer de cookies',11.5,8),
	 (32,'agua com gas',3.5,8),
	 (33,'agua sem gas',3.5,8),
	 (34,'refil um litro',6,8),
	 (35,'Hossomaki de terra',10,9),
	 (36,'niguiri de pedra',12,9),
	 (37,'um salmao cru inteiro',85,9),
	 (38,'shoyu cem ml',100,9),
	 (39,'hossomaki de rocha',4,9),
	 (40,'uramaki de terra',34,9);
INSERT INTO produto (pk_produto,nome_produto,preco,pk_restaurante) VALUES
	 (41,'um hossomaki normal',10,9),
	 (42,'Sangue o positivo',40,10),
	 (44,'Tipo o negativo',27,10),
	 (45,'Tipo O negativo',37,10),
	 (46,'Yakisoba de alho',560,10),
	 (47,'geroxe cruo',6,11),
	 (48,'maranax pallex',6,11),
	 (49,'crudux cruo',6,11),
	 (50,'Queijo',20,13),
	 (51,'queijo mofado',50,13);
INSERT INTO produto (pk_produto,nome_produto,preco,pk_restaurante) VALUES
	 (52,'Chorume',10,13),
	 (53,'Linguiça pequena',8,14),
	 (54,'Linguiça média',15,14),
	 (55,'Linguiça grande',23,14),
	 (56,'Linguição',30,14),
	 (57,'Linguição',30,15),
	 (58,'Picanha',20,15),
	 (59,'Varão',40,15),
	 (60,'Pescoção',40,15);
INSERT INTO usuario (pk_usuario,nome_usuario,email_usuario,senha_usuario,criacao,ultima_atualizacao,admin) VALUES
	 (1,'Theo Bola Cunha','bola@gmail.com','274672838a8002344fed81ca1228bf05','2024-11-13 09:42:47','2024-11-21 10:33:16',0),
	 (2,'Carlos Dias','cadu@cadu.com','274672838a8002344fed81ca1228bf05','2024-11-16 17:49:51','2024-11-21 09:11:26',0),
	 (3,'Jão Lauro','joaolauro@gmail.com','274672838a8002344fed81ca1228bf05','2024-11-19 09:09:07','2024-11-26 08:27:49',1),
	 (5,'admin','admin@androidfood.com','274672838a8002344fed81ca1228bf05','2024-11-25 11:00:15','2024-11-25 11:00:15',1),
	 (9,'Mestor Yiliotto Talamon','mestor@gmail.com','4c9f82895cc9ea0c86c7ba5f3372a25a','2024-11-25 11:16:26','2024-11-25 11:16:34',0),
	 (10,'Joaozinho Um Dois Tres','joaozinho@youtube.com','274672838a8002344fed81ca1228bf05','2024-11-26 08:00:53','2024-11-26 08:01:02',0),
	 (11,'Xi Jinping China','xijiping@alibaba.cn','5f414d0e802b620c988d6acca4d80301','2024-11-26 08:03:39','2024-11-26 08:03:51',0);
INSERT INTO venda (pk_venda,valor,pk_usuario,pk_restaurante,criacao,status) VALUES
	 (1,306,1,2,'2024-11-13 09:43:05','criado'),
	 (2,100,1,4,'2024-11-13 09:51:18','criado'),
	 (3,250,1,3,'2024-11-13 09:59:35','entregue'),
	 (4,360,1,3,'2024-11-14 09:01:22','entregue'),
	 (6,310,1,3,'2024-11-14 10:48:49','entregue'),
	 (7,150,1,3,'2024-11-14 10:54:52','entregue'),
	 (8,228,2,3,'2024-11-16 17:50:14','entregue'),
	 (9,170,2,5,'2024-11-21 09:11:33','criado'),
	 (10,1496,2,2,'2024-11-21 09:11:40','criado'),
	 (11,90,2,5,'2024-11-21 09:11:46','criado');
INSERT INTO venda (pk_venda,valor,pk_usuario,pk_restaurante,criacao,status) VALUES
	 (12,296,2,4,'2024-11-21 09:12:03','criado'),
	 (13,268,2,3,'2024-11-21 09:12:29','rejeitado'),
	 (14,150,2,3,'2024-11-21 09:12:33','aceito'),
	 (15,250,2,3,'2024-11-21 09:12:40','criado'),
	 (16,18,2,3,'2024-11-21 09:12:45','entregue'),
	 (17,1600,1,2,'2024-11-21 10:33:20','criado'),
	 (18,2605,9,7,'2024-11-25 11:16:52','criado'),
	 (19,100002,9,3,'2024-11-25 11:17:07','rejeitado'),
	 (20,29.5,9,8,'2024-11-25 11:17:20','criado'),
	 (21,51,9,4,'2024-11-25 11:17:32','criado');
INSERT INTO venda (pk_venda,valor,pk_usuario,pk_restaurante,criacao,status) VALUES
	 (22,560,9,10,'2024-11-25 11:17:39','criado'),
	 (23,64,9,2,'2024-11-25 11:17:46','criado'),
	 (24,108,9,11,'2024-11-25 11:17:59','criado'),
	 (25,20,9,5,'2024-11-25 11:18:16','criado'),
	 (26,30,9,3,'2024-11-25 11:18:44','saiu para a entrega'),
	 (27,105,10,9,'2024-11-26 08:01:15','criado'),
	 (28,50,10,13,'2024-11-26 08:01:25','criado'),
	 (29,2078,10,14,'2024-11-26 08:01:51','criado'),
	 (30,21,10,8,'2024-11-26 08:02:22','criado'),
	 (31,120,10,15,'2024-11-26 08:02:37','criado');
INSERT INTO venda (pk_venda,valor,pk_usuario,pk_restaurante,criacao,status) VALUES
	 (32,74,11,10,'2024-11-26 08:04:18','criado'),
	 (33,14.5,11,8,'2024-11-26 08:04:29','criado'),
	 (34,1080,11,9,'2024-11-26 08:04:40','criado'),
	 (35,88,11,7,'2024-11-26 08:04:57','criado'),
	 (36,108,11,11,'2024-11-26 08:05:10','criado'),
	 (37,102,11,2,'2024-11-26 08:05:17','criado'),
	 (38,100,11,4,'2024-11-26 08:05:26','criado');
INSERT INTO venda_produto (pk_venda_produto,pk_venda,pk_produto,quantidade,valor_total) VALUES
	 (1,1,1,6,210),
	 (2,1,2,3,96),
	 (3,2,8,2,100),
	 (4,3,3,5,150),
	 (5,3,4,2,100),
	 (6,4,7,3,300),
	 (7,4,3,2,60),
	 (11,6,4,5,250),
	 (12,6,3,2,60),
	 (13,7,4,3,150);
INSERT INTO venda_produto (pk_venda_produto,pk_venda,pk_produto,quantidade,valor_total) VALUES
	 (14,8,5,4,8),
	 (15,8,3,4,120),
	 (16,8,6,4,100),
	 (17,9,11,2,80),
	 (18,9,12,3,90),
	 (19,10,1,40,1400),
	 (20,10,2,3,96),
	 (21,11,12,3,90),
	 (22,12,8,1,50),
	 (23,12,9,4,196);
INSERT INTO venda_produto (pk_venda_produto,pk_venda,pk_produto,quantidade,valor_total) VALUES
	 (24,12,10,50,50),
	 (25,13,6,2,50),
	 (26,13,3,2,60),
	 (27,13,4,3,150),
	 (28,13,5,4,8),
	 (29,14,4,3,150),
	 (30,15,4,5,250),
	 (31,16,5,9,18),
	 (32,17,2,50,1600),
	 (33,18,14,60,2400);
INSERT INTO venda_produto (pk_venda_produto,pk_venda,pk_produto,quantidade,valor_total) VALUES
	 (34,18,16,4,8),
	 (35,18,17,59,177),
	 (36,18,19,1,20),
	 (37,19,7,1000,100000),
	 (38,19,5,1,2),
	 (39,20,34,1,6),
	 (40,20,25,2,23.5),
	 (41,21,10,1,1),
	 (42,21,8,1,50),
	 (43,22,46,1,560);
INSERT INTO venda_produto (pk_venda_produto,pk_venda,pk_produto,quantidade,valor_total) VALUES
	 (44,23,2,2,64),
	 (45,24,49,6,36),
	 (46,24,48,6,36),
	 (47,24,47,6,36),
	 (48,25,13,2,20),
	 (49,26,3,1,30),
	 (50,27,35,2,20),
	 (51,27,37,1,85),
	 (52,28,52,3,30),
	 (53,28,50,1,20);
INSERT INTO venda_produto (pk_venda_produto,pk_venda,pk_produto,quantidade,valor_total) VALUES
	 (54,29,56,69,2070),
	 (55,29,53,1,8),
	 (56,30,28,2,21),
	 (57,31,60,1,40),
	 (58,31,59,1,40),
	 (59,31,58,2,40),
	 (60,32,45,2,74),
	 (61,33,32,1,3.5),
	 (62,33,26,1,11),
	 (63,34,40,2,68);
INSERT INTO venda_produto (pk_venda_produto,pk_venda,pk_produto,quantidade,valor_total) VALUES
	 (64,34,39,3,12),
	 (65,34,38,10,1000),
	 (66,35,14,1,40),
	 (67,35,15,2,48),
	 (68,36,47,6,36),
	 (69,36,48,6,36),
	 (70,36,49,6,36),
	 (71,37,1,2,70),
	 (72,37,2,1,32),
	 (73,38,10,50,50);
INSERT INTO venda_produto (pk_venda_produto,pk_venda,pk_produto,quantidade,valor_total) VALUES
	 (74,38,8,1,50);

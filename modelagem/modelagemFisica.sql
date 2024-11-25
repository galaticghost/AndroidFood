CREATE TABLE IF NOT EXISTS restaurante (
pk_restaurante INTEGER PRIMARY KEY NOT NULL,
    restaurante VARCHAR(100) NOT NULL,
    comissao INTEGER CHECK (comissao >= 0) NOT NULL,
    email_restaurante VARCHAR(200) NOT NULL,
    senha_restaurante VARCHAR(100) NOT NULL,
    criacao DATE DEFAULT (datetime('now', 'localtime')),
    ultima_atualizacao DATE DEFAULT (datetime('now', 'localtime')),
    tem_produtos bool DEFAULT 0
);

CREATE TABLE IF NOT EXISTS produto (
pk_produto INTEGER PRIMARY KEY,
nome_produto VARCHAR(100) NOT NULL,
preco NUMERIC CHECK (preco > 0) NOT NULL,
pk_restaurante INTEGER REFERENCES restaurante NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario(
                            pk_usuario INTEGER PRIMARY KEY NOT NULL,
                            nome_usuario VARCHAR(200) NOT NULL,
                            email_usuario VARCHAR(200) NOT NULL,
                            senha_usuario VARCHAR(100) NOT NULL,
                            criacao DATE DEFAULT (datetime('now', 'localtime')),
                            ultima_atualizacao DATE DEFAULT (datetime('now', 'localtime')),
                            admin BOOLEAN NOT NULL DEFAULT 0 
                            );

CREATE TABLE IF NOT EXISTS venda(
                            pk_venda INTEGER PRIMARY KEY NOT NULL,
                            valor NUMERIC CHECK (valor > 0) NOT NULL,
                            pk_usuario INTEGER REFERENCES usuario NOT NULL,
                            pk_restaurante INTEGER REFERENCES restaurante NOT NULL,
                            criacao DATE DEFAULT(datetime('now', 'localtime')),
                            status VARCHAR(50) DEFAULT "criado"
                            );

CREATE TABLE IF NOT EXISTS venda_produto(
                            pk_venda_produto INTEGER PRIMARY KEY NOT NULL,
                            pk_venda INTEGER REFERENCES venda NOT NULL,
                            pk_produto INTEGER REFERENCES produto NOT NULL,
                            quantidade INTEGER NOT NULL,
                            valor_total NUMERIC CHECK(valor_total > 0) NOT NULL
                            );
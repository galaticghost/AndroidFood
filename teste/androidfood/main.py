from flask import Flask,render_template, url_for
from flask import session
from flask import request
from os import urandom
from hashlib import md5

from database.database import Database

app = Flask(__name__)
key = urandom(12).hex()
app.secret_key = key
database = Database()

@app.route("/", methods=['GET','POST'])
def index():
    if session.get('login') == None:
        session['login'] = False
    return render_template("index.jinja",login = session['login'])

@app.route("/login", methods=['GET','POST'])
def login():
    falha = False
    if session.get('login') == None:
        session['login'] = False
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        senha = request.form['senha']
        senha = md5(senha.encode())
        senha = senha.hexdigest()
        restaurante_query = database.consulta_restaurante(email,senha)
        if restaurante_query is not None:
            session['pk'] = restaurante_query[0]
            session['nome'] = restaurante_query[1]
            session['comissao'] = restaurante_query[2]
            session['ultimo_acesso'] = restaurante_query[3]
            database.executar("UPDATE restaurante SET ultima_atualizacao = datetime('now','localtime') WHERE email_restaurante = ? AND senha_restaurante = ?",(email,senha)) # atualiza a data do ultimo login
            session['login'] = True
            return render_template("index.jinja",login = session['login'])
        else:
            session['login'] = False
            falha = True
    return render_template("login.jinja",login = session['login'],falha = falha)

@app.route('/logoff', methods=['GET','POST'])
def logoff():
    session['login'] = False
    return render_template("index.jinja",login = session['login'])

@app.route('/restaurante', methods=['GET','POST'])
def restaurante():
    if session.get('login') == None or session['login'] == False:
        session['login'] = False
        return render_template("index.jinja",login = session['login'])
    vendas = database.consulta_pedidos(session['pk'])
    pedidos = []
    for venda in vendas:
        if venda[4] != "cancelado" or venda[4] == "entregue":
            pedido = {
                        "pk": venda[0],
                        "valor": venda[1],
                        "pk_usuario": venda[2],
                        "criacao": venda[3],
                        "status": venda[4]
                    }
            pedidos.append(pedido)
    if pedidos == []:
        pedidos = None
    
    return render_template("restaurante.jinja",nome = session['nome'],pedidos = pedidos)
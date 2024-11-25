from flask import Flask,render_template, url_for
from flask import session
from flask import request
from flask import redirect
from os import urandom
from hashlib import md5

from database.database import Database

app = Flask(__name__)

key = urandom(12).hex() #Gera a chave secreta
app.secret_key = key # Chave secreta

database = Database() # Conecta a database

@app.route("/index", methods=['GET','POST']) # tela inicial
@app.route("/", methods=['GET','POST'])
def index():
    if session.get('login') == None: # Ve se tem login
        session['login'] = False
    return render_template("index.jinja",login = session['login'])

@app.route("/login", methods=['GET','POST']) # login do restaurante
def login():
    falha = False
    
    if session.get('login') == None:
        session['login'] = False
    
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        
        senha = request.form['senha']
        senha = md5(senha.encode())
        senha = senha.hexdigest()
        
        restaurante_query = database.consulta_login("restaurante",email,senha) == False # Checa se o login existe
        if restaurante_query is False: # Coloca os valores na sessão e renderiza o template
            restaurante_query = database.consulta_restaurante(email,senha)
            session['pk'] = restaurante_query[0]
            session['nome'] = restaurante_query[1]
            session['comissao'] = restaurante_query[2]
            session['ultimo_acesso'] = restaurante_query[3]
            session['admin'] = False
            session['restaurante'] = True
            
            database.executar("""UPDATE restaurante 
            SET ultima_atualizacao = datetime('now','localtime') 
            WHERE email_restaurante = ? AND senha_restaurante = ?""",(email,senha)) # atualiza a data do ultimo login
            
            session['login'] = True

            return render_template("index.jinja",login = session['login'])
        else:
            session['login'] = False # Se der erro
            falha = True
    
    return render_template("login.jinja",login = session['login'],falha = falha,type_login = "login")

@app.route("/login/admin", methods=['GET','POST']) # login do admin
def login_admin():
    falha = False
    
    if session.get('login') == None:
        session['login'] = False
    
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        senha = request.form['senha']
        senha = md5(senha.encode())
        senha = senha.hexdigest()
        
        admin_query = database.consulta_login("usuario",email,senha) # Checa o login
        if admin_query is True and database.consulta_admin(email,senha) == 1: # Checa se o usuario é um admin,coloca os valores na sessão e renderiza o template 
            admin_query = database.consulta_usuario(email,senha)
            session['pk'] = admin_query[0]
            session['nome'] = admin_query[1]
            session['ultima_atualizacao'] = admin_query[2]
            session['admin'] = 1
            session['restaurante'] = False
            
            database.executar("""UPDATE usuario 
            SET ultima_atualizacao = datetime('now','localtime') 
            WHERE email_usuario = ? AND senha_usuario = ?""",(email,senha)) # atualiza a data do ultimo login
            
            session['login'] = True

            return render_template("index.jinja",login = session['login'])
        else: # Se der erro
            session['login'] = False
            falha = True
    
    return render_template("login.jinja",login = session['login'],falha = falha,type_login = "login_admin")

@app.route('/logout', methods=['GET','POST'])
def logout(): # Logout
    session.clear()
    return index()

@app.route('/restaurante', methods=['GET','POST'])
def restaurante():
    if (session.get('login') == None or session['login'] == False) or (session.get('restaurante') == None or session['restaurante'] == False):
        return index()
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
    
    session['pedidos'] = pedidos
    
    return render_template("restaurante.jinja",nome = session['nome'],pedidos = session['pedidos'])

@app.route('/restaurante/aceitar/<pk>', methods=['GET','POST'])
def aceitar(pk = None): # Atualiza o status do pedido para aceito
    return inserir(pk,"criado","aceito")
    
@app.route('/restaurante/rejeitar/<pk>', methods=['GET','POST'])
def rejeitar(pk = None): # Atualiza o status do pedido para rejeitado
    return inserir(pk,"criado","rejeitado")

@app.route('/restaurante/entrega/<pk>', methods=['GET','POST'])
def entrega(pk = None): # Atualiza o status do pedido para saiu para a entrega
    return inserir(pk,"aceito","saiu para a entrega")
    
@app.route('/restaurante/entregue/<pk>', methods=['GET','POST'])
def entregue(pk = None): # Atualiza o status do pedido para entregue
    return inserir(pk,"saiu para a entrega","entregue")

def inserir(pk,status_check,status): # Atualiza o status do pedido
    if (session.get('login') == None or session['login'] == False) or (session.get('restaurante') == None or session['restaurante'] == False):
        return index()
    if database.consulta_status(pk,session['pk']) == status_check:
        database.executar(f"UPDATE venda SET status = '{status}' WHERE pk_venda = ? AND pk_restaurante = ?;", (pk,session['pk']))
    return restaurante()

@app.route("/restaurante/relatorio", methods=['GET','POST'])
def relatorio():
    if (session.get('login') == None or session['login'] == False) or (session.get('restaurante') == None or session['restaurante'] == False):
        return index()
    
    consultas = database.relatorio(session["pk"])
    
    return render_template("relatorio.jinja",consultas = consultas)

@app.route("/restaurante/relatorioAdmin/<pk>", methods=['GET','POST'])
def relatorio_restaurante_admin(pk = None): # Relatorio mas visto pelo admin
    if (session.get('login') == None or session['login'] == False) or (session.get('admin') == None or session['admin'] == False):
        return index()
    
    consultas = database.relatorio(pk)
    
    return render_template("relatorio.jinja",consultas = consultas)

@app.route("/relatorioAdmin", methods=['GET','POST']) # relatório do admin
def relatorio_admin():
    if (session.get('login') == None or session['login'] == False) or (session.get('admin') == None or session['admin'] == False):
        return index()

    consultas = database.relatorio_administrativo()
    
    return render_template("relatorioAdmin.jinja", consultas = consultas)

@app.route("/relatorioAdmin/adminRestaurantes", methods=['GET','POST'])
def restaurantes_admin(): # Mostra os restaurantes pro admin
    if (session.get('login') == None or session['login'] == False) or (session.get('admin') == None or session['admin'] == False):
        return index()
    
    restaurantes = database.consulta_restaurantes()

    return render_template("adminRestaurantes.jinja", restaurantes = restaurantes)

@app.errorhandler(404) # 404
def not_found(e):
    return render_template("/notFound.jinja")
    
@app.template_filter() # Função para formatar dinheiro
def formatoDinheiro(valor):
    if valor == None:
        return f"0.00" 
    return f"{float(valor):.2f}"
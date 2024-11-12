from flask import Flask,render_template
from flask import session
from flask import request
from os import urandom

from database.database import Database

app = Flask(__name__)
key = urandom(12).hex()
app.secret_key = key
database = Database()


@app.route("/", methods=['GET','POST'])
def index():
    if session['login'] is not None:
        session['login'] = False
    return render_template("index.jinja",login = session['login'])

@app.route("/login", methods=['GET','POST'])
def login():
    session['login'] = False
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        restaurante = database.consulta_restaurante(email,senha)
        if restaurante is not None:
            session['login'] = True
        else:
            session['login'] = False
    return render_template("login.jinja",login = session['login'])

@app.route('/')
def logoff():
    session['login'] = False
    return render_template("index.jinja",login = session['login'])
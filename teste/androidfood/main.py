from flask import Flask,render_template

app = Flask(__name__)


@app.route("/")
def index():
    login = False
    return render_template("index.jinja",login = login)

@app.route("/login")
def login():
    login = False
    return render_template("login.jinja",login = login)


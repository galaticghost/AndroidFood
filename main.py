#!/opt/homebrew/bin/python3
from app.app import App
from database.database import Database

database = Database()
app = App(database)

app.menu_inicial()

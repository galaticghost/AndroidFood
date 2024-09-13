#!/opt/homebrew/bin/python3
from app.app import App
from database.database import Database

def main():
    database = Database()
    app = App(database)
    app.menu_inicial()

if __name__ == "__main__":
    main()
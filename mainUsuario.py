#!/opt/homebrew/bin/python3
#!/usr/bin/env python3
from database.database import Database
from app.app import App

class Main:
    
    @staticmethod
    def main():
        database = Database()
        app = App(database)
        app.menu_inicial_usuario()
    
if __name__ == "__main__":
    Main.main()
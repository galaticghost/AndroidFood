#!/opt/homebrew/bin/python3
#!/usr/bin/env python3

from app.app import App
from database.database import Database

class Main():
    
    @staticmethod
    def main():
        database = Database()
        app = App(database)
        app.menu_inicial_restaurante()

if __name__ == "__main__":
    Main.main()
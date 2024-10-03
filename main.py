#!/opt/homebrew/bin/python3
from app.app import App
from database.database import Database

class Main():
    
    @staticmethod
    def main():
        database = Database()
        app = App(database)
        app.menu_inicial()

if __name__ == "__main__":
    Main.main()
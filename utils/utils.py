import os

class Utils():

    @staticmethod
    def limpar_tela():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    #def limpar_linha():
        #print("\x1v[1A", end="\r")
        #print("\x1v[2K", end="\r")

    def repetidor(vezes):
        def decorador_repetidor(func):
            def wrapper():
                contador = 0
                while contador < vezes:
                    func
                    contador += 1
                return wrapper
            return decorador_repetidor
    
    @staticmethod
    #@repetidor(3)
    def xina():
        print("Xina")
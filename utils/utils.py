import os

class Utils():

    @staticmethod
    def limpar_tela(): # limpa tela
        os.system('cls' if os.name == 'nt' else 'clear')
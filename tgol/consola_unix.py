from os import system
from consola_base import ConsolaBase

class ConsolaUnix(ConsolaBase):
    
    def __init__(self):
        super().__init__()
        
    def cambiar_letra_terminal(self, letra=None, x=None, y=None):
        return
    
    def resize_terminal(self, x, y):
        return
    
    def poner_titulo(self, titulo):
        return
    
    def limpiar_cmd(self):
        os.system("clear")
        
    def tecla_presionada(self):
        return False
    
    def get_tecla(self):
        return ""
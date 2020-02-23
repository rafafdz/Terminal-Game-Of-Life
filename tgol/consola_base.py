import colorama
from abc import ABC, abstractmethod
from os import get_terminal_size


class ConsolaBase(ABC):
    
    def __init__(self, modo_limpiar="colorama"):
        self.modo_limpiar = modo_limpiar
        
        if modo_limpiar == "colorama":
            colorama.init()
            self.limpiar = self.limpiar_colorama
        elif modo_limpiar == "cls":
            self.limpiar = self.limpiar_cmd
        elif modo_limpiar == "espacio":
            self.limpiar = self.limpiar_espacio
        
    @abstractmethod
    def cambiar_letra_terminal(self, letra, x, y):
        pass
    
    @abstractmethod
    def resize_terminal(self, x, y):
        pass
    
    @abstractmethod
    def poner_titulo(self, titulo):
        pass
    
    # retorna un booleano indicando si hay una tecla en el buffer o no
    @abstractmethod
    def tecla_presionada(self):
        pass
    
    # Bloquea el thread y entrega el caracter usado en bytes
    @abstractmethod
    def get_tecla(self):
        pass
    
    @abstractmethod
    def limpiar_cmd(self):
        pass
    
    def limpiar_colorama(self):
        print("\033[1;1H")
        input()
        
    def limpiar_espacio(self):
        print("\n" * 50)
    
    def get_size_terminal(self):
        porte = str(get_terminal_size())[17:-1]
        porte = porte.split(",")
        x = int(porte[0][8:])
        y = int(porte[1][7:])
        return (x, y)
    
    def imprimir(self, obj):
        print(obj)
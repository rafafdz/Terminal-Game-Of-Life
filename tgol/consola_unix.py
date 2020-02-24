"""
Basado en https://code.activestate.com/recipes/572182-how-to-implement-kbhit-on-linux/
"""
import sys, termios, atexit
from select import select
from os import system
from consola_base import ConsolaBase


fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def setup_terminal_mode():
    atexit.register(set_normal_term)
    set_curses_term()
    
def getch():
    return sys.stdin.read(1)

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr != []

class ConsolaUnix(ConsolaBase):
    def __init__(self):
        super().__init__()
        self.map_tecla = {"a" : "K", "d" : "M", 
                          "s" : "P", "w" : "H"}
        setup_terminal_mode()
        
    def cambiar_letra_terminal(self, letra=None, x=None, y=None):
        # No soportado en linux
        return
    
    def resize_terminal(self, x, y):
        # No soportado en linux
        return
    
    def poner_titulo(self, titulo):
        # No soportado en linux
        return
    
    def limpiar_os_cmd(self):
        system("clear")
        
    def tecla_presionada(self):
        return kbhit()
    
    def get_tecla(self):
        tecla = getch()
        low = tecla.lower()
        if low in self.map_tecla:
            tecla = self.map_tecla[low]
            
        return tecla.encode()
    
if __name__ == "__main__":
    atexit.register(set_normal_term)
    set_curses_term()
    while True:
        print(".")
        if kbhit():
            print(repr(getch()))
            break
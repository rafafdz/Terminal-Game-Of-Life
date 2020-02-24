import ctypes
from time import sleep
from os import system
import msvcrt

LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11

class COORD(ctypes.Structure):
    _fields_ = [("X",ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]
 
 
class ConsolaWin(ConsolaBase):
    
    def __init__(self):
        super().__init__()

    def cambiar_letra_terminal(self, letra = "Terminal", x = 8, y = 8):
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        font.nfont = 12
        font.dwFontSize.X = x
        font.dwFontSize.Y = y
        font.FontFamily = 16
        font.FontWeight = 400
        font.FaceName = letra

        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))
        return

    def resize_terminal(self, x, y):
        system(f"mode con:cols={x} lines={y}")

    def poner_titulo(self, titulo="Ventana sin titulo"):
        ctypes.windll.kernel32.SetConsoleTitleW(titulo)
  
    def tecla_presionada(self):
        return msvcrt.kbhit()

    def get_tecla(self):
        return msvcrt.getch()

    def limpiar_os_cmd(self):
        system("cls")




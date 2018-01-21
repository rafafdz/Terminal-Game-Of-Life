import ctypes
from time import sleep
from os import system, get_terminal_size

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

def cambiar_letra_terminal(letra = "Terminal", x = 8, y = 8):
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

def resize_terminal(x, y):
	x = str(x)
	y = str(y)
	system("mode con:cols=" + x + " lines=" + y)

def poner_titulo(titulo = "Ventana sin titulo"):
	ctypes.windll.kernel32.SetConsoleTitleW(titulo)

def get_size_terminal():
	porte = str(get_terminal_size())[17:-1]
	porte = porte.split(",")
	x = int(porte[0][8:])
	y = int(porte[1][7:])
	return (x, y)
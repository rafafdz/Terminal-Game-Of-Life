import platform
from tgol.ventana import Ventana

if platform.system() == "Windows":
    from tgol.consola_win import ConsolaWin
    consola = ConsolaWin()
else:
    from tgol.consola_unix import ConsolaUnix
    consola = ConsolaUnix()

if __name__ == "__main__":
    ventana = Ventana(consola, 60, 1200, 10)
    ventana.mainloop()
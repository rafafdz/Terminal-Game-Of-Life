import platform
from tgol.ventana import Ventana

if platform.system() == "Windows":
    from tgol.consola_win import ConsolaWin
    consola = ConsolaWin()
else:
    from tgol.consola_unix import ConsolaUnix
    consola = ConsolaUnix()

ventana = Ventana(consola, 30, 50 , 60)
ventana.mainloop()

if __name__ == "__main__":
    main()
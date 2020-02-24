import platform
from tgol.ventana import Ventana

if platform.system() == "Windows":
    from tgol.consola_win import ConsolaWin
    consola = ConsolaWin()
else:
    from tgol.consola_unix import ConsolaUnix
    consola = ConsolaUnix()

ventana = Ventana(consola, 50, 400 , 60)
ventana.mainloop()

if __name__ == "__main__":
    main()
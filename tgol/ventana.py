from time import perf_counter, sleep
from os import system
from tablero import *
import msvcrt, colorama, consola

class Ventana:
	def __init__(self, size, random, fps, tipo):
		self.size_inicial = size
		self.tick = 1 / fps

		if str(random)[-1] == "%":
			self.cantidad_random = int(int(random[:-1]) / 100)

		else:
			self.cantidad_random = random

		self.modo_limpiar = "colorama"
		
		if tipo == "opti1":
			self.tablero = Tablero_opt1(self.size_inicial)
		elif tipo == "basico":
			self.tablero = Tablero(size)

		colorama.init()
		consola.cambiar_letra_terminal()
		consola.poner_titulo("Terminal Game of Life")
		consola.resize_terminal(size + 2, size + 5)
	
	def init_tablero(self, modo, archivo = None, cantidad_archivo = 0):
		self.tablero.rellenar()
		
		if modo == "random":
			self.tablero.randomizar(self.cantidad_random)
		elif modo == "cargar":
			self.tablero.cargar_random(archivo, cantidad_archivo)

	def calcular_next_frame(self):
		self.tablero.check_expansion()
		self.tablero.refresh()

	def imprimir(self):
		print(self.tablero)

	def limpiar(self):
		if self.modo_limpiar == "colorama":
			print("\033[1;1H")

		elif self.modo_limpiar == "cls":
			system("cls")

		elif self.modo_limpiar == "espacio":
			#print("\n" * 50)
			pass

	def key_press_check(self):
		if msvcrt.kbhit():
			tecla = msvcrt.getch()
			if tecla == b"q":
				self.salir = True

			elif tecla == b"p":
				if continuar:
					inicio_pausa = perf_counter()
					continuar = False
				else:
					descuento_pausa += (perf_counter() - inicio_pausa)
					continuar = True

			elif tecla in (b"K", b"M", b"H", b"P"):
				mapeo = {b"K": ("x", "restar"), b"M" : ("x", "sumar"),
						b"H" : ("y", "restar"), b"P" : ("y", "sumar")}

				self.tablero.mover_esquina(mapeo[tecla][0], mapeo[tecla][1])

				self.limpiar()
				self.imprimir()

	def mainloop(self):
		self.init_tablero("random")
		self.salir = False
		continuar = True
		t_inicial = perf_counter()
		tiempo_final = t_inicial + 20000
		tiempo_siguiente, tiempo_actual, descuento_pausa = 0, 0, 0

		while tiempo_actual <= tiempo_final:
			tiempo_actual = perf_counter()
			
			if tiempo_actual >= tiempo_siguiente and continuar:
				tiempo_siguiente += self.tick
				self.limpiar()
				self.imprimir()
				print("Generacion", self.tablero.gen, "/ Vivas:", len(self.tablero.celulas_vivas))
				self.calcular_next_frame()

			self.key_press_check()

			if self.salir:
				break

			sleep(0.001)

		gen = self.tablero.gen
		trans = perf_counter() - t_inicial - descuento_pausa

		print("Simulacion terminada:", gen, "Generaciones")
		print("Tiempo Transcurrido:", perf_counter() - t_inicial - descuento_pausa)
		print("FPS promedio:", gen / trans)
		input()
from time import perf_counter, sleep
from tablero import Tablero, Tablero_opt1

class Ventana:
	def __init__(self, consola, size, random, fps, opti=True):
		self.size_inicial = size
		self.tick = 1 / fps
		self.cantidad_random = random
		self.consola = consola
		
		if opti:
			self.tablero = Tablero_opt1(self.size_inicial)
		else:
			self.tablero = Tablero(size)

		self.consola.cambiar_letra_terminal()
		self.consola.poner_titulo("Terminal Game of Life")
		self.consola.resize_terminal(size + 2, size + 5)
	
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
		self.consola.imprimir(self.tablero)
  
	def limpiar(self):
		self.consola.limpiar()

	def key_press_check(self):
		if self.consola.tecla_presionada():
			tecla = self.consola.get_tecla()
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

				consola.limpiar()
				self.imprimir()

	def mainloop(self):
		# TODO: Que dependa del exterior
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
				#print("Generacion", self.tablero.gen, "/ Vivas:", len(self.tablero.celulas_vivas))
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
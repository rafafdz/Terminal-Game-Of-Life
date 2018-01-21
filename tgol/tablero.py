from celula import *
from random import sample
import colorama

class Tablero:
	def __init__(self, grid):
		self.grid = grid
		self.esq_grid = [0,0]
		self.pasos_esq = 3
		self.filas_extra = [0,0] # Arriba, abajo
		self.cols_extra = [0,0] # Izquierda, Derecha
		self.gen = 0

		# Genera matriz de grid x grid
		self.matriz = []
		linea = ["" for x in range(self.grid)]
		for x in range(self.grid): self.matriz.append(linea.copy())

	def __str__(self):
		lim_izq_x = self.cols_extra[0] + self.esq_grid[0] 
		lim_der_x = lim_izq_x + self.grid
		lim_arriba_y = self.filas_extra[0] + self.esq_grid[1] 
		lim_abajo_y = lim_arriba_y + self.grid


		output = "_" * (self.grid + 2) + "\n"
		for linea in self.matriz[lim_arriba_y : lim_abajo_y]: 
			output  += "|" + "".join([str(x) for x in linea[lim_izq_x : lim_der_x]]) + "|\n"
		output += "_" * (self.grid + 2)

		return output

	def celula_en(self, cords):
		cord_x_real = cords[0] + self.cols_extra[0]
		cord_y_real = cords[1] + self.filas_extra[0]

		largo_x = self.grid + self.cols_extra[0] + self.cols_extra[1]
		largo_y = self.grid + self.filas_extra[0] + self.filas_extra[1]

		if (cord_x_real < 0 or cord_y_real < 0 or 
		cord_x_real >= largo_x or cord_y_real >= largo_y):
			return None
		else:
			obj_encontrado = self.matriz[cord_y_real][cord_x_real] 
			return obj_encontrado

	def rellenar(self):
		for y in range(self.grid):
			for x in range(self.grid):
				self.matriz[y][x] = Celula((x,y), self)

	def cargar_random(self, nombre, cantidad):
		archivo = open(nombre, "r")
		cuenta_lineas = 0
		arch = archivo.readlines()
		for linea in arch:
			linea = linea.strip()
			if linea == str(cantidad):
				cords = eval(arch[cuenta_lineas + 1].strip())
				break
			cuenta_lineas += 1

		self.celulas_vivas = cords.copy()
		for cord in self.celulas_vivas:
			self.celula_en(cord).vida = True
		archivo.close()

	def mirar(self, cord):
		cord_x_real = cord[0] + self.cols_extra[0]
		cord_y_real = cord[1] + self.filas_extra[0]
		
		if (cord_x_real < 0 or cord_y_real < 0 or 
		cord_x_real >= len(self.matriz[0]) or cord_y_real >= len(self.matriz)):
			return 0
		else:
			return self.celula_en((cord_x_real, cord_y_real)).vida

	def refresh(self):
		for veces in range(2):
			for linea in self.matriz:
				for celula in linea:
					if veces == 0: celula.calcular_siguiente()
					else: celula.actualizar()

		self.gen += 1

	def check_expansion(self):
		posiciones = (0, -1)
		arriba_abajo, izq_der  = [], []
		for indice in posiciones:
			arriba_abajo.append(self.matriz[indice])
			izq_der.append([x[indice] for x in self.matriz])

		vidas_lineas = [False for x in range(4)]
		indice = 0
		for linea in arriba_abajo + izq_der:
			vidas_consec = 0
			for celula in linea:
				if celula.vida:
					vidas_consec += 1
					if vidas_consec == 3:
						vidas_lineas[indice] = True
						break
				else:
					vidas_consec = 0
			indice += 1
			
			
		contador = 0
		for cuenta in vidas_lineas:
			if cuenta > 0:
				pos_min_x = self.matriz[0][0].pos[0]
				pos_min_y = self.matriz[0][0].pos[1]
				largo_fila = len(self.matriz[0])
				largo_col = len(self.matriz)
				
				if contador in (0,1):
					if contador == 0:
						pos_y = pos_min_y - 1
						linea_insert = 0
						self.filas_extra[0] += 1
					else:
						pos_y = pos_min_y + largo_col
						linea_insert = largo_col
						self.filas_extra[1] += 1
						
					nueva_fila = [Celula((x, pos_y), self) for x in range(pos_min_x, pos_min_x + largo_fila)]
					self.matriz.insert(linea_insert, nueva_fila)

					#limpiar()
					#print("Se ha expandido una fila", contador)
					#input()

				elif contador in (2,3):
					if contador == 2:
						pos_x = pos_min_x - 1
						linea_insert = 0
						self.cols_extra[0] += 1
					else:
						pos_x = pos_min_x + largo_fila
						linea_insert = largo_fila
						self.cols_extra[1] += 1

					cuenta_fila = 0
					for y in range(pos_min_y, pos_min_y + largo_col):
						self.matriz[cuenta_fila].insert(linea_insert, Celula((pos_x, y), self))
						cuenta_fila += 1

			contador += 1

	def reset(self):
		self.matriz = []
		linea = ["" for x in range(self.grid)]
		for x in range(self.grid):
			self.matriz.append(linea.copy())

	def mover_esquina(self, eje, operacion):
		if eje == "x":
			fil_o_col = self.cols_extra
			ind_esq = 0
		else:
			fil_o_col = self.filas_extra
			ind_esq = 1

		if operacion == "sumar" and self.esq_grid[ind_esq] <= fil_o_col[1] - self.pasos_esq:
			self.esq_grid[ind_esq] += self.pasos_esq

		elif operacion == "sumar" and self.esq_grid[ind_esq] <= fil_o_col[1]:
			self.esq_grid[ind_esq] = fil_o_col[1]

		elif operacion == "restar" and self.esq_grid[ind_esq] >=  - fil_o_col[0] + self.pasos_esq:
			self.esq_grid[ind_esq] -= self.pasos_esq

		elif operacion == "restar" and self.esq_grid[ind_esq] >= fil_o_col[0]:
			self.esq_grid[ind_esq] = fil_o_col[0]


class Tablero_opt1(Tablero):
	def __init__(self, grid):
		Tablero.__init__(self, grid)
		self.celulas_vivas = []
		self.contadas_alguna_vez = []
		self.base_random = [(x,y) for y in range(self.grid) for x in range(self.grid)]

	def celula_en(self, cords, contar = False):
		cord_x_real = cords[0] + self.cols_extra[0]
		cord_y_real = cords[1] + self.filas_extra[0]

		largo_x = self.grid + self.cols_extra[0] + self.cols_extra[1]
		largo_y = self.grid + self.filas_extra[0] + self.filas_extra[1]

		if (cord_x_real < 0 or cord_y_real < 0 or 
		cord_x_real >= largo_x or cord_y_real >= largo_y):
			return None
		else:
			celula = self.matriz[cord_y_real][cord_x_real]

			if contar == True:
				celula.contar()
				if celula.veces_contada == 1:
					self.contadas_alguna_vez.append(celula.pos)
			return celula

	def rellenar(self):
		for y in range(self.grid):
			for x in range(self.grid):
				self.matriz[y][x] = Celula_opt1((x,y), self)

	def cargar_random(self, nombre, cantidad):
		archivo = open(nombre, "r")
		cuenta_lineas = 0
		arch = archivo.readlines()
		for linea in arch:
			linea = linea.strip()
			if linea == str(cantidad):
				cords = eval(arch[cuenta_lineas + 1].strip())
				break
			cuenta_lineas += 1

		self.celulas_vivas = cords.copy()
		for cord in self.celulas_vivas:
			self.celula_en(cord).vida = True
		archivo.close()

	def randomizar(self, cantidad):
		cords = sample(self.base_random, cantidad)
		for cord in cords:
			self.celula_en(cord).vida = True
			self.celulas_vivas.append(cord)

	def refresh(self):
		self.contadas_alguna_vez = []
		for cord in self.celulas_vivas:
			self.celula_en(cord).calcular_siguiente()

		# Se recorre todo el tablero buscando las celulas que fueron contadas 3 veces
		cola_update = self.celulas_vivas.copy()
		
		for cord in self.contadas_alguna_vez:
			celula = self.celula_en(cord)
			if celula.veces_contada == 3 and celula.vida == False:
				celula.vida_siguiente = True
				cola_update.append(cord)
				
			celula.reset_cuenta() # Resetear la cuenta de todas las celulas


		for cord in cola_update:
			celula = self.celula_en(cord)
			if celula.vida != celula.vida_siguiente:
				if celula.vida: #Celula que estaba viva y morirá
					self.celulas_vivas.remove(cord)

				else: #Celula muerta que en la siguiente ronda vivirá
					self.celulas_vivas.append(cord)
			
			celula.actualizar()

		self.gen += 1

	def check_expansion(self):
		posiciones = (0, -1)
		arriba_abajo, izq_der  = [], []
		for indice in posiciones:
			arriba_abajo.append(self.matriz[indice])
			izq_der.append([x[indice] for x in self.matriz])

		vidas_lineas = [False for x in range(4)]
		indice = 0
		for linea in arriba_abajo + izq_der:
			vidas_consec = 0
			for celula in linea:
				if celula.vida:
					vidas_consec += 1
					if vidas_consec == 3:
						vidas_lineas[indice] = True
						break
				else:
					vidas_consec = 0
			indice += 1
			
			
		contador = 0
		for booleano in vidas_lineas:
			if booleano == True:
				pos_min_x = self.matriz[0][0].pos[0]
				pos_min_y = self.matriz[0][0].pos[1]
				largo_fila = len(self.matriz[0])
				largo_col = len(self.matriz)
				
				if contador in (0,1):
					if contador == 0:
						pos_y = pos_min_y - 1
						linea_insert = 0
						self.filas_extra[0] += 1
					else:
						pos_y = pos_min_y + largo_col
						linea_insert = largo_col
						self.filas_extra[1] += 1
						
					nueva_fila = [Celula_opt1((x, pos_y), self) for x in range(pos_min_x, pos_min_x + largo_fila)]
					self.matriz.insert(linea_insert, nueva_fila)


				elif contador in (2,3):
					if contador == 2:
						pos_x = pos_min_x - 1
						linea_insert = 0
						self.cols_extra[0] += 1
					else:
						pos_x = pos_min_x + largo_fila
						linea_insert = largo_fila
						self.cols_extra[1] += 1

					cuenta_fila = 0
					for y in range(pos_min_y, pos_min_y + largo_col):
						self.matriz[cuenta_fila].insert(linea_insert, Celula_opt1((pos_x, y), self))
						cuenta_fila += 1

			contador += 1

	def reset(self):
		self.matriz = []
		self.celulas_vivas = []
		linea = ["" for x in range(self.grid)]
		for x in range(self.grid):
			self.matriz.append(linea.copy())
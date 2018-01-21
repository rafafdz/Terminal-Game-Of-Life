class Celula:
	def __init__(self, pos, tablero):
		self.pos = pos
		self.vida = False
		self.vida_siguiente = None
		self.skin = "o"
		self.skin_muerto = " "
		self.tablero_padre = tablero

	def __str__(self):
		if self.vida:
			return self.skin
		else:
			return self.skin_muerto

	def revisar(self):
		# Barrer primero la fila de arriba, de ahí abajo y despues los dos espacios de cada lado.
		x_inicial = self.pos[0] - 1
		cont = 0
		for x in range(3):	
			cont += self.tablero_padre.mirar((x_inicial + x, self.pos[1] - 1))
			cont += self.tablero_padre.mirar((x_inicial + x, self.pos[1] + 1))

		cont += self.tablero_padre.mirar((self.pos[0] - 1, self.pos[1]))
		cont += self.tablero_padre.mirar((self.pos[0] + 1, self.pos[1]))

		return cont

	def calcular_siguiente(self):
		alrededor = self.revisar()
		if self.vida and alrededor < 2:
			self.vida_siguiente = False

		elif self.vida and alrededor in (2,3):
			self.vida_siguiente = True

		elif self.vida and alrededor > 3: # Muerte por sobrepoblacion
			self.vida_siguiente = False

		elif not self.vida and alrededor == 3: # Nace una nueva celula
			self.vida_siguiente = True

		elif not self.vida and alrededor != 3:
			self.vida_siguiente = False

	def actualizar(self):
		self.vida = self.vida_siguiente
		self.vida_siguiente = None

	

class Celula_opt1(Celula):
	def __init__(self, pos, tablero):
		Celula.__init__(self, pos, tablero)
		self.veces_contada = 0

	def revisar(self):
		# Barrer primero la fila de arriba, de ahí abajo y despues los dos espacios de cada lado.
		offsets = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))
		pos_x, pos_y = self.pos[0], self.pos[1]
		cont = 0

		for cord in offsets:
			x, y = cord[0], cord[1]
			celula = self.tablero_padre.celula_en((pos_x + x, pos_y + y), contar = True)
			
			if celula is not None:
				cont += celula.vida

		return cont

	def actualizar(self):
		self.vida = self.vida_siguiente
		self.vida_siguiente = None

	def contar(self):
		self.veces_contada += 1

	def reset_cuenta(self):
		self.veces_contada = 0
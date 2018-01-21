from cgol import *

tabla = Tablero_opt1(200)

def bench(forma, cantidad):
	suma = 0
	for x in range(30):
		tabla.rellenar()
		t0 = perf_counter()
		if forma == 1:
			tabla.randomizar(cantidad)

		elif forma == 2:
			tabla.randomizar2(cantidad)

		elif forma == 3:
			tabla.randomizar3(cantidad)

		suma += (perf_counter() - t0)

	return suma / 30

valores = [1, 100, 500, 2500, 6000, 8000, 40000]
for valor in valores:
	b1 = bench(1, valor)
	b2 = bench(2, valor)
	b3 = bench(3, valor)
	pruebas = [b1, b2, b3]
	ordenes = pruebas.copy()
	pruebas.sort()
	print("Prueba para el valor", valor, ":")
	print("La prueba más rapida fue la", ordenes.index(pruebas[0]) + 1)
	print("Fue", ((pruebas[1] - pruebas[0]) / pruebas[1]) * 100, "% mas rapida que la", ordenes.index(pruebas[1]) + 1)
	print("-" * 20 + "\n")
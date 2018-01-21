from cgol import *

def main():

	limite_generaciones = 200
	resultados = [["" for x in range(3)] for x in range(20)]
	nombre_archivo = "prueba2.txt"
	pruebas_bench = [x for x in range(500, 10500, 500)]
	valores_limpiar = [0, 100]
	indice_max = len(valores_limpiar)
	tabla_bench = Tablero_opt1(100)

	indice_filas = 0
	for cant_celulas in pruebas_bench:
		
		indice = -1
		while indice < indice_max:
			tabla_bench.reset()
			tabla_bench.rellenar()
			tabla_bench.randomizar(None, "random.txt", cant_celulas)
			generacion = 0
			descontar = 0
			tiempo_inicial = perf_counter()
			
			while generacion < limite_generaciones:
				if indice >= 0:
					limpiar(valores_limpiar[indice])
					print(tabla_bench)

				print("Prueba en curso:", indice_filas, ":", indice + 1)
				tabla_bench.check_expansion()
				tabla_bench.refresh()
				generacion += 1

				if msvcrt.kbhit():
					tecla = msvcrt.getch()
					if tecla == b"q":
						exit()

					elif tecla == b"p":
						inicio_descuento = perf_counter()
						print("Resultdos hasta ahora: ", resultados)
						input()
						descontar += (perf_counter() - inicio_descuento)


			resultados[indice_filas][indice + 1] = perf_counter() - tiempo_inicial - descontar
			indice += 1
		indice_filas += 1


	# Escribir los resultados en archivo
	archivo_bench = open(nombre_archivo, "w")
	archivo_bench.write(repr(resultados) + "\n")
	archivo_bench.close()

if __name__ == "__main__":
	main()
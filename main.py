import numpy as np
from ida import profundizar
import tablero
import time
tama = 8
destino = np.array([
    [ 1,  2,  3,  4,  5,  6,  7,  8],
    [ 9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [49, 50, 51, 52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61, 62, 63,  0]
])
aux = destino.copy() 

tablero_final = tablero.generar_tablero(destino, 10, tama)

print("Tablero destino:")
print(aux)
print("\nTablero final:")
print(tablero_final)

print("iniciamos el algoritmo")

inicio = time.time()
camino = profundizar(tablero_final, aux,tama)
fin = time.time()

tiempo = fin - inicio

if camino:
    print(f"\nSolución encontrada en {len(camino)-1} movimientos")
    for i, paso in enumerate(camino):
        print(f"Paso {i}:")
        print(paso)
        print()
else:
    print("No se encontró solución")

print(f"\nTiempo total: {tiempo:.4f} segundos ({tiempo/60:.2f} minutos)")
import numpy as np
from ida import algoritmo 
import tablero
import time

destino = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
aux = destino.copy() 

tablero_final = tablero.generar_tablero(destino, 50, 4)

print("Tablero destino:")
print(aux)
print("\nTablero final:")
print(tablero_final)

print("iniciamos el algoritmo")

inicio = time.time()
camino = algoritmo(tablero_final, aux, 4)
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
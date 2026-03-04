from tablero import generar_tablero
import numpy as np 
import time 
from ida import profundizar


size = 4 
movimietos = 10
destino = np.array([
    [ 1,  2,  3,  4],
    [ 5,  6,  7,  8],
    [ 9, 10, 11, 12],
    [13, 14, 15,  0]
])

inicial = generar_tablero(destino.copy,movimietos,size)


inicio = time.time()
camino = profundizar(inicial,destino,4)
fin = time.time()
tiempo = fin - inicio

pasos = len(camino)

for parcial in camino:
    print(parcial)
    
print(time/60)
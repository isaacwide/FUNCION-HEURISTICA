import numpy as np
import ida 
import signal 
import time 
from ida import profundizar
TIMEOUT = 120 

class TimeoutError(Exception):
    pass

def handler_timeout(signum, frame):
    ida.set_stop()
    raise TimeoutError()

print("Recuerde que el formato es .txt y debe estar la misma carpeta")
direction = input("ingrese el nombre del archivo \n \n")

try:

    with open(direction,'r') as f :
        lineas = [l.strip() for l in f if l.strip()]

    n = int(lineas[0])
    tablero_inicial = []
    tablero_destino = []
    
    #tablero inicial 
    for i in range(1, n + 1):
        fila = list(map(int, lineas[i].split(",")))
        tablero_inicial.append(fila)
    #tablero deseado 
    for i in range(n + 1, 2 * n + 1):
        fila = list(map(int, lineas[i].split(",")))
        tablero_destino.append(fila)

    


except Exception as e :
    print(f"Error archivo no encontrado : {e}")

print(f"tamaño del tablero:{n} \n")
print(f"Tablero inical: \n{np.array(tablero_inicial)} \n")
print(f"Tablero inical: \n{np.array(tablero_destino)} \n")


try: 
    inicio = time.time()
    path = profundizar(np.array(tablero_inicial),np.array(tablero_destino),n)
    fin = time.time()
    #tiempo que se tardo el algoritmo 
    t_total = fin-inicio
    signal.alarm(0)
    
    for camino in path:
        print(camino, end=",")
    print("\n")
    print(f"|-->camino encontrado con {len(path)}")
    print(f"|-->tiempo de ejecucion {t_total:.4f}")

    

except TimeoutError:

    tiempo = TIMEOUT
    estado = "timeout"
    signal.alarm(0)
    print(f"Timeout ({TIMEOUT}s) alcanzado")

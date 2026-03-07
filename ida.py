import numpy as np
import heapq
import os 
import psutil
import gc
import threading
from evaluacion import piesas, manhathan, conflictos, completa, centro

class Nodo:
    def __init__(self, valor, heuristica, padre, move):
        self.valor = valor
        self.heuristica = heuristica
        self.padre = padre
        self.move = move
    
    def __lt__(self, other):
        return self.heuristica < other.heuristica  #
visitados = set()
path = []
limite_ram = 0.03 


_stop_flag = threading.Event()

def set_stop():
    _stop_flag.set()

def memoria():
    proceso = psutil.Process(os.getpid())
    mem_usada = proceso.memory_info().rss
    mem_total = psutil.virtual_memory().total
    return mem_usada < mem_total * limite_ram  


def encontrar_path(camino):
    movimientos = []
    for i in range(len(camino)-1):
        actual = camino[i]
        siguiente = camino[i+1]

        k = tuple(np.argwhere(actual == 0)[0])
        x , y = k 
        k_n = tuple(np.argwhere(siguiente == 0)[0])   
        xD , yd = k_n

        difx = xD - x 
        dify = yd - y

        if difx == -1:
            movimientos.append("U")
        elif difx == 1 :
            movimientos.append("D")
        elif dify == -1:
            movimientos.append("L")
        elif dify == 1:
            movimientos.append("R")
    return movimientos

def evaluacion(tablero_inicial, tablero_destino, n_movimientos, size):
    h1 = piesas.h_1(tablero_inicial, tablero_destino)
    h2 = manhathan.h_2(tablero_inicial, tablero_destino)
    h3 = conflictos.h_3(tablero_inicial, tablero_destino)
    h4 = completa.h_4(tablero_inicial, tablero_destino)
    h5 = centro.h_5(tablero_inicial, tablero_destino)
    crecimiento = size/2
    g = n_movimientos/(int(crecimiento*100))
    f = (0.05*h1 + 0.60*h2 + 0.25*h3 + 0.05*h4 + 0.05*h5) - 0.01*g 

    #print(f"h1={h1:.4f} | h2={h2:.4f} | h3={h3:.4f} | h4={h4:.4f} | h5={h5:.4f} | g={g:.4f} | f={f:.4f}")

    return f

def path_encontrado(nodo):
    path_parcial = []
    while nodo:
        path_parcial.append(nodo.valor)
        nodo = nodo.padre
    return path_parcial[::-1]

def algoritmo(tablero_inicial, tablero_destino, size):
    global abierto, abierto_dict, close
    abierto = []
    abierto_dict = {}
    close = {}
    n_movimientos = 1

    f = evaluacion(tablero_inicial, tablero_destino, n_movimientos, size)
    nodo = Nodo(tablero_inicial, f, None, n_movimientos)
    heapq.heappush(abierto, (nodo.heuristica, nodo))
    abierto_dict[tuple(tablero_inicial.flatten())] = {"heuristica": f, "padre": None}

    ultimo_x = nodo

    while abierto and memoria():
        _, x = heapq.heappop(abierto)
        ultimo_x = x  
        x_tuple = tuple(x.valor.flatten())

        if abierto_dict.get(x_tuple, {}).get("heuristica") != x.heuristica:
            continue

        del abierto_dict[x_tuple]

        if np.array_equal(x.valor, tablero_destino):
            return path_encontrado(x), x

        posiciones = tuple(np.argwhere(x.valor == 0)[0])
        i, j = posiciones

        movimientos_posibles = []

        if i > 0:
            movimientos_posibles.append((-1, 0))
        if i < size-1:
            movimientos_posibles.append((1, 0))
        if j > 0:
            movimientos_posibles.append((0, -1))
        if j < size-1:
            movimientos_posibles.append((0, 1))

        for movimiento in movimientos_posibles:
            di, dj = movimiento
            ni, nj = i + di, j + dj

            tablero_copia = x.valor.copy()
            tablero_copia[i][j], tablero_copia[ni][nj] = tablero_copia[ni][nj], tablero_copia[i][j]
            heuristica = evaluacion(tablero_copia, tablero_destino, x.move+1, size)

            new_nodo = Nodo(tablero_copia, heuristica, x, x.move+1)
            tablero_tuple = tuple(tablero_copia.flatten())

            if tablero_tuple not in abierto_dict and tablero_tuple not in close and tablero_tuple not in visitados:
                heapq.heappush(abierto, (heuristica, new_nodo))
                abierto_dict[tablero_tuple] = {"heuristica": heuristica, "padre": x}

            elif tablero_tuple in abierto_dict:
                if heuristica > abierto_dict[tablero_tuple]["heuristica"]:
                    abierto_dict[tablero_tuple] = {"heuristica": heuristica, "padre": x}
                    heapq.heappush(abierto, (heuristica, new_nodo))

            elif tablero_tuple in close:
                if heuristica > close[tablero_tuple]["heuristica"]:
                    del close[tablero_tuple]
                    heapq.heappush(abierto, (heuristica, new_nodo))
                    abierto_dict[tablero_tuple] = {"heuristica": heuristica, "padre": x}

        close[tuple(x.valor.flatten())] = {"heuristica": x.heuristica, "padre": x.padre}

    
    print("Límite de memoria alcanzado")
    
    if abierto:  
        _, x = heapq.heappop(abierto)
    else:  
        # en caso de que abierto se vacie
        x = ultimo_x

    path_parcial = path_encontrado(x)
    abierto.clear()
    abierto_dict.clear()
    close.clear()
    gc.collect()
    
    return path_parcial, x

def profundizar(tablero_inicial, tablero_destino, size):
    global visitados, path, limite_ram  
    _stop_flag.clear()  
    visitados.clear()     
    limite_ram = 0.03 
    path = []
    
    camino, nodo = algoritmo(tablero_inicial, tablero_destino, size)
    path.append(camino)
    
    for estado in camino:
        visitados.add(tuple(estado.flatten()))

    ultimo_estado = None
    

    while not np.array_equal(nodo.valor, tablero_destino):
        if _stop_flag.is_set():     
            return []
        
        
        if ultimo_estado is not None and np.array_equal(nodo.valor, ultimo_estado):
            print("Ciclo detectado, aumentando límite RAM")
            visitados.clear()
            limite_ram += 0.05  
            

        visitados.add(tuple(nodo.valor.flatten())) 
        ultimo_estado = nodo.valor.copy()
        
        print(f"Profundizando... paso {len(path)}")
        camino, nodo = algoritmo(nodo.valor, tablero_destino, size)
        path.append(camino)

        for estado in camino:
            visitados.add(tuple(estado.flatten()))

    resultado = [estado for camino in path for estado in camino]

    movements = encontrar_path(resultado)

    return movements
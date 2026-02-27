import numpy as np
import heapq
from evaluacion import piesas, manhathan, conflictos, completa, centro

class Nodo:
    def __init__(self, valor, heuristica, padre):
        self.valor = valor
        self.heuristica = heuristica
        self.padre = padre
    
    def __lt__(self, other):
        return self.heuristica > other.heuristica  # > porque maximizas

#diccionario de la soguiente manera 
# abierto {"tablero":["heuristica":n,"padre":"tablero padre"]}
abierto = [] # heap para poder simpre tener el valor menor 
abierto_dict = {}  # tablero_tuple -> heuristica -> padre 

close = {}
path = []

def evaluacion(tablero_inicial, tablero_destino, n_movimientos):
    h1 = piesas.h_1(tablero_inicial, tablero_destino)
    h2 = manhathan.h_2(tablero_inicial, tablero_destino)
    h3 = conflictos.h_3(tablero_inicial, tablero_destino)
    h4 = max(completa.h_4(tablero_inicial, tablero_destino), 0.001)
    h5 = centro.h_5(tablero_inicial, tablero_destino)

    f = (0.1*h1 - 0.1*h2 - 0.3*h3 + 0.15*(1/h4) - 0.05*h5) - 0.2*(n_movimientos/100)
    return f

def path_encontrado(nodo):
    while nodo:
        path.append(nodo.valor)
        nodo = nodo.padre
    return path[::-1]  
    

def algoritmo(tablero_inicial, tablero_destino, size):
    n_movimientos = 0

    f = evaluacion(tablero_inicial, tablero_destino, n_movimientos)
    nodo = Nodo(tablero_inicial, f, None)
    heapq.heappush(abierto, (nodo.heuristica, nodo))
    abierto_dict[tuple(tablero_inicial.flatten())] = {"heuristica": f, "padre": None}


    while abierto:
        _, x = heapq.heappop(abierto)
        x_tuple = tuple(x.valor.flatten())

        if abierto_dict.get(x_tuple, {}).get("heuristica") != x.heuristica:
            continue

        del abierto_dict[x_tuple]  # eliminar del dict

        if np.array_equal(x.valor, tablero_destino):
            return path_encontrado(x)
        
        posiciones = tuple(np.argwhere(x.valor == 0)[0])
        i, j = posiciones

        chil = []
        movimientos_posibles = []

        if i > 0:
            movimientos_posibles.append((-1, 0))
        if i < size-1:
            movimientos_posibles.append((1, 0))
        if j > 0:
            movimientos_posibles.append((0, -1))
        if j < size-1:
            movimientos_posibles.append((0, 1))

        n_movimientos += 1

        for movimiento in movimientos_posibles:
            di, dj = movimiento
            ni, nj = i + di, j + dj

            tablero_copia = x.valor.copy()
            tablero_copia[i][j], tablero_copia[ni][nj] = tablero_copia[ni][nj], tablero_copia[i][j]

            heuristica = evaluacion(tablero_copia, tablero_destino, n_movimientos)
            new_nodo = Nodo(tablero_copia, heuristica, x)
            chil.append(new_nodo)

        for c in chil:
            tablero_tuple = tuple(c.valor.flatten())#obtenemos el valor en tuplas 

            if tablero_tuple not in abierto_dict and tablero_tuple not in close:#si no esta en open si em close
                heapq.heappush(abierto, (c.heuristica, c))
                abierto_dict[tablero_tuple] = {"heuristica":c.heuristica,"padre":c.padre}

            elif tablero_tuple in abierto_dict:
                if c.heuristica > abierto_dict[tablero_tuple]["heuristica"]:  # c es mejor
                    abierto_dict[tablero_tuple] = {"heuristica": c.heuristica, "padre": c.padre} # actualizar dict
                    heapq.heappush(abierto, (c.heuristica, c))  # el viejo se ignora en el pop

            elif tablero_tuple in close:
                if c.heuristica > close[tablero_tuple]["heuristica"]:
                    del close[tablero_tuple]                    # ← eliminar de close
                    heapq.heappush(abierto, (c.heuristica, c))
                    abierto_dict[tablero_tuple] = {"heuristica": c.heuristica, "padre": c.padre} # ← tablero actual, no el inicial

        close[tuple(x.valor.flatten())]={"heuristica":x.heuristica,"padre":x.padre}


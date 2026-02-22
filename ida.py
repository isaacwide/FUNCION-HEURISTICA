
import numpy as np
import heapq # para buscar simpre el nodo mejor 
from evaluacion import piesas, manhathan, conflictos, completa, centro

#clase para cada nodo que iterara en el ida*
class Nodo:
    def __init__(self,valor,heuristica,padre):
        self.valor = valor #tablero asignado 
        self.heuristica= heuristica #heuristica del tablero
        self.padre = padre # padre el tablero directo para obtener el path


open = []
close = set() #usamos un set para guardar los close 
path = []#guardaremos nuestro path  para busqueda tabu esta lista la convertiremos en un set
#tanto inicial y destino son tableros 


def evaluacion(tablero_inicial,tablero_destino,n_movimientos):

    h1 = piesas.h_1(tablero_inicial, tablero_destino)
    h2 = manhathan.h_2(tablero_inicial, tablero_destino)
    h3 = conflictos.h_3(tablero_inicial, tablero_destino)
    h4 = max(completa.h_4(tablero_inicial, tablero_destino), 0.1)
    h5 = centro.h_5(tablero_inicial, tablero_destino)

    f = (0.1*h1 - 0.1*h2 - 0.3*h3 + 0.15*(1/h4) - 0.05*h5) - 0.2*(n_movimientos/100)

    return f

def algoritmo(tablero_inicial,tablero_destino,size):
    posiciones = tuple(np.argwhere(tablero_inicial == 0)[0])
    i, j = posiciones #posiciones de la piesa en blanco
    n_movimientos = 0 

    #evaluaciones con nuestras h 
    f = evaluacion(tablero_inicial,tablero_destino,n_movimientos)
    nodo = Nodo(tablero_inicial,f,None)
    heapq.heappush(open, (nodo.heuristica, nodo))

    while open :
        _, x = heapq.heappop(open)

        


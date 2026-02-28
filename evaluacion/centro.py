import numpy as np 

def h_5(tablero_inicial, tablero_destino):
    a = len(tablero_destino)
    centro = a // 2  
    
    valor_centro = tablero_destino[centro][centro]
    
    posicion_actual = tuple(np.argwhere(tablero_inicial == valor_centro)[0])
    posicion_i, posicion_j = posicion_actual
    
    # Distancia Manhattan desde su posición actual hasta el centro
    distancia = abs(posicion_i - centro) + abs(posicion_j - centro)
    
    posibles_vecinos = []
    if centro > 0:
        posibles_vecinos.append((-1, 0))
    if centro < a-1:
        posibles_vecinos.append((1, 0))
    if centro > 0:
        posibles_vecinos.append((0, -1))
    if centro < a-1:
        posibles_vecinos.append((0, 1))
    
    # Contar vecinos del centro que ya están bien colocados
    vecinos_correctos = 0
    for delta, gama in posibles_vecinos:
        vecino_i = centro + delta
        vecino_j = centro + gama
        
        valor_esperado = tablero_destino[vecino_i][vecino_j]
        
        valor_actual = tablero_inicial[vecino_i][vecino_j]
        
        if valor_actual == valor_esperado:
            vecinos_correctos += 1
    
    return (distancia+ vecinos_correctos)/((2*a))+4
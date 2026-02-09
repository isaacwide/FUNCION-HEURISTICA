from collections import deque
import numpy as np 
import random

def generar_tablero(resultado, movimientos):
    """
    Genera un tablero realizando movimientos aleatorios desde la posición del 0
    """
    while movimientos > 0:
        # Encontrar posición del 0
        posiciones = tuple(np.argwhere(resultado == 0)[0])
        i, j = posiciones
        
        
        # Direcciones posibles: arriba, abajo, izquierda, derecha
        movimientos_posibles = []
        
        if i > 0:  # Puede moverse arriba
            movimientos_posibles.append((-1, 0))
        if i < 3:  # Puede moverse abajo
            movimientos_posibles.append((1, 0))
        if j > 0:  # Puede moverse izquierda
            movimientos_posibles.append((0, -1))
        if j < 3:  # Puede moverse derecha
            movimientos_posibles.append((0, 1))
        
        # Elegir movimiento aleatorio
        if movimientos_posibles:
            di, dj,  = random.choice(movimientos_posibles)
            ni, nj = i + di, j + dj
            
            # Intercambiar el 0 con la ficha adyacente
            resultado[i][j], resultado[ni][nj] = resultado[ni][nj], resultado[i][j]
            
        
        
        movimientos -= 1
    
    return resultado










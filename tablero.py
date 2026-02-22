import numpy as np 
import random

def generar_tablero(resultado, movimientos,size):
    # Set para guardar estados visitados
    estados_visitados = set()
    estados_visitados.add(tuple(resultado.flatten()))
    
    movimientos_realizados = 0
    intentos_sin_avance = 0
    max_intentos = 10  # Para evitar bucles infinitos
    
    while movimientos_realizados < movimientos:
        # Encontrar posición del 0
        posiciones = tuple(np.argwhere(resultado == 0)[0])
        i, j = posiciones
        
        # Direcciones posibles: arriba, abajo, izquierda, derecha
        movimientos_posibles = []
        
        if i > 0:  # Puede moverse arriba
            movimientos_posibles.append((-1, 0))
        if i < size-1:  # Puede moverse abajo
            movimientos_posibles.append((1, 0))
        if j > 0:  # Puede moverse izquierda
            movimientos_posibles.append((0, -1))
        if j < size-1:  # Puede moverse derecha
            movimientos_posibles.append((0, 1))
        
        # Mezclar para probar en orden aleatorio
        random.shuffle(movimientos_posibles)
        
        movimiento_exitoso = False
        
        for di, dj in movimientos_posibles:
            ni, nj = i + di, j + dj
            
            resultado[i][j], resultado[ni][nj] = resultado[ni][nj], resultado[i][j]
            
            # Convertir a tupla para verificar si ya existe
            estado_actual = tuple(resultado.flatten())
            
            if estado_actual not in estados_visitados:
                # Movimiento válido, guardarlo
                estados_visitados.add(estado_actual)
                movimientos_realizados += 1
                movimiento_exitoso = True
                intentos_sin_avance = 0
                break
            else:
                # Revertir el movimiento
                resultado[ni][nj], resultado[i][j] = resultado[i][j], resultado[ni][nj]
        
        if not movimiento_exitoso:
            intentos_sin_avance += 1
            if intentos_sin_avance >= max_intentos:
                break
    
    return resultado


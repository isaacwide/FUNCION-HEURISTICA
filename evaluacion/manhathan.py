import numpy as np 

def h_2(tablero_inicial, tablero_d):
    # Calcularemos la distancia de Manhattan
    distancia = 0  
    
    for i in range(len(tablero_inicial)):
        for j in range(len(tablero_inicial[0])):
            
            valor = tablero_inicial[i][j]
        
            if valor == 0:
                continue
            
            posicion_objetivo = tuple(np.argwhere(tablero_d == valor)[0])
            objetivo_i, objetivo_j = posicion_objetivo
            
            aux = abs(i - objetivo_i) + abs(j - objetivo_j)
            distancia += aux
    
    return distancia / 64
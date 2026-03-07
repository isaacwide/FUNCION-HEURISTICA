import numpy as np 

def h_5(tablero_inicial, tablero_destino):
    a = len(tablero_destino)
    # caso cento es impar 
    #posiciones deseadas 
    if a % 2 != 0 :
        i= int((a+1)/2 )
        j= int((a+1)/2)
    else :  #caso el centro  es par 
        i = int(a/2)
        j = int((a/2)+1)

    valor_centro = tablero_destino[i][j]
    
    posicion_actual = tuple(np.argwhere(tablero_inicial == valor_centro)[0])
    posicion_i, posicion_j = posicion_actual
    
    distancia = abs(posicion_i - i) + abs(posicion_j - j)
    
    posibles_vecinos = []
    if i > 0:
        posibles_vecinos.append((-1, 0))
    if i < a-1:
        posibles_vecinos.append((1, 0))
    if j > 0:
        posibles_vecinos.append((0, -1))
    if j < a-1:
        posibles_vecinos.append((0, 1))
    
    # Contar vecinos del centro que ya están bien colocados
    vecinos_correctos = 0
    for delta, gama in posibles_vecinos:
        vecino_i = i + delta
        vecino_j = j + gama
        
        valor_esperado = tablero_destino[vecino_i][vecino_j]
        
        valor_actual = tablero_inicial[vecino_i][vecino_j]
        
        if valor_actual == valor_esperado:
            vecinos_correctos += 1
            
    peor_distancia = (i+j)-1
    return (distancia+ vecinos_correctos)/(peor_distancia+4)
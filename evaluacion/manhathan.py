import numpy as np 

def h_2(tablero_inicial,tablero_d):
    #calcularemos la distancia de manhathan
    distancia = 0  
    for i, fila in enumerate(tablero_d):
            for j, valor in enumerate(fila):
                
                valor = tablero_inicial[i][j]
                # dada una ficha a debemos calcular que tan legos esta de su posicion incial
                #buscamos donde esta la ficha ij en el segundo tablero 
                posiciones = tuple(np.argwhere(tablero_d == valor)[0])

                actuali , actualj = posiciones

                aux = abs(actuali-i) + abs(actualj-j)

                distancia = distancia + aux
    return distancia / 64

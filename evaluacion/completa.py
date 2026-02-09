import numpy as np 

def h_4(tablero_inicial, tablero_destino):
    cumple = 0
    a = len(tablero_destino)

    for i in range(a):  
        for j in range(a):
            
            # Primero checamos si la ficha ya está en la posición correcta
            if tablero_destino[i][j] == tablero_inicial[i][j]:
                # Comparamos los vecinos
                
                fichas = []  # Los vecinos posibles 

                if i > 0:  
                    fichas.append((-1, 0))
                if i < a-1:  
                    fichas.append((1, 0))
                if j > 0:  
                    fichas.append((0, -1))
                if j < a-1: 
                    fichas.append((0, 1))
                
                todos_correctos = 0  
                
                for movimiento in fichas:
                    delta, gama = movimiento
                    if  tablero_destino[i+delta][j+gama] == tablero_inicial[i+delta][j+gama]:
                        todos_correctos += 1 
                        
                
                if todos_correctos == len(fichas):
                    cumple += 1

    return cumple/16
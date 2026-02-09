import numpy as np 

def h_3(tablero_inicial, tablero_destino):
    conflictos = 0 
    pares_contados = set()  

    for i, fila in enumerate(tablero_inicial):  
        for j, valor in enumerate(fila):
            
            
            if valor == 0:
                continue
            
            
            if tablero_destino[i][j] != valor:
                valor_tablero = tablero_destino[i][j]  # Lo que debería estar aquí (en el destino)
                
                if valor_tablero == 0:
                    continue
                
                # ¿Dónde está actualmente (en tablero_inicial) la ficha que debería estar aquí?
                posiciones_en_actual = tuple(np.argwhere(tablero_inicial == valor_tablero)[0])
                
                # ¿Dónde DEBERÍA estar la ficha actual (valor) según el destino?
                posiciones_destino = tuple(np.argwhere(tablero_destino == valor)[0])
                
                # Si están intercambiadas:
                if posiciones_en_actual == posiciones_destino:
                    # Crear un par ordenado para evitar contar dos veces
                    par = tuple(sorted([valor, valor_tablero]))
                    
                    if par not in pares_contados: 
                        conflictos += 1
                        pares_contados.add(par)
    
    return conflictos / 16
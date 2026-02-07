def h_1(tablero_inicial,tablero_d):
    
    contador= 0 
    for i, fila in enumerate(tablero_d):
            for j, valor in enumerate(fila):
                if tablero_inicial[i][j] == tablero_d[i][j]:
                    contador = contador +1

    
    return contador / 16
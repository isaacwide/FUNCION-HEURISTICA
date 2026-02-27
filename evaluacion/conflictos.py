def h_3(tablero_inicial, tablero_destino):
    conflictos = 0

    # Mapa: valor -> posición destino
    pos_destino = {}
    for i in range(len(tablero_destino)):
        for j in range(len(tablero_destino[i])):
            pos_destino[tablero_destino[i][j]] = (i, j)

    size = len(tablero_inicial)

    # Conflictos lineales por FILAS
    for i in range(size):
        for j in range(size):
            val1 = tablero_inicial[i][j]
            if val1 == 0:
                continue
            fi, fj = pos_destino[val1]
            if fi != i:  # val1 no pertenece a esta fila en destino
                continue

            for k in range(j + 1, size):
                val2 = tablero_inicial[i][k]
                if val2 == 0:
                    continue
                gi, gj = pos_destino[val2]
                if gi != i:  # val2 tampoco pertenece a esta fila
                    continue

                # Ambos en la misma fila destino pero en orden invertido
                if fj > gj:
                    conflictos += 1

    # Conflictos lineales por COLUMNAS
    for j in range(size):
        for i in range(size):
            val1 = tablero_inicial[i][j]
            if val1 == 0:
                continue
            fi, fj = pos_destino[val1]
            if fj != j:  # val1 no pertenece a esta columna en destino
                continue

            for k in range(i + 1, size):
                val2 = tablero_inicial[k][j]
                if val2 == 0:
                    continue
                gi, gj = pos_destino[val2]
                if gj != j:
                    continue

                # Ambos en la misma columna destino pero en orden invertido
                if fi > gi:
                    conflictos += 1

    return conflictos / 16
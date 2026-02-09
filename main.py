import numpy as np
import matplotlib.pyplot as plt
import tablero
from evaluacion import piesas, manhathan, conflictos, completa, centro

tableros = set()
heuristica = []

# Tenemos que iniciar con dos matrices de 4 x 4
destino = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
aux = destino.copy() 

tablero_final = tablero.generar_tablero(destino, 50)

print("Tablero destino:")
print(aux)
print("\nTablero final:")
print(tablero_final)

def expandir(aux, tablero_final, profundidad, n_movimientos):
    # Caso base: detener si llegamos a profundidad 0
    if profundidad == 0:
        return
    
    posiciones = tuple(np.argwhere(tablero_final == 0)[0])
    i, j = posiciones
        
    movimientos_posibles = []
        
    if i > 0:  # Puede moverse arriba
        movimientos_posibles.append((-1, 0))
    if i < 3:  # Puede moverse abajo
        movimientos_posibles.append((1, 0))
    if j > 0:  # Puede moverse izquierda
        movimientos_posibles.append((0, -1))
    if j < 3:  # Puede moverse derecha
        movimientos_posibles.append((0, 1))

    for movimiento in movimientos_posibles:
        di, dj = movimiento
        ni, nj = i + di, j + dj  
        
        # Hacer copia para no modificar el original
        tablero_copia = tablero_final.copy()
        tablero_copia[i][j], tablero_copia[ni][nj] = tablero_copia[ni][nj], tablero_copia[i][j]
        
        tablero_tupla = tuple(tablero_copia.flatten())
        
        global tableros
        if tablero_tupla not in tableros:
            tableros.add(tablero_tupla)

            h1 = piesas.h_1(tablero_copia, aux)
            h2 = manhathan.h_2(tablero_copia, aux)
            h3 = conflictos.h_3(tablero_copia, aux)
            h4 = max(completa.h_4(tablero_copia, aux), 0.1)
            h5 = centro.h_5(tablero_copia, aux)

            global heuristica
            f = (0.1*h1 - 0.1*h2 - 0.3*h3 + 0.15*(1/h4) - 0.05*h5) - 0.2*(n_movimientos/100)
            heuristica.append(f)

            expandir(aux, tablero_copia, profundidad-1, n_movimientos+1)

expandir(aux, tablero_final, profundidad=25, n_movimientos=0)

print(f"\nTotal de estados explorados: {len(tableros)}")
print(f"Total de heurísticas calculadas: {len(heuristica)}")



plt.figure(figsize=(12, 7))

# Histograma con más detalles
n, bins, patches = plt.hist(heuristica, bins=60, edgecolor='black', alpha=0.75, color='steelblue')


cm = plt.cm.RdYlGn  
bin_centers = 0.5 * (bins[:-1] + bins[1:])
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))



# Etiquetas y título
plt.xlabel('Valor heurístico f(n)', fontsize=14, fontweight='bold')
plt.ylabel('Frecuencia (número de estados)', fontsize=14, fontweight='bold')

# Leyenda y grid
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, alpha=0.3, linestyle='--')

# Añadir texto con estadísticas
stats_text = f'Total de estados: {len(heuristica)}'
plt.text(0.98, 0.97, stats_text, transform=plt.gca().transAxes, 
         fontsize=11, verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.show()

print("\n📊 Histograma guardado como 'histograma_heuristicas.png'")
print(f"\n🏆 Valor máximo: {max(heuristica):.4f}")
print(f"📈 Promedio: {np.mean(heuristica):.4f}")
print(f"📊 Mediana: {np.median(heuristica):.4f}")
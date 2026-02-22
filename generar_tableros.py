import numpy as np
import os
import tablero

def generar_tablero_txt(size, iteraciones, num_instancias, dificultad):
    # Crear carpeta con subcarpeta de dificultad
    carpeta = f'data/{size}x{size}/{dificultad}'
    os.makedirs(carpeta, exist_ok=True)
    
    tablero_meta = np.arange(1, (size * size) + 1)
    tablero_meta[-1] = 0
    tablero_meta = tablero_meta.reshape(size, size)
    
    for i in range(num_instancias):
        tablero_inicial = tablero.generar_tablero(tablero_meta.copy(), iteraciones, size)
        
        nombre_archivo = f'{carpeta}/instancia_{i+1}.txt'
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(f'{size}\n')
            
            for fila in tablero_inicial:
                f.write(','.join(map(str, fila)) + '\n')
            
            for fila in tablero_meta:
                f.write(','.join(map(str, fila)) + '\n')
        
        print(f'Generado: {nombre_archivo}')


def generar_todos_los_tableros(num_instancias):
    
    tamanios = [3, 4, 5, 6, 7, 8]
    
    dificultades = {
        'facil':  10,
        'medio':  20,
        'dificil': 50
    }
    
    for size in tamanios:
        for dificultad, iteraciones in dificultades.items():
            print(f'\nGenerando tableros {size}x{size} - {dificultad} ({iteraciones} movimientos)...')
            generar_tablero_txt(size, iteraciones, num_instancias, dificultad)
    
generar_todos_los_tableros(num_instancias=100)

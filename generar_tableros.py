import json
import numpy as np
import tablero

def generar_tablas(size,interaciones,tableros):
    #ocuparemso esta funcion para generar tableros aleatorios un unico tablero inicial y n tableros finales 

    nuevo_tablero = np.arange(1,(size*size)+1)
    nuevo_tablero[-1]=0
    nuevo_tablero = nuevo_tablero.reshape(size,size)

    total_de_tableros = []

    for i in range(tableros):
        #generamos tablero inicial 
        tablero_aux = tablero.generar_tablero(nuevo_tablero.copy(),interaciones)

        total_de_tableros.append(tablero_aux.tolist())

    try:

        datos = {
            'tablero_inical':nuevo_tablero.tolist(),
            'instancias':total_de_tableros
        }
        with open('data/data.json','w',encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2)


    except:
        print("error en la operacion")

generar_tablas(4,50,5)
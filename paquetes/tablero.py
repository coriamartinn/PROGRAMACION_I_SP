import random

import pygame as pg


NIVELES = {
    "FACIL": {
        "tamano": 10,
        "tipos_naves": {
            "submarino": (1, 4),
            "destructor": (2, 3),
            "crucero": (3, 2),
            "acorazado": (4, 1),
        },
    },
    "MEDIO": {
        "tamano": 20,
        "tipos_naves": {
            "submarino": (1, 8),  # el doble de cada tipo
            "destructor": (2, 6),
            "crucero": (3, 4),
            "acorazado": (4, 2),
        },
    },
    "DIFICIL": {
        "tamano": 30,
        "tipos_naves": {
            "submarino": (1, 12),  # el triple de cada tipo
            "destructor": (2, 9),
            "crucero": (3, 6),
            "acorazado": (4, 3),
        },
    },
}


def crear_tablero_vacio(tamano):
    tablero = []
    for _ in range(tamano):
        fila = []
        for _ in range(tamano):
            fila.append(0)
        tablero.append(fila)
        
    return tablero


def es_posicion_valida(tablero, fila, col, tamaño, orientacion):
    es_valida = False
    if orientacion == "horizontal":
        if col + tamaño <= len(tablero[0]):
            es_valida = all(tablero[fila][c] == 0 for c in range(col, col + tamaño))
    else:
        if fila + tamaño <= len(tablero):
            es_valida = all(tablero[r][col] == 0 for r in range(fila, fila + tamaño))
    return es_valida


def colocar_nave(tablero, tamaño):
    max_intentos = 100
    exito = False  # Variable para controlar si se colocó o no

    for _ in range(max_intentos):
        fila = random.randint(0, len(tablero) - 1)
        col = random.randint(0, len(tablero[0]) - 1)
        orientacion = random.choice(["horizontal", "vertical"])
        if es_posicion_valida(tablero, fila, col, tamaño, orientacion):
            if orientacion == "horizontal":
                for c in range(col, col + tamaño):
                    tablero[fila][c] = 1
            else:
                for r in range(fila, fila + tamaño):
                    tablero[r][col] = 1
            exito = True
            break  # Salimos del for porque ya colocamos la nave
    return exito


def crear_tablero_con_naves(nivel="FACIL"):
    if nivel == "FACIL":
        dificultad = NIVELES["FACIL"]
    elif nivel == "MEDIO":
        dificultad = NIVELES["MEDIO"] 
    elif nivel == "DIFICIL":
        dificultad = NIVELES["DIFICIL"]

    tablero = crear_tablero_vacio(dificultad["tamano"])
    for tipo, (tamaño, cantidad) in dificultad["tipos_naves"].items():
        colocadas = 0
        for _ in range(cantidad):
            if colocar_nave(tablero, tamaño):
                colocadas += 1
        if colocadas < cantidad:
            print(f"Advertencia: no se colocaron todas las naves de tipo {tipo}")
    return tablero


def imprimir_tablero(pantalla, tablero):
    pg.font.init()
    fuente = pg.font.SysFont("OCR A Extended", 45)

    margen_izquierdo = 40
    margen_arriba = 40
    ancho_pantalla, alto_pantalla = pantalla.get_size()
    espacio_disponible_x = ancho_pantalla - 2 * margen_izquierdo
    espacio_disponible_y = alto_pantalla - 2 * margen_arriba
    tamano_celda = min(espacio_disponible_x // len(tablero[0]), espacio_disponible_y // len(tablero))
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            calcular_x = margen_izquierdo + columna * tamano_celda
            calcular_y = margen_arriba + fila * tamano_celda

            color_celda = (200, 200, 255)
                
            pg.draw.rect(pantalla,color_celda,(calcular_x, calcular_y, tamano_celda, tamano_celda))
            pg.draw.rect(pantalla,(0, 0, 0),(calcular_x, calcular_y, tamano_celda, tamano_celda),1)

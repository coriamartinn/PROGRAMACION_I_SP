import random
import pygame as pg
TAMANO_TABLERO = 10
TIPOS_NAVES = {
    "submarino": (1, 4),
    "destructor": (2, 3),
    "crucero": (3, 2),
    "acorazado": (4, 1),
}


def crear_tablero_vacio(tamano):
    return [[0 for _ in range(tamano)] for _ in range(tamano)]


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


def crear_tablero_con_naves():
    tablero = crear_tablero_vacio(TAMANO_TABLERO)
    for tipo, (tamaño, cantidad) in TIPOS_NAVES.items():
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
    #print(type(tablero))
    for fila in range(len(tablero)):
        y = fila * 15 + 5
        for columna in range(len(tablero)):
            x = columna * 15 + 5
            posicion_celda = (x, y)
            superficie_tablero = fuente.render("", True, (0, 0, 0))
            rect_tablero = superficie_tablero.get_rect()
            rect_tablero.center = (400, 200)
            pg.draw.rect(pantalla, (0, 0, 255), (x, y, 40, 40))
            pantalla.blit(superficie_tablero, (x+5, y+5))
        

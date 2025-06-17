import random
import pygame as pg
TAMANO_TABLERO = 10
TIPOS_NAVES = {
    "submarino": (1, 4),
    "destructor": (2, 3),
    "crucero": (3, 2),
    "acorazado": (4, 1),
}
NIVELES = {
    "FACIL": {
        "tamano": 10,
        "tipos_naves": {
            "submarino": (1, 4),
            "destructor": (2, 3),
            "crucero": (3, 2),
            "acorazado": (4, 1),
        }
    },
    "MEDIO": {
        "tamano": 20,
        "tipos_naves": {
            "submarino": (1, 8),   # el doble de cada tipo
            "destructor": (2, 6),
            "crucero": (3, 4),
            "acorazado": (4, 2),
        }
    },
    "DIFICIL": {
        "tamano": 40,
        "tipos_naves": {
            "submarino": (1, 12),  # el triple de cada tipo
            "destructor": (2, 9),
            "crucero": (3, 6),
            "acorazado": (4, 3),
        }
    },
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


def crear_tablero_con_naves(nivel="FACIL"):
    if nivel == "FACIL":
        tamano = 10
        tipos_naves = {
            "submarino": (1, 4),
            "destructor": (2, 3),
            "crucero": (3, 2),
            "acorazado": (4, 1),
        }
    elif nivel == "MEDIO":
        tamano = 20
        tipos_naves = {
            "submarino": (1, 8),   # doble cantidad
            "destructor": (2, 6),
            "crucero": (3, 4),
            "acorazado": (4, 2),
        }
    elif nivel == "DIFICIL":
        tamano = 40
        tipos_naves = {
            "submarino": (1, 12),  # triple cantidad
            "destructor": (2, 9),
            "crucero": (3, 6),
            "acorazado": (4, 3),
        }
    else:
        # Por si llega un nivel inesperado
        tamano = 10
        tipos_naves = {
            "submarino": (1, 4),
            "destructor": (2, 3),
            "crucero": (3, 2),
            "acorazado": (4, 1),
        }
    
    tablero = crear_tablero_vacio(tamano)
    for tipo, (tamaño, cantidad) in tipos_naves.items():
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
    tamano_celda = 15
    #print(type(tablero))
    for fila in range(len(tablero)):
        for columna in range(len(tablero)):
            calcular_x = margen_izquierdo + columna * tamano_celda
            calcular_y = margen_arriba + fila * tamano_celda

            if tablero[fila][columna] == 1:
                color_celda = (0, 0, 255)
            else:
                color_celda = (200, 200, 255)
                
            pg.draw.rect(pantalla, color_celda, (calcular_x, calcular_y, tamano_celda, tamano_celda))
            pg.draw.rect(pantalla, (0, 0, 0), (calcular_x, calcular_y, tamano_celda, tamano_celda), 1)

"""def imprimir_tablero(pantalla, tablero):
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
            pantalla.blit(superficie_tablero, (x+5, y+5))"""
        
            
        
            
        

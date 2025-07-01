import random
import string

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


def crear_tablero_vacio(tamano: int) -> list:
    """
    Crea un tablero de juego vacío de un tamaño especificado.

    Args:
        tamano (int): El tamaño del tablero (por ejemplo, 10 para un tablero de 10x10).

    Returns:
        list: Una lista de listas representando el tablero vacío, donde cada celda contiene un 0.
    """
    tablero = []
    for _ in range(tamano):
        fila = []
        for _ in range(tamano):
            fila.append(0)
        tablero.append(fila)

    return tablero


def es_posicion_valida(tablero: list, fila: int, col: int, tamaño: int, orientacion: str
) -> bool:
    """
    Verifica si una posición y orientación dadas son válidas para colocar una nave en el tablero.
    Una posición es válida si la nave cabe en el tablero y no se superpone con otras naves
    ni con sus zonas de seguridad (vecinos).

    Args:
        tablero (list): El tablero de juego actual.
        fila (int): La fila inicial para colocar la nave.
        col (int): La columna inicial para colocar la nave.
        tamaño (int): El tamaño de la nave.
        orientacion (str): La orientación de la nave ('horizontal' o 'vertical').

    Returns:
        bool: True si la posición es válida, False en caso contrario.
    """
    es_valida = False

    if orientacion == "horizontal":
        if col + tamaño <= len(tablero[0]):
            es_valida = True
            for c in range(col, col + tamaño):
                if tablero[fila][c] != 0:
                    es_valida = False
                    break
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf = fila + df
                        nc = c + dc
                        if 0 <= nf < len(tablero) and 0 <= nc < len(tablero[0]):
                            if tablero[nf][nc] != 0:
                                es_valida = False
                                break
                        if not es_valida:
                            break
    else:  # orientación vertical
        if fila + tamaño <= len(tablero):
            es_valida = True
            for r in range(fila, fila + tamaño):
                if tablero[r][col] != 0:
                    es_valida = False
                    break
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf = r + df
                        nc = col + dc
                        if 0 <= nf < len(tablero) and 0 <= nc < len(tablero[0]):
                            if tablero[nf][nc] != 0:
                                es_valida = False
                                break
                        if not es_valida:
                            break
    return es_valida


def colocar_nave(tablero: list, tamaño: int, id_nave: int) -> bool:
    """
    Intenta colocar una nave de un tamaño y ID específicos en una posición aleatoria válida en el tablero.

    Args:
        tablero (list): El tablero de juego.
        tamaño (int): El tamaño de la nave a colocar.
        id_nave (int): El identificador único de la nave.

    Returns:
       bool: True si la nave se colocó con éxito, False en caso contrario.
    """
    max_intentos = 100
    exito = False  # Variable para controlar si se colocó o no
    for _ in range(max_intentos):
        fila = random.randint(0, len(tablero) - 1)
        col = random.randint(0, len(tablero[0]) - 1)
        orientacion = random.choice(["horizontal", "vertical"])
        if es_posicion_valida(tablero, fila, col, tamaño, orientacion):
            if orientacion == "horizontal":
                for c in range(col, col + tamaño):
                    tablero[fila][c] = id_nave
            else:
                for r in range(fila, fila + tamaño):
                    tablero[r][col] = id_nave
            exito = True
            break  # Salimos del for porque ya colocamos la nave
    return exito


def crear_tablero_con_naves(nivel="FACIL") -> list:
    """
    Intenta colocar una nave de un tamaño y ID específicos en una posición aleatoria válida en el tablero.

    Args:
        tablero (list): El tablero de juego.
        tamaño (int): El tamaño de la nave a colocar.
        id_nave (int): El identificador único de la nave.

    Returns:
       bool: True si la nave se colocó con éxito, False en caso contrario.
    """
    if nivel == "FACIL":
        dificultad = NIVELES["FACIL"]
    elif nivel == "MEDIO":
        dificultad = NIVELES["MEDIO"]
    elif nivel == "DIFICIL":
        dificultad = NIVELES["DIFICIL"]

    tablero = crear_tablero_vacio(dificultad["tamano"])
    id_actual_nave = 2
    for tipo, (tamaño, cantidad) in dificultad["tipos_naves"].items():
        colocadas = 0
        for _ in range(cantidad):
            if colocar_nave(tablero, tamaño, id_actual_nave):
                colocadas += 1
                id_actual_nave += 1
        if colocadas < cantidad:
            print(f"Advertencia: no se colocaron todas las naves de tipo {tipo}")
    return tablero


def manejar_disparo(
    tablero: list, tablero_disparos: list, posicion: int, dimension_pantalla: tuple
) -> int:
    """
    Maneja el disparo en el tablero de juego, actualizando el tablero de disparos y calculando el puntaje.

    Args:
        tablero (list): El tablero de juego con las naves.
        tablero_disparos (list): El tablero que registra los disparos.
        posicion (int): Una tupla (x, y) de las coordenadas del clic en la pantalla.
        dimension_pantalla (tuple): Una tupla (ancho, alto) de las dimensiones de la pantalla.

    Returns:
        int: El puntaje obtenido por el disparo
    """
    margen_izquierdo = 40
    margen_arriba = 40
    ancho_pantalla, alto_pantalla = dimension_pantalla
    espacio_disponible_x = ancho_pantalla - 2 * margen_izquierdo
    espacio_disponible_y = alto_pantalla - 2 * margen_arriba
    tamano_celda = min(
        espacio_disponible_x // len(tablero[0]), espacio_disponible_y // len(tablero)
    )
    puntaje = 0

    x, y = posicion
    columna = (x - margen_izquierdo) // tamano_celda
    fila = (y - margen_arriba) // tamano_celda

    if 0 <= fila < len(tablero) and 0 <= columna < len(tablero[0]):
        if (
            tablero_disparos[fila][columna] == 0
        ):  # Si la celda no ha sido disparada #Se agrego 25/06
            valor_celda = tablero[fila][columna]

            if valor_celda == 0:  # Es agua
                tablero_disparos[fila][columna] = -1
                puntaje = -1  # Restar 1 punto por disparo al agua #Se agrego 25/06
            else:  # Es una nave (valor_celda > 1, ya que 1 era antes el marcador de nave) #Se agrego 25/06
                tablero_disparos[fila][columna] = 1  # Marcar como golpeado
                puntaje = 5  # Sumar 5 puntos por averiar la nave #Se agrego 25/06

                # Verificar si la nave fue hundida #Se agrego 25/06
                id_nave_golpeada = valor_celda  # Se agrego 25/06
                partes_totales_nave = sum(  # Se agrego 25/06
                    fila_tablero.count(id_nave_golpeada)
                    for fila_tablero in tablero  # Se agrego 25/06
                )  # Se agrego 25/06
                partes_danadas_nave = sum(  # Se agrego 25/06
                    1  # Se agrego 25/06
                    for r in range(len(tablero))  # Se agrego 25/06
                    for c in range(len(tablero[0]))  # Se agrego 25/06
                    if tablero[r][c] == id_nave_golpeada
                    and tablero_disparos[r][c] == 1  # Se agrego 25/06
                )  # Se agrego 25/06

                if partes_danadas_nave == partes_totales_nave:  # Se agrego 25/06
                    # Nave hundida, sumar 10 puntos por cada elemento de la nave #Se agrego 25/06
                    puntaje += 10 * partes_totales_nave  # Se agrego 25/06
                    celdas_barco = [
                        (r, c)
                        for r in range(len(tablero))
                        for c in range(len(tablero[0]))
                        if tablero[r][c] == id_nave_golpeada
                    ]

                    celdas_agua = obtener_vecinos_agua(
                        tablero, tablero_disparos, celdas_barco
                    )
                    for fila, columna in celdas_agua:
                        tablero_disparos[fila][columna] = -1
    return puntaje


def obtener_vecinos_agua(
    tablero: list, tablero_disparos: list, celdas_barco: tuple
) -> tuple:
    """
    Obtiene las coordenadas de las celdas de "agua" adyacentes a una nave hundida que aún no han sido marcadas.
    Args:
        tablero (list): El tablero de juego con las naves.
        tablero_disparos (list): El tablero que registra los disparos.
        celdas_barco (tuple): Una tupla de tuplas (fila, columna) que representan las celdas ocupadas por la nave hundida.
    Returns:
        tuple: Una tupla de tuplas (fila, columna) de las celdas de agua adyacentes.
    """
    vecinos_agua = set()  # guardar coordenadas celdas agua
    barco = set(
        celdas_barco
    )  # para hacer mas facil la busqueda de las celdas donde existe un barco
    filas = len(tablero)
    columnas = len(tablero[0])

    for fila, columna in celdas_barco:
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0:
                    continue
                f = fila + df
                c = columna + dc

                if (
                    0 <= f < filas
                    and 0 <= c < columnas
                    and (f, c) not in barco
                    and tablero[f][c] == 0
                    and tablero_disparos[f][c] == 0
                ):
                    vecinos_agua.add((f, c))

    return list(vecinos_agua)


def disparo_acertado(
    tablero: list, tablero_disparos: list, posicion: tuple, dimension_pantalla: tuple
) -> bool:
    """
    Verifica si un disparo en una posición dada impactaría una nave que aún no ha sido disparada.

    Args:
        tablero (list): El tablero de juego con las naves.
        tablero_disparos (list): El tablero que registra los disparos.
        posicion (tuple): Una tupla (x, y) de las coordenadas del clic en la pantalla.
        dimension_pantalla (tuple): Una tupla de las dimensiones de la pantalla.

    Returns:
        bool: True si el disparo es un acierto en una celda no disparada, False en caso contrario.
    """
    acertado = False
    margen_izquierdo = 40
    margen_arriba = 40
    ancho_pantalla, alto_pantalla = dimension_pantalla
    espacio_disponible_x = ancho_pantalla - 2 * margen_izquierdo
    espacio_disponible_y = alto_pantalla - 2 * margen_arriba
    tamano_celda = min(
        espacio_disponible_x // len(tablero[0]), espacio_disponible_y // len(tablero)
    )

    x, y = posicion
    columna = (x - margen_izquierdo) // tamano_celda
    fila = (y - margen_arriba) // tamano_celda

    if 0 <= fila < len(tablero) and 0 <= columna < len(tablero[0]):
        if tablero_disparos[fila][columna] == 0:
            if tablero[fila][columna] != 0:
                acertado = True

    return acertado


def imprimir_tablero(
    pantalla: pg.display, tablero: list, tablero_disparos=None, info_naves=None
) -> None:
    """
    Dibuja el tablero de juego en la pantalla de Pygame, incluyendo las naves, los disparos y las coordenadas del tablero.

    Args:
        pantalla (pg.display): El objeto de display de Pygame donde se dibujará el tablero.
        tablero (list): El tablero de juego con las naves.
        tablero_disparos (list, optional): El tablero que registra los disparos.
        info_naves (dict, optional): Un diccionario con información sobre los tipos de naves,utilizado para mostrar las iniciales de las naves.
    """
    if tablero_disparos is None:
        tablero_disparos = crear_tablero_vacio(len(tablero))
    pg.font.init()
    fuente = pg.font.SysFont("OCR A Extended", 45)

    margen_izquierdo = 40
    margen_arriba = 40
    ancho_pantalla, alto_pantalla = pantalla.get_size()
    tamano_celda = min(
        (ancho_pantalla - 2 * margen_izquierdo) // len(tablero[0]),
        (alto_pantalla - 2 * margen_arriba) // len(tablero),
    )

    fuente_celda = pg.font.SysFont("Arial", int(tamano_celda * 0.7))
    fuente_coord = pg.font.SysFont("Arial", tamano_celda // 2)
    # Dibujar números columnas arriba
    for col in range(len(tablero[0])):
        numero = str(col + 1)
        texto_numero = fuente_coord.render(numero, True, (255, 255, 255))
        x = (
            margen_izquierdo
            + col * tamano_celda
            + tamano_celda // 2
            - texto_numero.get_width() // 2
        )
        y = margen_arriba // 2 - texto_numero.get_height() // 2
        pantalla.blit(texto_numero, (x, y))

    # Letras filas a la izquierda
    letras = string.ascii_uppercase
    for fila in range(len(tablero)):
        letra = letras[fila] if fila < len(letras) else "?"
        texto_letra = fuente_coord.render(letra, True, (255, 255, 255))
        x = margen_izquierdo // 2 - texto_letra.get_width() // 2
        y = (
            margen_arriba
            + fila * tamano_celda
            + tamano_celda // 2
            - texto_letra.get_height() // 2
        )
        pantalla.blit(texto_letra, (x, y))

    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            calcular_x = margen_izquierdo + columna * tamano_celda
            calcular_y = margen_arriba + fila * tamano_celda

            color_celda = (200, 200, 255)
            contenido_celda = None

            if tablero_disparos[fila][columna] == 1:
                color_celda = (255, 0, 0)  # impacto (rojo)
                id_nave_golpeada = tablero[fila][columna]

                if (
                    id_nave_golpeada > 0
                    and info_naves is not None
                    and id_nave_golpeada in info_naves
                ):
                    tipo_nave = info_naves[id_nave_golpeada]["tipo"]
                    contenido_celda = tipo_nave[0].upper()

            elif tablero_disparos[fila][columna] == -1:
                color_celda = (0, 148, 218)  # agua (celeste)

            pg.draw.rect(
                pantalla,
                color_celda,
                (calcular_x, calcular_y, tamano_celda, tamano_celda),
            )
            pg.draw.rect(
                pantalla,
                (0, 0, 0),
                (calcular_x, calcular_y, tamano_celda, tamano_celda),
                1,
            )

            if contenido_celda:
                texto_letra_nave = fuente_celda.render(
                    contenido_celda, True, (255, 255, 255)
                )
                rect_texto_letra_nave = texto_letra_nave.get_rect(
                    center=(
                        calcular_x + tamano_celda // 2,
                        calcular_y + tamano_celda // 2,
                    )
                )
                pantalla.blit(texto_letra_nave, rect_texto_letra_nave)

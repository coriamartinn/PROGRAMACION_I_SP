import pygame as pg
from operator import itemgetter

from paquetes.archivos import *
from paquetes.tablero import *
from paquetes.validates import *

def menu(pantalla: pg.display, nivel_actual="FACIL"):
    jugar = "Jugar"
    nivel = "Nivel"
    puntaje = "Puntajes"
    salir = "Salir"
    musica = "On/Off"
    padding_x = 20
    padding_y = 15

    pg.font.init()
    fuente = pg.font.SysFont("OCR A Extended", 45)
    fuente_titulo = pg.font.SysFont("OCR A Extended", 90)
    fuente_alternativa = pg.font.SysFont("OCR A Extended", 25)

    # Superficies de texto
    superficie_titulo = fuente_titulo.render("Batalla Naval", True, (255, 255, 255))
    superficie_jugar = fuente.render(jugar, True, (255, 255, 255))
    superficie_nivel = fuente.render(nivel, True, (255, 255, 255))
    superficie_puntaje = fuente.render(puntaje, True, (255, 255, 255))
    superficie_salir = fuente.render(salir, True, (255, 255, 255))
    superficie_musica = fuente_alternativa.render(musica, True, (255, 255, 255))

    # Obtener rects
    rect_titulo = superficie_titulo.get_rect()
    rect_jugar = superficie_jugar.get_rect()
    rect_nivel = superficie_nivel.get_rect()
    rect_puntajes = superficie_puntaje.get_rect()
    rect_salir = superficie_salir.get_rect()
    rect_musica = superficie_musica.get_rect()

    # Centrar posiciones
    rect_titulo.center = (512, 120)
    rect_jugar.center = (512, 284)
    rect_nivel.center = (512, 384)
    rect_puntajes.center = (512, 484)
    rect_salir.center = (512, 584)
    rect_musica.center = (959, 726)

    # Fondos con padding
    fondo_titulo = pg.Rect(
        rect_titulo.left - padding_x,
        rect_titulo.top - padding_y,
        rect_titulo.width + 2 * padding_x,
        rect_titulo.height + 2 * padding_y,
    )
    fondo_jugar = pg.Rect(
        rect_jugar.left - padding_x,
        rect_jugar.top - padding_y,
        rect_jugar.width + 2 * padding_x,
        rect_jugar.height + 2 * padding_y,
    )
    fondo_nivel = pg.Rect(
        rect_nivel.left - padding_x,
        rect_nivel.top - padding_y,
        rect_nivel.width + 2 * padding_x,
        rect_nivel.height + 2 * padding_y,
    )
    fondo_puntajes = pg.Rect(
        rect_puntajes.left - padding_x,
        rect_puntajes.top - padding_y,
        rect_puntajes.width + 2 * padding_x,
        rect_puntajes.height + 2 * padding_y,
    )
    fondo_salir = pg.Rect(
        rect_salir.left - padding_x,
        rect_salir.top - padding_y,
        rect_salir.width + 2 * padding_x,
        rect_salir.height + 2 * padding_y,
    )
    fondo_musica = pg.Rect(
        rect_musica.left - padding_x,
        rect_musica.top - padding_y,
        rect_musica.width + 2 * padding_x,
        rect_musica.height + 2 * padding_y,
    )

    # Dibujar fondos
    color_fondo = (4, 6, 88)
    pg.draw.rect(pantalla, color_fondo, fondo_titulo, border_radius=15)
    pg.draw.rect(pantalla, color_fondo, fondo_jugar, border_radius=15)
    pg.draw.rect(pantalla, color_fondo, fondo_nivel, border_radius=15)
    pg.draw.rect(pantalla, color_fondo, fondo_puntajes, border_radius=15)
    pg.draw.rect(pantalla, color_fondo, fondo_salir, border_radius=15)
    pg.draw.rect(pantalla, color_fondo, fondo_musica, border_radius=15)

    # Dibujar textos
    pantalla.blit(superficie_titulo, rect_titulo)
    pantalla.blit(superficie_jugar, rect_jugar)
    pantalla.blit(superficie_nivel, rect_nivel)
    pantalla.blit(superficie_puntaje, rect_puntajes)
    pantalla.blit(superficie_salir, rect_salir)
    pantalla.blit(superficie_musica, rect_musica)

    # Retornamos todos los rects para control de clics
    return rect_jugar, rect_nivel, rect_puntajes, rect_salir, rect_musica


def interfaz_jugar(
    pantalla: pg.display,
    tablero: list,
    tablero_disparos: list,
    puntaje_jugador: int,
    puntaje_jugador_vivo: int,
    nombre_jugador,
    nivel="FACIL",
) -> None:
    """
    Esta funcion se encarga de dibujar en pantalla la interfaz del interfaz principal
    Args:
        pantalla (pg.display): Recibe el display de pantalla
    Returns:
        None: No existe retorno
    """
    if nivel != "FACIL" and nivel != "MEDIO" and nivel != "DIFICIL":
        nivel = "FACIL"
    if tablero is None:
        tablero = crear_tablero_con_naves(nivel)
    if tablero_disparos is None:
        tablero_disparos = crear_tablero_vacio(len(tablero))

    imprimir_tablero(pantalla, tablero, tablero_disparos)
    # Crear botón "Volver"
    pg.font.init()
    fuente = pg.font.SysFont("OCR A Extended", 30)
    texto_volver = fuente.render("Volver", True, (255, 255, 255))
    rect_volver = texto_volver.get_rect(center=(950, 738))
    fondo_volver = pg.Rect(
        rect_volver.left - 10,
        rect_volver.top - 10,
        rect_volver.width + 20,
        rect_volver.height + 20,
    )
    pg.draw.rect(pantalla, (88, 6, 6), fondo_volver, border_radius=12)
    pantalla.blit(texto_volver, rect_volver)

    # Mostrar nombre jugador en pantalla
    fuente_nombre = pg.font.SysFont("OCR A Extended", 30)
    texto_nombre = fuente_nombre.render(
        f"Jugador: {nombre_jugador}", True, (255, 255, 255)
    )
    pantalla.blit(texto_nombre, (737, 12))

    # Mostrar Puntajes en vivo
    fuente_puntaje = pg.font.SysFont("OCR A Extended", 35)
    texto_puntaje = fuente_puntaje.render(
        f"PUNTAJE: {puntaje_jugador}{puntaje_jugador}{puntaje_jugador}{puntaje_jugador_vivo}",
        True,
        (255, 255, 255),
    )
    pantalla.blit(texto_puntaje, (754, 55))

    # Botón Reiniciar
    texto_reiniciar = fuente.render("Reiniciar", True, (255, 255, 255))
    rect_reiniciar = texto_reiniciar.get_rect(center=(839, 738))
    fondo_reiniciar = pg.Rect(
        rect_reiniciar.left - 10,
        rect_reiniciar.top - 10,
        rect_reiniciar.width + 20,
        rect_reiniciar.height + 20,
    )
    pg.draw.rect(pantalla, (6, 88, 6), fondo_reiniciar, border_radius=12)
    pantalla.blit(texto_reiniciar, rect_reiniciar)

    return fondo_volver, fondo_reiniciar


def interfaz_puntajes(pantalla: pg.display, ruta) -> None:
    """
    Esta funcion se encarga de dibujar en pantalla la interfaz del interfaz principal
    Args:
        pantalla (pg.display): Recibe el display de pantalla
    Returns:
        None: No existe retorno
    """
    jugadores = leer_json(ruta)
    puntajes = list(jugadores.items())
    puntajes.sort(key=itemgetter(1), reverse=True)

    puntaje = " TOP puntajes"
    padding_x = 20
    padding_y = 15

    fuente = pg.font.SysFont("OCR A Extended", 70)
    fuente_alternativa = pg.font.SysFont("OCR A Extended", 25)
    fuente_jugadores = pg.font.SysFont("OCR A Extended", 45)
    # Creamos superficie
    superficie_puntajes = fuente.render(puntaje, True, (255, 255, 255))
    texto_volver = fuente_alternativa.render("Volver", True, (255, 255, 255))

    # Obtengo el RECT de la superficie
    rect_puntaje = superficie_puntajes.get_rect()
    rect_volver = texto_volver.get_rect()

    rect_puntaje.center = (512, 100)
    rect_volver.center = (970, 738)

    # Creamos el fondo
    color_fondo = (4, 6, 88)
    fondo_puntaje = pg.Rect(
        rect_puntaje.left - padding_x,
        rect_puntaje.top - padding_y,
        rect_puntaje.width + 2 * padding_x,
        rect_puntaje.height + 2 * padding_y,
    )
    fondo_volver = pg.Rect(
        rect_volver.left - 10,
        rect_volver.top - 10,
        rect_volver.width + 20,
        rect_volver.height + 20,
    )
    y = 250
    for puntaje in puntajes:
        texto = f"{puntaje[0]}: {puntaje[1]} pts"
        superficie_jugador = fuente_jugadores.render(texto, True, (255, 255, 255))
        rect_jugador = superficie_jugador.get_rect()
        rect_jugador.center = (512, y)
        fondo_jugador = pg.Rect(
            rect_jugador.left - 10,
            rect_jugador.top - 10,
            rect_jugador.width + 20,
            rect_jugador.height + 20,
        )
        if y < 550:
            pg.draw.rect(pantalla, color_fondo, fondo_jugador, border_radius=15)
            pantalla.blit(superficie_jugador, rect_jugador)
            y += 100

    # Centro la posicion de la superficie -> (texto creado)

    pg.draw.rect(pantalla, color_fondo, fondo_puntaje, border_radius=15)
    pg.draw.rect(pantalla, (88, 6, 6), fondo_volver, border_radius=12)
    # Dibujamos en pantalla
    pantalla.blit(superficie_puntajes, rect_puntaje)
    pantalla.blit(texto_volver, rect_volver)
    
    return rect_volver


def interfaz_nivel(pantalla: pg.display, fondo, dimensiones: tuple) -> None:
    # Dibuja tres botones: Fácil, Medio, Difícil
    # Devuelve los rects de esos botones para detectar clicks
    padding_x = 20
    padding_y = 15

    fuente = pg.font.SysFont("OCR A Extended", 45)
    fuente_alternativa = pg.font.SysFont("OCR A Extended", 25)
    facil = fuente.render("Fácil", True, (255, 255, 255))
    medio = fuente.render("Medio", True, (255, 255, 255))
    dificil = fuente.render("Difícil", True, (255, 255, 255))
    texto_volver = fuente_alternativa.render("Volver", True, (255, 255, 255))

    rect_facil = facil.get_rect()
    rect_medio = medio.get_rect()
    rect_dificil = dificil.get_rect()
    rect_volver = texto_volver.get_rect()
    
    rect_facil.center = (512, 250)
    rect_medio.center = (512, 350)
    rect_dificil.center = (512, 450)
    rect_volver.center = (970, 738)

    color_fondo = (4, 6, 88)
    fondo_facil = pg.Rect(
        rect_facil.left - padding_x,
        rect_facil.top - padding_y,
        rect_facil.width + 2 * padding_x,
        rect_facil.height + 2 * padding_y,
    )
    fondo_medio = pg.Rect(
        rect_medio.left - padding_x,
        rect_medio.top - padding_y,
        rect_medio.width + 2 * padding_x,
        rect_medio.height + 2 * padding_y,
    )
    fondo_dificil = pg.Rect(
        rect_dificil.left - padding_x,
        rect_dificil.top - padding_y,
        rect_dificil.width + 2 * padding_x,
        rect_dificil.height + 2 * padding_y,
    )
    fondo_volver = pg.Rect(
        rect_volver.left - 10,
        rect_volver.top - 10,
        rect_volver.width + 20,
        rect_volver.height + 20,
    )
    
    
    pantalla.blit(fondo, (0, 0))  # Fondo lindo

    pg.draw.rect(pantalla, color_fondo, fondo_facil, border_radius=15)
    pg.draw.rect(pantalla, color_fondo, fondo_medio, border_radius=15)
    pg.draw.rect(pantalla, color_fondo, fondo_dificil, border_radius=15)
    pg.draw.rect(pantalla, (88, 6, 6), fondo_volver, border_radius=12)
    
    pantalla.blit(texto_volver, rect_volver)
    pantalla.blit(facil, rect_facil)
    pantalla.blit(medio, rect_medio)
    pantalla.blit(dificil, rect_dificil)

    return rect_facil, rect_medio, rect_dificil, rect_volver


def mostrar_selector_nivel(pantalla: pg.Surface) -> tuple:
    """
    Dibuja la pantalla de selección de nivel y retorna los rects para detectar clics.
    """
    pg.font.init()
    fuente = pg.font.SysFont("OCR A Extended", 40)

    opciones = {
        "FACIL": fuente.render("FACIL", True, (255, 255, 255)),
        "MEDIO": fuente.render("MEDIO", True, (255, 255, 255)),
        "DIFICIL": fuente.render("DIFICIL", True, (255, 255, 255)),
    }

    rects = {}
    y = 180
    for nombre, superficie in opciones.items():
        rect = superficie.get_rect(center=(400, y))
        fondo = pg.Rect(
            rect.left - 20, rect.top - 15, rect.width + 40, rect.height + 30
        )
        pg.draw.rect(pantalla, (50, 50, 200), fondo, border_radius=10)
        pantalla.blit(superficie, rect)
        rects[nombre] = rect
        y += 100

    return rects["FACIL"], rects["MEDIO"], rects["DIFICIL"]

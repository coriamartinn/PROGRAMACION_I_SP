from pygame import mixer

from paquetes.archivos import *
from paquetes.interfaces import *
from paquetes.tablero import *
from paquetes.validates import *


def jugar(
    pantalla,
    evento,
    estado,
    tablero_actual,
    tablero_disparos,
    puntaje_jugador,
    puntaje_jugador_vivo,
    nombre_jugador,
    nivel_actual,
    datos_jugadores,
    ruta,
):
    """
    Controla la lógica principal del juego durante el estado 'JUGAR'.

    Inicializa los tableros si no existen, gestiona los eventos de clic para jugar, reiniciar
    o volver al menú, actualiza el puntaje y verifica la condición de victoria.

    Args:
        pantalla (Surface): La ventana donde se renderiza el juego.
        evento (Event): El evento actual capturado por Pygame.
        estado (str): El estado actual del juego.
        tablero_actual (list): El tablero con las naves colocadas.
        tablero_disparos (list): El tablero que registra los disparos realizados.
        puntaje_jugador (int): Puntaje total acumulado del jugador.
        puntaje_jugador_vivo (int): Puntaje acumulado en la partida actual.
        nombre_jugador (str): Nombre del jugador.
        nivel_actual (str): Nivel de dificultad actual.
        datos_jugadores (dict): Diccionario con datos de jugadores y puntajes.
        ruta (str): Ruta al archivo JSON donde se guardan los puntajes.

    Returns:
        tuple: Contiene el nuevo estado, tablero_actual actualizado, tablero_disparos actualizado,
               puntaje_jugador_vivo actualizado, y click_procesado (bool).
    """
    if tablero_actual is None:
        tablero_actual = crear_tablero_con_naves(nivel_actual)
        tablero_disparos = crear_tablero_vacio(len(tablero_actual))

    rect_volver, rect_reiniciar = interfaz_jugar(
        pantalla,
        tablero_actual,
        tablero_disparos,
        puntaje_jugador,
        puntaje_jugador_vivo,
        nombre_jugador,
        nivel_actual,
    )
    """
    Gestiona la entrada del nombre del jugador en el estado 'NOMBRE'.

    Permite capturar letras, borrar con Backspace y confirma el nombre al presionar Enter,
    siempre que el nombre tenga 3 caracteres.

    Args:
        pantalla (Surface): La ventana donde se renderiza el juego.
        evento (Event): El evento actual capturado por Pygame.
        nombre_jugador (str): Nombre actual introducido por el jugador.

    Returns:
        tuple: Nuevo estado (str) y nombre_jugador actualizado (str).
    """

    click_procesado = False

    if evento.type == pg.MOUSEBUTTONDOWN and evento.button == 1:
        posicion = pg.mouse.get_pos()

        if rect_volver and rect_volver.collidepoint(posicion):
            estado = "MENU"
        elif rect_reiniciar and rect_reiniciar.collidepoint(posicion):
            tablero_actual = crear_tablero_con_naves(nivel_actual)
            tablero_disparos = crear_tablero_vacio(len(tablero_actual))
            puntaje_jugador_vivo = 0
        else:
            puntaje = manejar_disparo(
                tablero_actual,
                tablero_disparos,
                posicion,
                pantalla.get_size(),
            )
            puntaje_jugador_vivo += puntaje

        if verificar_victoria(tablero_actual, tablero_disparos):
            datos_jugadores[nombre_jugador] = puntaje_jugador_vivo
            guardar_json(ruta, datos_jugadores)
            estado = "MENU"
            tablero_actual = None
            tablero_disparos = None
            puntaje_jugador_vivo = 0

        click_procesado = True

    return (
        estado,
        tablero_actual,
        tablero_disparos,
        puntaje_jugador_vivo,
        click_procesado,
    )


def estado_nombre(pantalla, evento, nombre_jugador):
    nuevo_estado = "NOMBRE"

    if evento.type == pg.KEYDOWN:
        if evento.key == pg.K_BACKSPACE:
            nombre_jugador = nombre_jugador[:-1]
        elif evento.key == pg.K_RETURN and len(nombre_jugador) == 3:
            nuevo_estado = "JUGAR"
        elif len(nombre_jugador) < 3 and evento.unicode.isalpha():
            nombre_jugador += evento.unicode.upper()

    return nuevo_estado, nombre_jugador


def manejar_evento_estado(
    evento, estado, nombre_jugador, musica_activada, nivel_actual, rects
):
    """
    Gestiona los eventos de clic según el estado actual del juego.

    Cambia el estado del juego, el nombre del jugador, el nivel de dificultad y el estado de la música
    dependiendo del área de la pantalla clickeada.

    Args:
        evento (Event): Evento actual capturado por Pygame.
        estado (str): Estado actual del juego.
        nombre_jugador (str): Nombre del jugador.
        musica_activada (bool): Indicador si la música está activada o no.
        nivel_actual (str): Nivel de dificultad actual.
        rects (dict): Diccionario con rectángulos clickeables según el estado.

    Returns:
        tuple: Nuevo estado (str), nombre_jugador actualizado (str), estado de la música (bool),
               y nivel_actual actualizado (str).
    """
    nuevo_estado = estado
    nuevo_nombre = nombre_jugador
    nuevo_nivel = nivel_actual
    nueva_musica = musica_activada
    reset_nombre = False

    if estado == "MENU":
        nuevo_estado, nueva_musica, reset_nombre = manejar_click_menu(
            evento.pos, rects, musica_activada
        )
        if reset_nombre:
            nuevo_nombre = ""

    elif estado == "NIVEL":
        nuevo_estado, nivel = manejar_click_nivel(evento.pos, rects)
        if nivel:
            nuevo_nivel = nivel

    elif estado == "PUNTAJES":
        if rects.get("volver") and rects["volver"].collidepoint(evento.pos):
            nuevo_estado = "MENU"

    return nuevo_estado, nuevo_nombre, nueva_musica, nuevo_nivel


def manejar_click_menu(posicion_click, rects, musica_activada):
    """
    Maneja los clics en el menú principal del juego.

    Detecta si se clickeó en opciones como jugar, cambiar nivel, ver puntajes, salir o activar/desactivar música,
    y devuelve el nuevo estado, el estado de la música y si se debe resetear el nombre.

    Args:
        posicion_click (tuple): Coordenadas (x, y) del clic del ratón.
        rects (dict): Diccionario con rectángulos para las opciones del menú.
        musica_activada (bool): Estado actual de la música.

    Returns:
        tuple: Nuevo estado (str), estado actualizado de la música (bool), y reset_nombre (bool).
    """
    nuevo_estado = "MENU"
    reset_nombre = False

    if rects["jugar"] and rects["jugar"].collidepoint(posicion_click):
        nuevo_estado = "NOMBRE"
        reset_nombre = True
    elif rects["nivel"].collidepoint(posicion_click):
        nuevo_estado = "NIVEL"
    elif rects["puntajes"].collidepoint(posicion_click):
        nuevo_estado = "PUNTAJES"
    elif rects["salir"].collidepoint(posicion_click):
        nuevo_estado = "SALIR"
    elif rects["musica"].collidepoint(posicion_click):
        if musica_activada:
            mixer.pause()
            musica_activada = False
        else:
            mixer.unpause()
            musica_activada = True

    return nuevo_estado, musica_activada, reset_nombre


def manejar_click_nivel(posicion_click, rects):
    """
    Maneja los clics en la pantalla de selección de nivel.

    Cambia el nivel de dificultad y el estado según el botón clickeado, o vuelve al menú.

    Args:
        posicion_click (tuple): Coordenadas (x, y) del clic del ratón.
        rects (dict): Diccionario con rectángulos para las opciones de nivel.

    Returns:
        tuple: Nuevo estado (str) y nuevo nivel seleccionado (str o None).
    """
    nuevo_estado = "NIVEL"
    nuevo_nivel = None

    if rects["facil"].collidepoint(posicion_click):
        nuevo_nivel = "FACIL"
        nuevo_estado = "MENU"
    elif rects["medio"].collidepoint(posicion_click):
        nuevo_nivel = "MEDIO"
        nuevo_estado = "MENU"
    elif rects["dificil"].collidepoint(posicion_click):
        nuevo_nivel = "DIFICIL"
        nuevo_estado = "MENU"
    elif rects["volver"].collidepoint(posicion_click):
        nuevo_estado = "MENU"

    return nuevo_estado, nuevo_nivel

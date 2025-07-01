import pygame as pg
import pygame.mixer as mixer

from paquetes.interfaces import *
from paquetes.logica import *
from paquetes.tablero import *


def main() -> None:
    """
    Esta funcion realiza la ejecucion del juego de una forma mas ordenada
    Args:
        No hay argumentos
    Returns:
        None: no existe retorno
    """

    # Inicializamos juego y musica
    pg.init()
    mixer.init()

    # Ordenamos musica
    sonido = mixer.Sound("estaticos/sonidos/menu.mp3")
    sonido.set_volume(0.2)  # PONER VOLUMEN 0.4
    sonido.play(-1)

    # CONFIGURACION DE PANTALLA
    DIMENSIONES = (1024, 768)
    pantalla = pg.display.set_mode(DIMENSIONES)
    titulo = pg.display.set_caption(
        "Batalla naval"
    )  # -> TITULO DEL EJECUTABLE (DEL JUEGO)
    icono_surface = pg.image.load("estaticos/imagenes/icono.png")
    pg.display.set_icon(icono_surface)  # -> ICONO DEL JUEGO

    # variables
    estado = "MENU"
    nivel_actual = "FACIL"  # Nivel por defecto
    musica_activada = True
    tablero_actual = None
    tablero_disparos = None
    rect_reiniciar = None
    nombre_jugador = ""  # inicia vacio
    puntaje_jugador = 0  # inicia en 0 -> (puede bajar a negativo)
    puntaje_jugador_vivo = 0
    ruta = "estaticos/archivos/puntajes.json"
    datos_jugadores = {}
    click_procesado = False

    # CREACION DE IMAGEN -> (FONDO)
    fondo = pg.image.load("estaticos/imagenes/fondo.jpg")  # MODIFICAR FONDO
    fondo = pg.transform.scale(fondo, DIMENSIONES)

    # BUCLE PRINCIPAL DEL JUEGO
    while True:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                quit()

            if estado == "NOMBRE":
                estado, nombre_jugador = estado_nombre(pantalla, evento, nombre_jugador)

            if evento.type == pg.MOUSEBUTTONUP and evento.button == 1:
                click_procesado = False
                rects = {}

                if estado == "MENU":
                    rects = {
                        "jugar": rect_jugar,
                        "nivel": rect_nivel,
                        "puntajes": rect_puntajes,
                        "salir": rect_salir,
                        "musica": rect_musica,
                    }
                elif estado == "NIVEL":
                    rects = {
                        "facil": rect_facil,
                        "medio": rect_medio,
                        "dificil": rect_dificil,
                        "volver": rect_volver,
                    }
                elif estado == "PUNTAJES":
                    rects = {"volver": rect_volver}

                estado, nombre_jugador, musica_activada, nivel_actual = (
                    manejar_evento_estado(
                        evento,
                        estado,
                        nombre_jugador,
                        musica_activada,
                        nivel_actual,
                        rects,
                    )
                )

        pantalla.blit(fondo, (0, 0))  # pintamos el fondo de la pantalla

        match estado:
            case "MENU":
                rect_jugar, rect_nivel, rect_puntajes, rect_salir, rect_musica = menu(
                    pantalla, nivel_actual
                )
            case "NOMBRE":
                interfaz_nombre(pantalla, nombre_jugador)
            case "JUGAR":
                (
                    estado,
                    tablero_actual,
                    tablero_disparos,
                    puntaje_jugador_vivo,
                    click_procesado,
                ) = jugar(
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
                )

            case "PUNTAJES":
                rect_volver = interfaz_puntajes(pantalla, ruta)
            case "NIVEL":
                rect_facil, rect_medio, rect_dificil, rect_volver = interfaz_nivel(
                    pantalla, fondo, DIMENSIONES
                )
            case "SALIR":
                pg.quit()
                quit()

        pg.display.flip()  # actualizamos la pantalla


main()  # llamado a la ejecución

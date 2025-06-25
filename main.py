import pygame as pg
import pygame.mixer as mixer

from paquetes.interfaces import *
from paquetes.tablero import *

# from paquetes.usuario import *
#from paquetes.validates import verificar_estado


def main() -> None:
    """
    Esta funcion realiza la ejecucion del juego de una forma mas ordenada
    """

    # Inicializamos juego y musica
    pg.init()
    mixer.init()

    # Ordenamos musica
    sonido = mixer.Sound("estaticos/sonidos/menu.mp3")
    sonido.set_volume(0)  # PONER VOLUMEN 0.4
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
                # Manejar ingreso de texto
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    elif evento.key == pg.K_RETURN:
                        # Termina ingreso si tiene 3 letras
                        if len(nombre_jugador) == 3:
                            estado = "JUGAR"
                    else:
                        if len(nombre_jugador) < 3 and evento.unicode.isalpha():
                            nombre_jugador += evento.unicode.upper()

            if evento.type == pg.MOUSEBUTTONUP and evento.button == 1:
                posicion_click = evento.pos
                if estado == "MENU":
                    if rect_jugar and rect_jugar.collidepoint(posicion_click):
                        estado = "NOMBRE"
                        nombre_jugador = ""  # Reseteo de nombre
                    elif rect_nivel.collidepoint(posicion_click):
                        estado = "NIVEL"
                    elif rect_puntajes.collidepoint(posicion_click):
                        estado = "PUNTAJES"
                    elif rect_salir.collidepoint(posicion_click):
                        estado = "SALIR"
                    elif rect_musica.collidepoint(posicion_click):
                        if musica_activada:
                            mixer.pause()
                            musica_activada = False
                        else:
                            mixer.unpause()
                            musica_activada = True
                elif estado == "NIVEL":
                    if rect_facil.collidepoint(posicion_click):
                        nivel_actual = "FACIL"
                        estado = "MENU"
                    elif rect_medio.collidepoint(posicion_click):
                        nivel_actual = "MEDIO"
                        estado = "MENU"
                    elif rect_dificil.collidepoint(posicion_click):
                        nivel_actual = "DIFICIL"
                        estado = "MENU"

        pantalla.blit(fondo, (0, 0))

        if estado == "MENU":
            rect_jugar, rect_nivel, rect_puntajes, rect_salir, rect_musica = menu(
                pantalla, nivel_actual
            )

        match estado:
            case "NOMBRE":
                pantalla.fill((0, 0, 0))
                fuente = pg.font.SysFont("OCR A Extended", 50)
                texto = fuente.render(
                    f"Ingrese nombre (3 letras): {nombre_jugador}",
                    True,
                    (255, 255, 255),
                )
                rect_texto = texto.get_rect()
                rect_texto.center = (512, 384)
                pantalla.blit(texto, rect_texto)
            case "JUGAR":
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
                # manejar disparos y verificar victoria
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
                        datos_jugadores[f"{nombre_jugador}"] = puntaje_jugador_vivo
                        guardar_json(ruta, datos_jugadores)
                        estado = "MENU"
                        tablero_actual = None
                        tablero_disparos = None
            case "PUNTAJES":
                rect_volver = interfaz_puntajes(pantalla, ruta)
                if (
                    evento.type == pg.MOUSEBUTTONDOWN
                    and evento.button == 1
                    and not click_procesado
                ):
                    posicion = pg.mouse.get_pos()
                    if rect_volver and rect_volver.collidepoint(posicion):
                        estado = "MENU"
            case "SALIR":
                pg.quit()
                quit()
            case "NIVEL":
                rect_facil, rect_medio, rect_dificil, rect_volver = interfaz_nivel(
                    pantalla, fondo, DIMENSIONES
                )
                if (
                    evento.type == pg.MOUSEBUTTONDOWN
                    and evento.button == 1
                    and not click_procesado
                ):
                    posicion = pg.mouse.get_pos()
                    if rect_volver and rect_volver.collidepoint(posicion):
                        estado = "MENU"

        pg.display.flip()


main()  # llamado a la ejecución

import pygame as pg
import pygame.mixer as mixer

from paquetes.interfaces import interfaz_jugar, interfaz_nivel, interfaz_puntajes, menu
from paquetes.tablero import crear_tablero_con_naves
from paquetes.validates import verificar_estado


def main() -> None:
    """
    Esta funcion realiza la ejecucion del juego de una forma mas ordenada
    """

    # Inicializamos juego y musica
    pg.init()
    mixer.init()

    # Ordenamos musica
    sonido = mixer.Sound("estaticos/sonidos/menu.mp3")
    sonido.set_volume(0.4)
    sonido.play(-1)
    # variables
    estado = "MENU"
    nivel_actual = "FACIL"  # Nivel por defecto
    padding_x = 15
    padding_y = 15
    musica_activada = True

    # CONFIGURACION DE PANTALLA
    DIMENSIONES = (800, 600)
    pantalla = pg.display.set_mode(DIMENSIONES)
    titulo = pg.display.set_caption(
        "Batalla naval"
    )  # -> TITULO DEL EJECUTABLE (DEL JUEGO)
    icono_surface = pg.image.load("estaticos/imagenes/icono.png")
    pg.display.set_icon(icono_surface)  # -> ICONO DEL JUEGO

    # CREACION DE IMAGEN -> (FONDO)
    fondo = pg.image.load("estaticos/imagenes/fondo.jpg")  # MODIFICAR FONDO
    fondo = pg.transform.scale(fondo, (800, 600))

    # BUCLE PRINCIPAL DEL JUEGO
    while True:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                quit()

            if evento.type == pg.MOUSEBUTTONDOWN:
                posicion_click = evento.pos
                if estado == "MENU":
                    if rect_jugar.collidepoint(posicion_click):
                        estado = "JUGAR"
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
            case "JUGAR":
                rect_volver = interfaz_jugar(pantalla, nivel_actual)
                if pg.mouse.get_pressed()[0]:
                    if rect_volver.collidepoint(pg.mouse.get_pos()):
                        estado = "MENU"
            case "PUNTAJES":
                interfaz_puntajes(pantalla)
            case "SALIR":
                pg.quit()
                quit()
            case "NIVEL":
                rect_facil, rect_medio, rect_dificil = interfaz_nivel(pantalla)

        pg.display.flip()


main()  # llamado a la ejecución

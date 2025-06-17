import pygame as pg
import pygame.mixer as mixer

from paquetes.interfaces import *
from paquetes.tablero import crear_tablero_con_naves
from paquetes.validates import verificar_estado

nivel_actual= "FACIL"
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
    padding_x = 15
    padding_y = 15
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
            # EVENTO DE CIERRE PREDETERMINADO
            if evento.type == pg.QUIT:
                pg.quit()
                quit()
            # EVENTO PARA VERIFICAR QUE INTERFAZ SE DEBE MOSTRAR SEGUN EL CLICK
            if evento.type == pg.MOUSEBUTTONDOWN:
                posicion_click = evento.pos
                if estado == "MENU":
                    estado = verificar_estado(rects, posicion_click)
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

        # ACTUALIZACION DEL FONDO
        # pantalla.fill((255, 255, 255))  # BLANCO
        pantalla.blit(fondo, (0, 0))
        # MENU PRINCIPAL
        if estado == "MENU":
            rect_jugar, rect_nivel, rect_puntajes, rect_salir = menu(pantalla)
            rects = (rect_jugar, rect_nivel, rect_puntajes, rect_salir)

        # INTERFACES DE USUARIO
        match estado:
            case "JUGAR":
                interfaz_jugar(pantalla, nivel_actual)
            case "NIVEL":
                 rect_facil, rect_medio, rect_dificil = interfaz_nivel(pantalla)
            case "PUNTAJES":
                interfaz_puntajes(pantalla)
            case "SALIR":
                pg.quit()
                quit()

        pg.display.flip()  # -> Actualizacion de pantalla


main()  # llamado a la ejecución

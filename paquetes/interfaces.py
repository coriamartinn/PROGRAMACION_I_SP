import pygame as pg
from paquetes.tablero import *
def menu(pantalla: pg.display) -> None:
    """
    Esta funcion se encarga de dibujar en pantalla la interfaz del interfaz principal y devolver los rects exacto de cada boton
    Args:
        pantalla (pg.display): Recibe el display de pantalla
    Returns:
        None: Retorna los rects de los botones.
    """
    jugar = "Jugar"
    puntaje = "Puntajes"
    salir = "Salir"
    musica = "On/Off"
    padding_x = 20
    padding_y = 15
    
    pg.font.init()
    fuente = pg.font.SysFont("OCR A Extended", 45)
    fuente_alternativa = pg.font.SysFont("OCR A Extended", 25)
    # Creo la superficie -> (los botones)
    superficie_jugar = fuente.render(jugar, True, (255, 255, 255))
    superficie_puntaje = fuente.render(puntaje, True, (255, 255, 255))
    superficie_salir = fuente.render(salir, True, (255, 255, 255))
    superficie_musica = fuente_alternativa.render(musica, True, (255, 255, 255))
    
    # Obtengo el RECT de la superficie
    rect_jugar = superficie_jugar.get_rect()
    rect_puntaje = superficie_puntaje.get_rect()
    rect_salir = superficie_salir.get_rect()
    rect_musica = superficie_musica.get_rect()
    
    # Centro la posicion de la superficie -> (texto creado)
    rect_jugar.center = (400, 150)
    rect_puntaje.center = (400, 250)
    rect_salir.center = (400, 350)
    rect_musica.center = (737, 562)
    
    
    # dibujo el rect para el padding
    fondo_jugar = pg.Rect(
    rect_jugar.left - padding_x,
    rect_jugar.top - padding_y,
    rect_jugar.width + 2 * padding_x,
    rect_jugar.height + 2 * padding_y
    )
    fondo_puntaje = pg.Rect(
    rect_puntaje.left - padding_x,
    rect_puntaje.top - padding_y,
    rect_puntaje.width + 2 * padding_x,
    rect_puntaje.height + 2 * padding_y
    )
    fondo_salir = pg.Rect(
    rect_salir.left - padding_x,
    rect_salir.top - padding_y,
    rect_salir.width + 2 * padding_x,
    rect_salir.height + 2 * padding_y
    )
    fondo_musica = pg.Rect(
    rect_musica.left - padding_x,
    rect_musica.top - padding_y,
    rect_musica.width + 2 * padding_x,
    rect_musica.height + 2 * padding_y
    )
    #FONDO NEGRO PARA EL BOTON CON UN PADDING
    pg.draw.rect(pantalla,(4, 6, 88), fondo_jugar, border_radius=15)
    pg.draw.rect(pantalla,(4, 6, 88), fondo_puntaje, border_radius=15)
    pg.draw.rect(pantalla,(4, 6, 88), fondo_salir, border_radius=15)
    pg.draw.rect(pantalla,(4, 6, 88), fondo_musica, border_radius=15)
    
    pantalla.blit(superficie_jugar, rect_jugar)
    pantalla.blit(superficie_puntaje, rect_puntaje)
    pantalla.blit(superficie_salir, rect_salir)
    pantalla.blit(superficie_musica, rect_musica)
    
    return rect_jugar, rect_puntaje, rect_salir

def interfaz_jugar(pantalla: pg.display) -> None:
    """
    Esta funcion se encarga de dibujar en pantalla la interfaz del interfaz principal
    Args:
        pantalla (pg.display): Recibe el display de pantalla
    Returns:
        None: No existe retorno
    """
    tablero = crear_tablero_con_naves()
    imprimir_tablero(pantalla, tablero)


def interfaz_puntajes(pantalla: pg.display) -> None:
    """
    Esta funcion se encarga de dibujar en pantalla la interfaz del interfaz principal
    Args:
        pantalla (pg.display): Recibe el display de pantalla
    Returns:
        None: No existe retorno
    """
    jugar = "PRUEBA2"
    puntaje = "Prueba2"
    salir = "Saliraa2"
    
    pg.font.init()
    fuente = pg.font.SysFont("Arial", 45)
    superficie_jugar = fuente.render(jugar, True, (0, 0, 0))
    superficie_puntaje = fuente.render(puntaje, True, (0, 0, 0))
    superficie_salir = fuente.render(salir, True, (0, 0, 0))
    
    # Obtengo el RECT de la superficie
    rect_jugar = superficie_jugar.get_rect()
    rect_puntaje = superficie_puntaje.get_rect()
    rect_salir = superficie_salir.get_rect()
    
    # Centro la posicion de la superficie ->(texto creado)
    rect_jugar.center = (400, 150)
    rect_puntaje.center = (400, 250)
    rect_salir.center = (400, 350)
    
    pantalla.blit(superficie_jugar, rect_jugar)
    pantalla.blit(superficie_puntaje, rect_puntaje)
    pantalla.blit(superficie_salir, rect_salir)


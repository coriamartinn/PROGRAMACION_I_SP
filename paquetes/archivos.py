import json


def leer_json(ruta: str) -> dict:
    """
    Realiza la lectura del json que se crea con los jugadores y puntajes
    """
    with open(ruta, "r", encoding="UTF-8") as archivo_json:
        puntajes = json.load(archivo_json)

    return puntajes

import json


def leer_json(ruta: str) -> dict:
    """
    Lee los datos en un archivo JSON en la ruta indicada y los retorna en un diccionario para poder manejarlo.
    Args:
        ruta (str): Recibe la ruta del archivo
    Return:
        dict: Retorna un diccionario con los datos del archivo
    """
    with open(ruta, "r", encoding="UTF-8") as archivo_json:
        puntajes = json.load(archivo_json)

    return puntajes


def guardar_json(ruta: str, datos: dict) -> None:
    """
    Guarda los datos en un archivo JSON en la ruta indicada.
    Si el archivo no existe, lo crea. Si existe, lo sobreescribe.
    Args:
        ruta (str): Recibe la ruta del archivo
        datos (dict): Recibe nombre y puntaje del jugador
    Return:
        None: No existe retorno.
    """
    with open(ruta, "w", encoding="UTF-8") as archivo_json:
        json.dump(datos, archivo_json, indent=4, ensure_ascii=False)

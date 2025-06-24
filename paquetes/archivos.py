import json


def leer_json(ruta: str) -> dict:
    """
    Realiza la lectura del json que se crea con los jugadores y puntajes
    """
    with open(ruta, "r", encoding="UTF-8") as archivo_json:
        puntajes = json.load(archivo_json)

    return puntajes


def guardar_json(ruta: str, datos: dict) -> None:
    """
    Guarda los datos en un archivo JSON en la ruta indicada.
    Si el archivo no existe, lo crea. Si existe, lo sobreescribe.
    """
    with open(ruta, "w", encoding="UTF-8") as archivo_json:
        json.dump(datos, archivo_json, indent=4, ensure_ascii=False)
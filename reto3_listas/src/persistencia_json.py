import json
import os


def exportar_json(lista, ruta):
    """
    Guarda una lista (ListaDoble o ListaCircular) en un archivo JSON.
    Funciona con cualquier lista que tenga el método to_dict().

    Parámetros:
        lista: la lista a guardar.
        ruta (str): ruta del archivo, por ejemplo 'data/historial.json'.
    """
    datos = lista.to_dict()
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"Loading!!!! {lista.tamaño} registros exportados a {ruta}")


def importar_json(lista, ruta):
    """
    Carga los datos de un archivo JSON en la lista indicada (se borra lo que tenía).
    Se usa json (y nunca eval o pickle) porque json solo lee datos, no ejecuta código.

    Lanza:
        FileNotFoundError: si el archivo no existe.
        ValueError: si el archivo está dañado o no corresponde a esa lista.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo {ruta}")
    with open(ruta, "r", encoding="utf-8") as f:
        try:
            datos = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"El archivo {ruta} no tiene un JSON válido")
    lista.from_dict(datos)
    print(f" Successful::::: {lista.tamaño} registros importados desde {ruta}")

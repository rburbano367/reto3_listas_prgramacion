import csv
import os

ENCABEZADO = ["id", "nombres", "correo"]


def proteger_celda(texto):
    """
    Evita la 'inyección de fórmulas' en CSV (CSV Injection).
    Si una celda empieza con = + - @ , Excel podría ejecutarla como fórmula,
    por eso se le antepone una comilla simple.
    """
    texto = str(texto)
    if texto != "" and texto[0] in ("=", "+", "-", "@"):
        return "'" + texto
    return texto


def exportar_csv(lista, ruta):
    """
    Guarda los inscritos (ListaSimple) en un archivo CSV.

    Parámetros:
        lista (ListaSimple): lista de inscritos.
        ruta (str): ruta del archivo, por ejemplo 'data/inscritos.csv'.
    """
    datos = lista.to_dict()
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(ENCABEZADO)
        for e in datos["estudiantes"]:
            writer.writerow([proteger_celda(e["id"]),
                             proteger_celda(e["nombres"]),
                             proteger_celda(e["correo"])])
    print(f"💾 {len(datos['estudiantes'])} inscritos exportados a {ruta}")


def importar_csv(lista, ruta):
    """
    Carga los inscritos desde un CSV a la ListaSimple (se borra lo que tenía).
    Las filas con datos inválidos se omiten y se informa cuántas fueron.

    Lanza:
        FileNotFoundError: si el archivo no existe.
        ValueError: si el encabezado no es id,nombres,correo.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo {ruta}")
    lista.limpiar()
    errores = 0
    with open(ruta, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        encabezado = next(reader, None)
        if encabezado != ENCABEZADO:
            raise ValueError(f"Encabezado inesperado {encabezado}, se esperaba {ENCABEZADO}")
        for fila in reader:
            try:
                id_est, nombres, correo = fila
                lista.insertar_final({"id": id_est.lstrip("'"),
                                     "nombres": nombres.lstrip("'"),
                                     "correo": correo.lstrip("'")})
            except ValueError as error:
                errores += 1
                print(f"  ⚠ Fila omitida {fila}: {error}")
    print(f" Successful::::: {lista.tamaño} inscritos importados desde {ruta} ({errores} filas con error)")

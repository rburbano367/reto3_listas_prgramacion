"""
Pruebas de robustez: ¿qué pasa si alguien manipula los archivos de datos?
(Enfoque de ciberseguridad: todo archivo que se importa es una entrada no confiable.)
"""

import contextlib
import io
import json
import os
import tempfile

from lista_simple import ListaSimple
from lista_doble import ListaDoble
from lista_circular import ListaCircular, MAX_GRUPOS
from persistencia_csv import exportar_csv, importar_csv
from persistencia_json import importar_json

carpeta = tempfile.mkdtemp()


def crear_archivo(nombre, contenido):
    """Crea un archivo temporal de prueba y retorna su ruta."""
    ruta = os.path.join(carpeta, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


print("[T1] JSON de grupos cargado como si fuera historial:")
ruta = crear_archivo("a.json", json.dumps({"tipo": "ListaCircular", "grupos": []}))
try:
    importar_json(ListaDoble(), ruta)
except ValueError as error:
    print(f"     🛡 bloqueado -> {error}")

print("[T2] JSON manipulado con una nota de 99:")
malo = {"tipo": "ListaDoble",
        "semestres": [{"año": 2024, "term": 1,
                       "materias": [{"cod": "X1", "nombre": "Hack", "nota": 99}]}]}
try:
    importar_json(ListaDoble(), crear_archivo("b.json", json.dumps(malo)))
except ValueError as error:
    print(f"     XXXX bloqueado -> {error}")

print("[T3] JSON dañado (texto que no es JSON):")
try:
    importar_json(ListaDoble(), crear_archivo("c.json", "{esto no es json"))
except ValueError as error:
    print(f"     XXXX bloqueado -> {error}")

print("[T4] CSV con una columna extra 'rol':")
try:
    importar_csv(ListaSimple(), crear_archivo("d.csv", "id,nombres,correo,rol\n1,Ana,a@u.ec,admin\n"))
except ValueError as error:
    print(f"     XXXX bloqueado -> {error}")

print("[T5] CSV con una fila válida y otra con <script> en el correo:")
importar_csv(ListaSimple(), crear_archivo("e.csv", "id,nombres,correo\n1,Ana,ana@u.ec\n2,Eve,<script>\n"))

print("[T6] CSV Injection: un nombre que empieza con '=':")
lista = ListaSimple()
lista.insertar_final({"id": "7", "nombres": "=HYPERLINK(\"http://malicioso\")", "correo": "eve@u.ec"})
ruta = os.path.join(carpeta, "f.csv")
exportar_csv(lista, ruta)
with open(ruta, encoding="utf-8") as f:
    print(f"     contenido guardado: {f.read().splitlines()[1]}")
print("     XXXX la comilla inicial evita que Excel lo ejecute como fórmula")

print(f"[T7] Límite de grupos ({MAX_GRUPOS}) para proteger la recursión:")
circular = ListaCircular()
with contextlib.redirect_stdout(io.StringIO()):     # oculta los 500 mensajes "✅ Grupo..."
    for i in range(MAX_GRUPOS):
        circular.insertar({"nombre_grupo": f"G{i}", "tutor": "Tutor", "tema": ""})
r = circular.buscar_recursivo(f"G{MAX_GRUPOS - 1}")
print(f"     buscar_recursivo del último -> {r[0]} llamadas de profundidad, sin error")
try:
    circular.insertar({"nombre_grupo": "Extra", "tutor": "Tutor", "tema": ""})
except OverflowError as error:
    print(f"     XXXX grupo {MAX_GRUPOS + 1} bloqueado -> {error}")

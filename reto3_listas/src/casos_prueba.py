"""
Casos de prueba MÍNIMOS del Reto 3 (para grabar el video).

Uso:
    python casos_prueba.py simple
    python casos_prueba.py doble
    python casos_prueba.py circular
    python casos_prueba.py          (ejecuta los tres)
"""

import os
import sys

from lista_simple import ListaSimple
from lista_doble import ListaDoble
from lista_circular import ListaCircular

CARPETA_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def titulo(texto):
    print("\n" + "=" * 60)
    print(" " + texto)
    print("=" * 60)


def caso_lista_simple():
    titulo("CASO 1 - LISTA SIMPLE (Inscritos)")
    lista = ListaSimple()
    print("▶ Agregar 3 inscritos")
    lista.insertar_final({"id": "1001", "nombres": "Ana Torres", "correo": "ana.torres@uni.edu.ec"})
    lista.insertar_final({"id": "1002", "nombres": "Luis Paredes", "correo": "luis.paredes@uni.edu.ec"})
    lista.insertar_final({"id": "1003", "nombres": "Carla Mena", "correo": "carla.mena@uni.edu.ec"})

    print("▶ Buscar y eliminar el 1002")
    print(f"  buscar('1002') -> {lista.buscar('1002')}")
    lista.eliminar("1002")
    print(f"  buscar('1002') -> {lista.buscar('1002')}")

    print("▶ Mostrar")
    lista.recorrer()

    ruta = os.path.join(CARPETA_DATA, "inscritos.csv")
    print("▶ Exportar CSV, limpiar e importar")
    lista.exportar_csv(ruta)
    lista.limpiar()
    print(f"  Después de limpiar(): tamaño = {lista.tamaño}, head = {lista.head}")
    lista.importar_csv(ruta)
    lista.recorrer()

    print("▶ Validación: correo mal escrito")
    try:
        lista.insertar_final({"id": "1004", "nombres": "Pedro Ruiz", "correo": "pedro-sin-arroba"})
    except ValueError as error:
        print(f"  ⚠ Rechazado: {error}")


def caso_lista_doble():
    titulo("CASO 2 - LISTA DOBLE (Historial académico)")
    lista = ListaDoble()
    print("▶ Insertar DESORDENADO: 2025-1, 2023-2, 2024-2, 2024-1")
    lista.insertar_ordenado({"año": 2025, "term": 1, "materias": [
        {"cod": "EST201", "nombre": "Estructuras de Datos", "nota": 9.1},
        {"cod": "RED201", "nombre": "Redes I", "nota": 8.7}]})
    lista.insertar_ordenado({"año": 2023, "term": 2, "materias": [
        {"cod": "MAT101", "nombre": "Cálculo I", "nota": 7.2},
        {"cod": "PRO101", "nombre": "Programación I", "nota": 8.0}]})
    lista.insertar_ordenado({"año": 2024, "term": 2, "materias": [
        {"cod": "SO201", "nombre": "Sistemas Operativos", "nota": 8.9},
        {"cod": "CRI201", "nombre": "Criptografía", "nota": 9.4}]})
    lista.insertar_ordenado({"año": 2024, "term": 1, "materias": [
        {"cod": "MAT201", "nombre": "Matemática Discreta", "nota": 7.8},
        {"cod": "PRO201", "nombre": "Programación II", "nota": 8.6}]})

    print("> Comprobar el orden")
    print(f"  Adelante: {lista.resumen()}")
    print(f"  Atrás:    {lista.resumen(hacia_atras=True)}")
    lista.recorrer_adelante()

    print("> Buscar 2024-1")
    lista.mostrar_semestre(lista.buscar("2024-1"))

    ruta = os.path.join(CARPETA_DATA, "historial.json")
    print("> Exportar JSON, limpiar e importar")
    lista.exportar_json(ruta)
    lista.limpiar()
    print(f"  Después de limpiar(): tamaño = {lista.tamaño}")
    lista.importar_json(ruta)
    print(f"  Adelante: {lista.resumen()}")
    print(f"  Atrás:    {lista.resumen(hacia_atras=True)}")
    lista.top_promedios(3)


def caso_lista_circular():
    titulo("CASO 3 - LISTA CIRCULAR (Rotación de prácticas)")
    lista = ListaCircular()
    print("> Agregar 3 grupos")
    lista.insertar({"nombre_grupo": "G1", "tutor": "Ing. Rivas", "tema": "Firewall con iptables"})
    lista.insertar({"nombre_grupo": "G2", "tutor": "Ing. Salazar", "tema": "Análisis con Wireshark"})
    lista.insertar({"nombre_grupo": "G3", "tutor": "Ing. Cevallos", "tema": "Hardening de Linux"})

    print("> Búsqueda recursiva")
    print(f"  buscar_recursivo('G3') -> {lista.buscar_recursivo('G3')}")
    print(f"  buscar_recursivo('G9') -> {lista.buscar_recursivo('G9')}")

    print("> Recorrer 2 vueltas (demuestra el ciclo)")
    lista.recorrer(2)

    print("> rotar(2)")
    lista.rotar(2)
    lista.recorrer(1)
    lista.rotar(2)

    print("▶ Eliminar G1 y comprobar que el ciclo se conserva")
    lista.eliminar("G1")
    lista.recorrer(3)
    print(f"  es_circular() = {lista.es_circular()}   tamaño = {lista.tamaño}")

    ruta = os.path.join(CARPETA_DATA, "grupos.json")
    print("> Exportar e importar JSON")
    lista.exportar_json(ruta)
    lista.limpiar()
    lista.importar_json(ruta)
    lista.mostrar()


if __name__ == "__main__":
    os.makedirs(CARPETA_DATA, exist_ok=True)
    caso = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if caso in ("simple", "todo"):
        caso_lista_simple()
    if caso in ("doble", "todo"):
        caso_lista_doble()
    if caso in ("circular", "todo"):
        caso_lista_circular()

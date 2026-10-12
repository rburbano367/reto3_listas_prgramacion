"""
Prueba aleatoria (fuzzing) de las tres listas.

Hace miles de operaciones al azar (insertar, eliminar, buscar, rotar) y, después
de CADA operación, compara la lista enlazada con un "modelo" hecho con una lista
normal de Python (solo aquí, para comprobar). Además revisa que todos los enlaces
sigan sanos: head/tail, anterior/siguiente y que el círculo siga cerrado.

Ejecutar:  python prueba_aleatoria.py
"""

import contextlib
import io
import os
import random
import tempfile

from lista_simple import ListaSimple
from lista_doble import ListaDoble
from lista_circular import ListaCircular

RONDAS, PASOS = 300, 40
carpeta = tempfile.mkdtemp()
fallos = 0


def silencio():
    """Oculta los mensajes que imprimen las listas."""
    return contextlib.redirect_stdout(io.StringIO())


def comprobar(condicion, mensaje):
    """Cuenta un fallo si la condición no se cumple."""
    global fallos
    if not condicion:
        fallos += 1
        print("FALLO:", mensaje)


def revisar_simple(lista, modelo):
    ids, nodo, ultimo = [], lista.head, None
    while nodo:
        ids.append(nodo.valor["id"])
        ultimo = nodo
        nodo = nodo.siguiente
    comprobar(ids == modelo, "el orden de la lista simple no coincide")
    comprobar(lista.tail is ultimo, "tail no apunta al último nodo")
    comprobar(lista.tamaño == len(modelo), "tamaño incorrecto (simple)")


def revisar_doble(lista, modelo):
    adelante, nodo, previo = [], lista.head, None
    while nodo:
        comprobar(nodo.anterior is previo, "enlace 'anterior' roto")
        adelante.append((nodo.valor["año"], nodo.valor["term"]))
        previo = nodo
        nodo = nodo.siguiente
    atras, nodo = [], lista.tail
    while nodo:
        atras.append((nodo.valor["año"], nodo.valor["term"]))
        nodo = nodo.anterior
    comprobar(adelante == sorted(modelo), "la lista doble no está ordenada")
    comprobar(atras == adelante[::-1], "el recorrido hacia atrás no es el inverso")
    comprobar(lista.tamaño == len(modelo), "tamaño incorrecto (doble)")


def revisar_circular(lista, modelo):
    if not modelo:
        comprobar(lista.actual is None and lista.tamaño == 0, "debería estar vacía")
        return
    nombres, nodo = [], lista.actual
    for _ in range(len(modelo)):
        nombres.append(nodo.valor["nombre_grupo"])
        nodo = nodo.siguiente
    comprobar(nodo is lista.actual, "el círculo no se cierra")
    comprobar(nombres == modelo, "el orden del turno no coincide")


random.seed(2026)

# ---------------- Lista simple ----------------
for _ in range(RONDAS):
    lista, modelo = ListaSimple(), []
    for _ in range(PASOS):
        i = str(random.randint(1, 15))
        with silencio():
            if random.random() < 0.55:
                try:
                    lista.insertar_final({"id": i, "nombres": "N" + i, "correo": f"u{i}@u.ec"})
                    modelo.append(i)
                except ValueError:
                    comprobar(i in modelo, "rechazó un id que no existía")
            else:
                eliminado = lista.eliminar(i)
                comprobar((eliminado is not None) == (i in modelo), "eliminar (simple)")
                if i in modelo:
                    modelo.remove(i)
        revisar_simple(lista, modelo)
    ruta = os.path.join(carpeta, "s.csv")
    with silencio():
        lista.exportar_csv(ruta)
        copia = ListaSimple()
        copia.importar_csv(ruta)
    revisar_simple(copia, modelo)

# ---------------- Lista doble ----------------
for _ in range(RONDAS):
    lista, modelo = ListaDoble(), []
    for _ in range(PASOS):
        k = (random.randint(2020, 2026), random.randint(1, 2))
        with silencio():
            if random.random() < 0.6:
                try:
                    lista.insertar_ordenado({"año": k[0], "term": k[1],
                                             "materias": [{"cod": "C", "nombre": "M", "nota": random.randint(0, 10)}]})
                    modelo.append(k)
                except ValueError:
                    comprobar(k in modelo, "rechazó un semestre que no existía")
            else:
                eliminado = lista.eliminar(f"{k[0]}-{k[1]}")
                comprobar((eliminado is not None) == (k in modelo), "eliminar (doble)")
                if k in modelo:
                    modelo.remove(k)
        revisar_doble(lista, modelo)
    ruta = os.path.join(carpeta, "d.json")
    with silencio():
        lista.exportar_json(ruta)
        copia = ListaDoble()
        copia.importar_json(ruta)
    revisar_doble(copia, modelo)

# ---------------- Lista circular ----------------
for _ in range(RONDAS):
    lista, modelo = ListaCircular(), []          # modelo[0] = grupo en turno
    for _ in range(PASOS):
        g = "G" + str(random.randint(1, 10))
        op = random.random()
        with silencio():
            if op < 0.4:
                try:
                    lista.insertar({"nombre_grupo": g, "tutor": "T", "tema": "x"})
                    modelo.append(g)
                except ValueError:
                    comprobar(g in modelo, "rechazó un grupo que no existía")
            elif op < 0.65:
                eliminado = lista.eliminar(g)
                comprobar((eliminado is not None) == (g in modelo), "eliminar (circular)")
                if g in modelo:
                    modelo.remove(g)                 # si era el turno, pasa al siguiente
            elif op < 0.85:
                k = random.randint(0, 25)
                lista.rotar(k)
                if modelo:
                    p = k % len(modelo)
                    modelo = modelo[p:] + modelo[:p]
            else:
                r = lista.buscar_recursivo(g)
                if g in modelo:
                    comprobar(r is not None and r[0] == modelo.index(g), "posición de buscar_recursivo")
                else:
                    comprobar(r is None, "buscar_recursivo encontró un grupo inexistente")
        revisar_circular(lista, modelo)
    ruta = os.path.join(carpeta, "c.json")
    with silencio():
        lista.exportar_json(ruta)
        copia = ListaCircular()
        copia.importar_json(ruta)
    revisar_circular(copia, modelo)

total = 3 * RONDAS * PASOS
print(f"Operaciones aleatorias: {total:,} (3 listas x {RONDAS} rondas x {PASOS} pasos)")
print(f"Fallos encontrados: {fallos}")
print("✅ Todas las listas se comportaron igual que el modelo" if fallos == 0 else "❌ Revisar los fallos")

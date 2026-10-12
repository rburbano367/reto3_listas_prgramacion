"""
Pruebas unitarias del Reto 3 con unittest (Clase 13).

Ejecutar:  python -m unittest test_listas -v
"""

import contextlib
import io
import os
import tempfile
import unittest

from lista_simple import ListaSimple
from lista_doble import ListaDoble, convertir_semestre
from lista_circular import ListaCircular


def silencio():
    """Oculta los mensajes que imprimen las listas para que la salida de las pruebas sea limpia."""
    return contextlib.redirect_stdout(io.StringIO())


class TestListaSimple(unittest.TestCase):

    def setUp(self):
        self.lista = ListaSimple()
        with silencio():
            self.lista.insertar_final({"id": "1001", "nombres": "Ana Torres", "correo": "ana@uni.edu.ec"})
            self.lista.insertar_final({"id": "1002", "nombres": "Luis Paredes", "correo": "luis@uni.edu.ec"})
            self.lista.insertar_final({"id": "1003", "nombres": "Carla Mena", "correo": "carla@uni.edu.ec"})

    def test_insertar_final(self):
        self.assertEqual(self.lista.tamaño, 3)
        self.assertEqual(self.lista.head.valor["id"], "1001")
        self.assertEqual(self.lista.tail.valor["id"], "1003")

    def test_buscar(self):
        self.assertEqual(self.lista.buscar("1002")["nombres"], "Luis Paredes")
        self.assertIsNone(self.lista.buscar("9999"))

    def test_eliminar_en_medio_y_en_cola(self):
        with silencio():
            self.lista.eliminar("1002")
            self.lista.eliminar("1003")
        self.assertEqual(self.lista.tamaño, 1)
        self.assertEqual(self.lista.tail.valor["id"], "1001")     # tail se actualizó
        self.assertIsNone(self.lista.head.siguiente)

    def test_id_duplicado(self):
        with self.assertRaises(ValueError):
            self.lista.insertar_final({"id": "1001", "nombres": "Otra Persona", "correo": "otra@uni.edu.ec"})

    def test_correo_invalido(self):
        with self.assertRaises(ValueError):
            self.lista.insertar_final({"id": "1004", "nombres": "Pedro", "correo": "pedro-sin-arroba"})

    def test_csv_ida_y_vuelta(self):
        ruta = os.path.join(tempfile.mkdtemp(), "inscritos.csv")
        with silencio():
            self.lista.exportar_csv(ruta)
            nueva = ListaSimple()
            nueva.importar_csv(ruta)
        self.assertEqual(nueva.to_dict(), self.lista.to_dict())

    def test_from_dict_rechaza_otro_tipo(self):
        with self.assertRaises(ValueError):
            ListaSimple().from_dict({"tipo": "ListaDoble", "semestres": []})


class TestListaDoble(unittest.TestCase):

    def setUp(self):
        self.lista = ListaDoble()
        with silencio():       # se insertan DESORDENADOS a propósito
            self.lista.insertar_ordenado({"año": 2025, "term": 1, "materias": [{"cod": "A", "nombre": "A", "nota": 9}]})
            self.lista.insertar_ordenado({"año": 2023, "term": 2, "materias": [{"cod": "B", "nombre": "B", "nota": 7}]})
            self.lista.insertar_ordenado({"año": 2024, "term": 1, "materias": [{"cod": "C", "nombre": "C", "nota": 8}]})

    def test_queda_ordenada(self):
        self.assertEqual(self.lista.resumen(), "2023-2 <-> 2024-1 <-> 2025-1")

    def test_recorrido_atras(self):
        self.assertEqual(self.lista.resumen(hacia_atras=True), "2025-1 <-> 2024-1 <-> 2023-2")

    def test_buscar(self):
        self.assertEqual(self.lista.buscar("2024-1")["materias"][0]["nota"], 8)
        self.assertIsNone(self.lista.buscar("2030-1"))

    def test_eliminar_head(self):
        with silencio():
            self.lista.eliminar("2023-2")
        self.assertEqual(self.lista.head.valor["año"], 2024)
        self.assertIsNone(self.lista.head.anterior)               # enlace atrás corregido

    def test_semestre_duplicado(self):
        with self.assertRaises(ValueError):
            self.lista.insertar_ordenado({"año": 2024, "term": 1, "materias": []})

    def test_nota_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            self.lista.insertar_ordenado({"año": 2026, "term": 1, "materias": [{"cod": "X", "nombre": "X", "nota": 11}]})

    def test_formato_de_semestre(self):
        self.assertEqual(convertir_semestre("2024-1"), (2024, 1))
        with self.assertRaises(ValueError):
            convertir_semestre("2024-3")                          # el término solo puede ser 1 o 2
        with self.assertRaises(ValueError):
            convertir_semestre("2024/1")

    def test_json_ida_y_vuelta(self):
        ruta = os.path.join(tempfile.mkdtemp(), "historial.json")
        with silencio():
            self.lista.exportar_json(ruta)
            nueva = ListaDoble()
            nueva.importar_json(ruta)
        self.assertEqual(nueva.resumen(), self.lista.resumen())


class TestListaCircular(unittest.TestCase):

    def setUp(self):
        self.lista = ListaCircular()
        with silencio():
            self.lista.insertar({"nombre_grupo": "G1", "tutor": "Ing. Rivas", "tema": "Firewall"})
            self.lista.insertar({"nombre_grupo": "G2", "tutor": "Ing. Salazar", "tema": "Wireshark"})
            self.lista.insertar({"nombre_grupo": "G3", "tutor": "Ing. Cevallos", "tema": "Hardening"})

    def test_buscar_recursivo(self):
        posicion, grupo = self.lista.buscar_recursivo("G3")
        self.assertEqual(posicion, 2)
        self.assertEqual(grupo["tutor"], "Ing. Cevallos")
        self.assertIsNone(self.lista.buscar_recursivo("G9"))      # no entra en bucle infinito

    def test_buscar_recursivo_lista_vacia(self):
        self.assertIsNone(ListaCircular().buscar_recursivo("G1"))

    def test_rotar(self):
        with silencio():
            self.assertEqual(self.lista.rotar(2)["nombre_grupo"], "G3")
            self.assertEqual(self.lista.rotar(2)["nombre_grupo"], "G2")   # dio la vuelta
            self.assertEqual(self.lista.rotar(3)["nombre_grupo"], "G2")   # 3 % 3 = 0

    def test_eliminar_conserva_ciclo(self):
        with silencio():
            self.lista.eliminar("G1")
        self.assertTrue(self.lista.es_circular())
        self.assertEqual(self.lista.tamaño, 2)
        self.assertEqual(self.lista.siguiente_turno()["nombre_grupo"], "G2")

    def test_eliminar_ultimo_grupo(self):
        with silencio():
            for g in ("G1", "G2", "G3"):
                self.lista.eliminar(g)
        self.assertTrue(self.lista.esta_vacia())

    def test_grupo_duplicado(self):
        with self.assertRaises(ValueError):
            self.lista.insertar({"nombre_grupo": "g1", "tutor": "Otro", "tema": ""})   # no distingue mayúsculas

    def test_json_ida_y_vuelta(self):
        ruta = os.path.join(tempfile.mkdtemp(), "grupos.json")
        with silencio():
            self.lista.rotar(1)
            self.lista.exportar_json(ruta)
            nueva = ListaCircular()
            nueva.importar_json(ruta)
        self.assertEqual(nueva.siguiente_turno()["nombre_grupo"], "G2")   # se conserva el turno


if __name__ == "__main__":
    unittest.main()

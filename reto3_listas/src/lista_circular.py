import persistencia_json
from nodo_circular import NodoCircular

# Máximo de grupos permitidos. La búsqueda es recursiva y Python corta en ~1000
# llamadas (RecursionError). Con este límite un archivo manipulado con miles de
# grupos no puede tumbar el programa.
MAX_GRUPOS = 500


def validar_grupo(grupo):
    """
    Revisa los datos de un grupo de prácticas.

    Parámetros:
        grupo (dict): {"nombre_grupo": ..., "tutor": ..., "tema": ...}

    Lanza:
        ValueError: si el nombre o el tutor están vacíos o son muy largos.
    """
    nombre_grupo = str(grupo.get("nombre_grupo", "")).strip()
    tutor = str(grupo.get("tutor", "")).strip()
    tema = str(grupo.get("tema", "")).strip()
    if nombre_grupo == "" or len(nombre_grupo) > 40:
        raise ValueError("El nombre del grupo no puede estar vacío ni pasar de 40 caracteres")
    if tutor == "" or len(tutor) > 80:
        raise ValueError("El tutor no puede estar vacío ni pasar de 80 caracteres")
    return {"nombre_grupo": nombre_grupo, "tutor": tutor, "tema": tema}


class ListaCircular:
    """
    Lista circular simple para la rotación de grupos de prácticas.

    Atributos:
        actual (NodoCircular): grupo al que le toca exponer (inicio del ciclo).
        tamaño (int): cantidad de grupos.

    El último nodo siempre apunta a 'actual', por eso nunca hay None al final.
    """

    def __init__(self):
        self.actual = None
        self.tamaño = 0

    def esta_vacia(self):
        """Retorna True si no hay grupos."""
        return self.actual is None

    def ultimo(self):
        """Retorna el último nodo del ciclo (aquel cuyo siguiente es 'actual')."""
        nodo = self.actual
        while nodo.siguiente != self.actual:
            nodo = nodo.siguiente
        return nodo

    def insertar(self, grupo):
        """
        Agrega un grupo al final del turno (justo antes de 'actual').

        Parámetros:
            grupo (dict): {"nombre_grupo": ..., "tutor": ..., "tema": ...}

        Lanza:
            ValueError: si los datos son inválidos o el grupo ya existe.
            OverflowError: si se supera MAX_GRUPOS.
        """
        grupo = validar_grupo(grupo)
        if self.tamaño >= MAX_GRUPOS:
            raise OverflowError(f"No se permiten más de {MAX_GRUPOS} grupos")
        if self.buscar_recursivo(grupo["nombre_grupo"]) is not None:
            raise ValueError(f"El grupo {grupo['nombre_grupo']} ya existe")

        nuevo = NodoCircular(grupo)
        if self.actual is None:              # lista vacía: el nodo apunta a sí mismo
            self.actual = nuevo
            nuevo.siguiente = nuevo
        else:                                # el último apunta al nuevo y el nuevo cierra el ciclo
            ultimo = self.ultimo()
            ultimo.siguiente = nuevo
            nuevo.siguiente = self.actual
        self.tamaño += 1
        print(f"✅ Grupo {grupo['nombre_grupo']} agregado ({grupo['tema']})")

    def buscar_recursivo(self, valor, nodo=None, posicion=0):
        """
        Busca un grupo por su nombre usando RECURSIVIDAD.

        Caso base 1: la lista está vacía                    -> None
        Caso base 2: el nodo coincide con el valor buscado  -> (posicion, grupo)
        Caso base 3: el siguiente nodo es 'actual'          -> None (vuelta completa)
        Caso recursivo: buscar en nodo.siguiente con posicion + 1

        Parámetros:
            valor (str): nombre del grupo a buscar (no distingue mayúsculas).
            nodo, posicion: de uso interno en las llamadas recursivas.

        Retorna:
            tuple: (posición desde el turno actual, grupo), o None si no existe.
        """
        if self.actual is None:                                   # caso base 1
            return None
        if nodo is None:                                          # primera llamada
            nodo = self.actual
        if nodo.valor["nombre_grupo"].lower() == str(valor).strip().lower():
            return (posicion, nodo.valor)                          # caso base 2
        if nodo.siguiente == self.actual:                         # caso base 3
            return None
        return self.buscar_recursivo(valor, nodo.siguiente, posicion + 1)   # caso recursivo

    def eliminar(self, nombre_grupo):
        """
        Elimina un grupo manteniendo el ciclo cerrado.

        Retorna:
            dict: el grupo eliminado, o None si no existe.
        """
        if self.actual is None:
            print("⚠ No hay grupos")
            return None
        objetivo = str(nombre_grupo).strip().lower()
        anterior = self.ultimo()          # el anterior de 'actual' es el último
        nodo = self.actual
        while True:
            if nodo.valor["nombre_grupo"].lower() == objetivo:
                if self.tamaño == 1:                     # era el único grupo
                    self.actual = None
                else:
                    anterior.siguiente = nodo.siguiente   # "puentear" el nodo
                    if nodo == self.actual:               # si era el turno, pasa al siguiente
                        self.actual = nodo.siguiente
                self.tamaño -= 1
                print(f"❌ Grupo {nodo.valor['nombre_grupo']} eliminado")
                return nodo.valor
            anterior = nodo
            nodo = nodo.siguiente
            if nodo == self.actual:                       # vuelta completa sin encontrarlo
                break
        print(f"⚠ El grupo {nombre_grupo} no existe")
        return None

    def rotar(self, k=1):
        """
        Avanza el puntero 'actual' k posiciones (cambio de turno).
        Usa k % tamaño para no dar vueltas innecesarias.

        Retorna:
            dict: el grupo que queda en turno.
        """
        if self.actual is None:
            print("⚠ No hay grupos")
            return None
        if k < 0:
            raise ValueError("k debe ser mayor o igual a 0")
        pasos = k % self.tamaño
        for _ in range(pasos):
            self.actual = self.actual.siguiente
        print(f"↻ rotar({k}) -> ahora es turno de {self.actual.valor['nombre_grupo']}")
        return self.actual.valor

    def siguiente_turno(self):
        """Retorna el grupo al que le toca exponer, o None."""
        if self.actual is None:
            return None
        return self.actual.valor

    def recorrer(self, n_vueltas=1):
        """Muestra los grupos dando n_vueltas al ciclo, empezando en 'actual'."""
        if self.actual is None:
            print("  (no hay grupos)")
            return
        nodo = self.actual
        for vuelta in range(n_vueltas):
            texto = f"  Vuelta {vuelta + 1}: "
            while True:
                texto += nodo.valor["nombre_grupo"] + " -> "
                nodo = nodo.siguiente
                if nodo == self.actual:
                    texto += "(vuelta completada)"
                    break
            print(texto)

    def mostrar(self):
        """Muestra el detalle de cada grupo, marcando el que está en turno."""
        if self.actual is None:
            print("  (no hay grupos)")
            return
        nodo = self.actual
        while True:
            marca = "->" if nodo == self.actual else "  "
            g = nodo.valor
            print(f"  {marca} {g['nombre_grupo']:<6} tutor: {g['tutor']:<15} tema: {g['tema']}")
            nodo = nodo.siguiente
            if nodo == self.actual:
                break

    def es_circular(self):
        """Comprueba que, al avanzar 'tamaño' pasos, se vuelve a 'actual'."""
        if self.actual is None:
            return True
        nodo = self.actual
        for _ in range(self.tamaño):
            nodo = nodo.siguiente
        return nodo == self.actual

    def limpiar(self):
        """Deja la lista vacía."""
        self.actual = None
        self.tamaño = 0

    # ------------------ persistencia ------------------
    def to_dict(self):
        """Convierte la lista en diccionario. El primer grupo guardado es el turno actual."""
        grupos = []
        if self.actual is not None:
            nodo = self.actual
            while True:
                grupos.append(dict(nodo.valor))
                nodo = nodo.siguiente
                if nodo == self.actual:
                    break
        return {"tipo": "ListaCircular", "grupos": grupos}

    def from_dict(self, datos):
        """Reconstruye la lista a partir de un diccionario leído de JSON."""
        if datos.get("tipo") != "ListaCircular":
            raise ValueError("Los datos no corresponden a una ListaCircular")
        self.limpiar()
        for g in datos["grupos"]:
            self.insertar(g)

    def exportar_json(self, ruta):
        """Guarda los grupos en un archivo JSON (usa persistencia_json.py)."""
        persistencia_json.exportar_json(self, ruta)

    def importar_json(self, ruta):
        """Carga los grupos desde un archivo JSON (usa persistencia_json.py)."""
        persistencia_json.importar_json(self, ruta)

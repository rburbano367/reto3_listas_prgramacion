import persistencia_json
from nodo_doble import NodoDoble
from nodo_simple import NodoSimple


def convertir_semestre(texto):
    """
    Convierte un texto como '2024-1' en la tupla (2024, 1).

    Lanza:
        ValueError: si el formato no es AAAA-T.
    """
    partes = str(texto).strip().split("-")
    if len(partes) != 2 or not partes[0].isdigit() or not partes[1].isdigit():
        raise ValueError(f"Semestre inválido '{texto}': use el formato AAAA-T (ej. 2024-1)")
    año, term = int(partes[0]), int(partes[1])
    if term not in (1, 2):
        raise ValueError(f"Semestre inválido '{texto}': el término debe ser 1 o 2")
    return año, term


def validar_semestre(registro):
    """
    Revisa los datos de un semestre y sus materias.

    Parámetros:
        registro (dict): {"año": 2024, "term": 1, "materias": [{"cod", "nombre", "nota"}, ...]}

    Retorna:
        dict: el semestre con los datos limpios.

    Lanza:
        ValueError: si el año, el término o alguna nota no son válidos.
    """
    año = int(registro.get("año", 0))
    term = int(registro.get("term", 0))
    materias = registro.get("materias", [])
    if año < 1990 or año > 2100:
        raise ValueError(f"Año fuera de rango: {año}")
    if term not in (1, 2):
        raise ValueError(f"El término debe ser 1 o 2, no {term}")
    limpias = []
    for m in materias:
        nota = float(m["nota"])
        if nota < 0 or nota > 10:
            raise ValueError(f"Nota fuera de rango (0-10): {nota}")
        limpias.append({"cod": str(m["cod"]).strip(),
                        "nombre": str(m["nombre"]).strip(),
                        "nota": nota})
    return {"año": año, "term": term, "materias": limpias}


def promedio(semestre):
    """Retorna el promedio de notas de un semestre (0 si no tiene materias)."""
    if len(semestre["materias"]) == 0:
        return 0.0
    suma = 0
    for m in semestre["materias"]:
        suma += m["nota"]
    return round(suma / len(semestre["materias"]), 2)


def clave(semestre):
    """Retorna (año, term), que se usa para ordenar los semestres."""
    return (semestre["año"], semestre["term"])


class ListaDoble:
    """
    Lista doblemente enlazada con el historial académico de un estudiante.
    Cada nodo es un semestre y la lista se mantiene ordenada por (año, term).

    Atributos:
        head (NodoDoble): semestre más antiguo.
        tail (NodoDoble): semestre más reciente.
        tamaño (int): cantidad de semestres.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.tamaño = 0

    def esta_vacia(self):
        """Retorna True si no hay semestres registrados."""
        return self.head is None

    def insertar_ordenado(self, registro_semestre):
        """
        Inserta un semestre en la posición que le corresponde según (año, term).

        Parámetros:
            registro_semestre (dict): {"año": ..., "term": ..., "materias": [...]}

        Lanza:
            ValueError: si los datos son inválidos o el semestre ya existe.
        """
        semestre = validar_semestre(registro_semestre)
        nuevo = NodoDoble(semestre)
        k = clave(semestre)

        if self.head is None:                       # caso 1: lista vacía
            self.head = nuevo
            self.tail = nuevo
        elif k < clave(self.head.valor):             # caso 2: va antes del head
            nuevo.siguiente = self.head
            self.head.anterior = nuevo
            self.head = nuevo
        elif k > clave(self.tail.valor):             # caso 3: va después del tail
            nuevo.anterior = self.tail
            self.tail.siguiente = nuevo
            self.tail = nuevo
        else:                                       # caso 4: va en medio
            actual = self.head
            while clave(actual.valor) < k:
                actual = actual.siguiente
            if clave(actual.valor) == k:
                raise ValueError(f"El semestre {semestre['año']}-{semestre['term']} ya existe")
            previo = actual.anterior                # nuevo va entre previo y actual
            nuevo.anterior = previo
            nuevo.siguiente = actual
            previo.siguiente = nuevo
            actual.anterior = nuevo
        self.tamaño += 1
        print(f"✅ Semestre {semestre['año']}-{semestre['term']} insertado en orden")

    def buscar_nodo(self, texto_semestre):
        """Retorna el nodo del semestre indicado ('2024-1') o None."""
        k = convertir_semestre(texto_semestre)
        actual = self.head
        while actual:
            if clave(actual.valor) == k:
                return actual
            if clave(actual.valor) > k:      # como está ordenada, ya no puede aparecer
                return None
            actual = actual.siguiente
        return None

    def buscar(self, texto_semestre):
        """
        Busca un semestre, por ejemplo '2024-1'.

        Retorna:
            dict: el semestre encontrado, o None si no existe.
        """
        nodo = self.buscar_nodo(texto_semestre)
        if nodo is None:
            return None
        return nodo.valor

    def eliminar(self, texto_semestre):
        """
        Elimina un semestre, por ejemplo '2024-1'.

        Retorna:
            dict: el semestre eliminado, o None si no existe.
        """
        nodo = self.buscar_nodo(texto_semestre)
        if nodo is None:
            print(f"⚠ No existe el semestre {texto_semestre}")
            return None
        if nodo.anterior:                   # enlace hacia adelante
            nodo.anterior.siguiente = nodo.siguiente
        else:
            self.head = nodo.siguiente
        if nodo.siguiente:                  # enlace hacia atrás
            nodo.siguiente.anterior = nodo.anterior
        else:
            self.tail = nodo.anterior
        self.tamaño -= 1
        print(f"❌ Semestre {texto_semestre} eliminado")
        return nodo.valor

    def mostrar_semestre(self, s):
        """Imprime un semestre con su promedio y sus materias."""
        print(f"  [{s['año']}-{s['term']}]  promedio: {promedio(s):.2f}")
        for m in s["materias"]:
            print(f"      {m['cod']:<8}{m['nombre']:<24}{m['nota']:>5.2f}")

    def recorrer_adelante(self):
        """Muestra los semestres del más antiguo al más reciente (head -> tail)."""
        print("↳ Recorrido hacia adelante:")
        if self.esta_vacia():
            print("  (no hay semestres)")
        actual = self.head
        while actual:
            self.mostrar_semestre(actual.valor)
            actual = actual.siguiente

    def recorrer_atras(self):
        """Muestra los semestres del más reciente al más antiguo (tail -> head)."""
        print("↳ Recorrido hacia atrás:")
        if self.esta_vacia():
            print("  (no hay semestres)")
        actual = self.tail
        while actual:
            self.mostrar_semestre(actual.valor)
            actual = actual.anterior

    def resumen(self, hacia_atras=False):
        """Retorna un texto corto con el orden de los semestres, p. ej. '2023-2 <-> 2024-1'."""
        texto = ""
        actual = self.tail if hacia_atras else self.head
        while actual:
            texto += f"{actual.valor['año']}-{actual.valor['term']}"
            actual = actual.anterior if hacia_atras else actual.siguiente
            if actual:
                texto += " <-> "
        return texto

    def top_promedios(self, k=3):
        """
        Muestra los k semestres con mejor promedio.
        No usa sorted(): arma una lista enlazada auxiliar ordenada de mayor a menor.
        """
        head_aux = None
        actual = self.head
        while actual:
            p = promedio(actual.valor)
            nuevo = NodoSimple((p, actual.valor))
            if head_aux is None or p > head_aux.valor[0]:    # va al inicio
                nuevo.siguiente = head_aux
                head_aux = nuevo
            else:                                           # buscar su lugar
                aux = head_aux
                while aux.siguiente and aux.siguiente.valor[0] >= p:
                    aux = aux.siguiente
                nuevo.siguiente = aux.siguiente
                aux.siguiente = nuevo
            actual = actual.siguiente

        print(f"🏆 Top {k} mejores promedios:")
        if head_aux is None:
            print("  (no hay semestres)")
        aux = head_aux
        posicion = 1
        while aux and posicion <= k:
            p, s = aux.valor
            print(f"  {posicion}. {s['año']}-{s['term']}  promedio {p:.2f}")
            aux = aux.siguiente
            posicion += 1

    def limpiar(self):
        """Deja la lista vacía."""
        self.head = None
        self.tail = None
        self.tamaño = 0

    # ------------------ persistencia ------------------
    def to_dict(self):
        """Convierte el historial en un diccionario (estructura jerárquica para JSON)."""
        semestres = []
        actual = self.head
        while actual:
            s = actual.valor
            semestres.append({"año": s["año"], "term": s["term"],
                              "materias": [dict(m) for m in s["materias"]]})
            actual = actual.siguiente
        return {"tipo": "ListaDoble", "semestres": semestres}

    def from_dict(self, datos):
        """Reconstruye el historial a partir de un diccionario leído de JSON."""
        if datos.get("tipo") != "ListaDoble":
            raise ValueError("Los datos no corresponden a una ListaDoble")
        self.limpiar()
        for s in datos["semestres"]:
            self.insertar_ordenado(s)

    def exportar_json(self, ruta):
        """Guarda el historial en un archivo JSON (usa persistencia_json.py)."""
        persistencia_json.exportar_json(self, ruta)

    def importar_json(self, ruta):
        """Carga el historial desde un archivo JSON (usa persistencia_json.py)."""
        persistencia_json.importar_json(self, ruta)

import persistencia_csv
from nodo_simple import NodoSimple


def validar_estudiante(estudiante):
    """
    Revisa los datos de un estudiante antes de guardarlos.

    Parámetros:
        estudiante (dict): {"id": solo números, "nombres": texto, "correo": texto}.

    Retorna:
        dict: el estudiante con los datos limpios.

    Lanza:
        ValueError: si algún valor no es válido.
    """
    id_est = str(estudiante.get("id", "")).strip()
    nombres = str(estudiante.get("nombres", "")).strip()
    correo = str(estudiante.get("correo", "")).strip().lower()

    if not id_est.isdigit():
        raise ValueError(f"ID inválido '{id_est}': debe tener solo números")
    if nombres == "" or len(nombres) > 80:
        raise ValueError("Los nombres no pueden estar vacíos ni pasar de 80 caracteres")
    if correo.count("@") != 1 or "." not in correo.split("@")[1] or " " in correo:
        raise ValueError(f"Correo inválido '{correo}'")

    return {"id": id_est, "nombres": nombres, "correo": correo}


class ListaSimple:
    """
    Lista simplemente enlazada de estudiantes inscritos en una asignatura.

    Atributos:
        head (NodoSimple): primer nodo de la lista.
        tail (NodoSimple): último nodo (permite insertar al final en O(1)).
        tamaño (int): cantidad de estudiantes.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.tamaño = 0

    def esta_vacia(self):
        """Retorna True si la lista no tiene estudiantes."""
        return self.head is None

    def insertar_final(self, estudiante):
        """
        Agrega un estudiante al final de la lista.

        Parámetros:
            estudiante (dict): {"id": ..., "nombres": ..., "correo": ...}

        Lanza:
            ValueError: si los datos son inválidos o el id ya existe.
        """
        estudiante = validar_estudiante(estudiante)
        if self.buscar(estudiante["id"]) is not None:
            raise ValueError(f"Ya existe un estudiante con id {estudiante['id']}")

        nuevo = NodoSimple(estudiante)
        if self.head is None:            # lista vacía: el nuevo es head y tail
            self.head = nuevo
            self.tail = nuevo
        else:                            # se enlaza después del tail actual
            self.tail.siguiente = nuevo
            self.tail = nuevo
        self.tamaño += 1
        print(f"✅ Inscrito {estudiante['id']} - {estudiante['nombres']}")

    def buscar(self, id_est):
        """
        Busca un estudiante por su id.

        Retorna:
            dict: el estudiante encontrado, o None si no existe.
        """
        actual = self.head
        while actual:
            if actual.valor["id"] == str(id_est).strip():
                return actual.valor
            actual = actual.siguiente
        return None

    def eliminar(self, id_est):
        """
        Elimina al estudiante con el id indicado.

        Retorna:
            dict: el estudiante eliminado, o None si no se encontró.
        """
        id_est = str(id_est).strip()
        anterior = None
        actual = self.head
        while actual:
            if actual.valor["id"] == id_est:
                if anterior is None:                 # era el head
                    self.head = actual.siguiente
                else:                                # "puentear" el nodo
                    anterior.siguiente = actual.siguiente
                if actual == self.tail:              # era el tail
                    self.tail = anterior
                self.tamaño -= 1
                print(f"XXXX Eliminado {actual.valor['id']} - {actual.valor['nombres']}")
                return actual.valor
            anterior = actual
            actual = actual.siguiente
        print(f"⚠ No existe el estudiante con id {id_est}")
        return None

    def recorrer(self):
        """Muestra todos los estudiantes, desde el head hasta el tail."""
        if self.esta_vacia():
            print("  (no hay inscritos)")
            return
        print(f"  {'ID':<8}{'NOMBRES':<20}CORREO")
        actual = self.head
        while actual:
            e = actual.valor
            print(f"  {e['id']:<8}{e['nombres']:<20}{e['correo']}")
            actual = actual.siguiente
        print(f"  Total inscritos: {self.tamaño}")

    def limpiar(self):
        """Deja la lista vacía."""
        self.head = None
        self.tail = None
        self.tamaño = 0

    # ------------------ persistencia ------------------
    def to_dict(self):
        """
        Convierte la lista en un diccionario para guardarlo en un archivo.
        (La lista de Python solo se usa aquí, para empaquetar los datos.)
        """
        estudiantes = []
        actual = self.head
        while actual:
            estudiantes.append(dict(actual.valor))
            actual = actual.siguiente
        return {"tipo": "ListaSimple", "estudiantes": estudiantes}

    def from_dict(self, datos):
        """
        Reconstruye la lista a partir de un diccionario leído de un archivo.
        Cada estudiante se inserta con insertar_final(), así pasa por las
        mismas validaciones que un valor escrito por teclado.
        """
        if datos.get("tipo") != "ListaSimple":
            raise ValueError("Los datos no corresponden a una ListaSimple")
        self.limpiar()
        for e in datos["estudiantes"]:
            self.insertar_final(e)

    def exportar_csv(self, ruta):
        """Guarda los inscritos en un archivo CSV (usa persistencia_csv.py)."""
        persistencia_csv.exportar_csv(self, ruta)

    def importar_csv(self, ruta):
        """Carga los inscritos desde un archivo CSV (usa persistencia_csv.py)."""
        persistencia_csv.importar_csv(self, ruta)

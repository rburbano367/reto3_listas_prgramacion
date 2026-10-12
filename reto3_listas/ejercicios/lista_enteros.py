class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaSimple:
    def __init__(self):
        self.head = None

    def insertar_inicio(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.head
        self.head = nuevo
        print(f"✅ Insertado {dato} al inicio")

    def insertar_final(self, dato):
        nuevo = Nodo(dato)
        if self.head is None:
            self.head = nuevo
        else:
            actual = self.head
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        print(f"✅ Insertado {dato} al final")

    def eliminar(self, dato):
        actual = self.head
        anterior = None
        while actual:
            if actual.dato == dato:
                if anterior is None:
                    self.head = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                print(f"❌ Eliminado {dato}")
                return
            anterior = actual
            actual = actual.siguiente
        print(f"⚠ {dato} no encontrado")

    def recorrer(self):
        actual = self.head
        while actual:
            print(actual.dato, end=" -> ")
            actual = actual.siguiente
        print("None")


if __name__ == "__main__":
    lista = ListaSimple()
    lista.insertar_final(10)
    lista.insertar_final(20)
    lista.insertar_final(30)
    lista.insertar_inicio(5)
    lista.recorrer()
    lista.eliminar(20)
    lista.recorrer()

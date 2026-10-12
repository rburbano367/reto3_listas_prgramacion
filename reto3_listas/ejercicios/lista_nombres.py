class NodoDoble:
    def __init__(self, nombre):
        self.nombre = nombre
        self.anterior = None
        self.siguiente = None


class ListaDoble:
    def __init__(self):
        self.head = None
        self.tail = None

    def insertar_cabeza(self, nombre):
        nuevo = NodoDoble(nombre)
        if self.head is None:
            self.head = self.tail = nuevo
        else:
            nuevo.siguiente = self.head
            self.head.anterior = nuevo
            self.head = nuevo
        print(f"✅ Insertado {nombre} en cabeza")

    def insertar_cola(self, nombre):
        nuevo = NodoDoble(nombre)
        if self.tail is None:
            self.head = self.tail = nuevo
        else:
            nuevo.anterior = self.tail
            self.tail.siguiente = nuevo
            self.tail = nuevo
        print(f"✅ Insertado {nombre} en cola")

    def eliminar_cabeza(self):
        if self.head is None:
            print("!!!!!! Lista vacia")
            return
        eliminado = self.head.nombre
        self.head = self.head.siguiente
        if self.head:
            self.head.anterior = None
        else:
            self.tail = None
        print(f" xxxx Eliminado {eliminado} de cabeza")

    def eliminar_cola(self):
        if self.tail is None:
            print("!!!!!! Lista vacia")
            return
        eliminado = self.tail.nombre
        self.tail = self.tail.anterior
        if self.tail:
            self.tail.siguiente = None
        else:
            self.head = None
        print(f" xxxx Eliminado {eliminado} de cola")

    def recorrer_adelante(self):
        actual = self.head
        print("↳ Recorrido hacia adelante:")
        while actual:
            print(actual.nombre, end=" <-> ")
            actual = actual.siguiente
        print("None")

    def recorrer_atras(self):
        actual = self.tail
        print("↳ Recorrido hacia atrás:")
        while actual:
            print(actual.nombre, end=" <-> ")
            actual = actual.anterior
        print("None")


if __name__ == "__main__":
    lista = ListaDoble()
    lista.insertar_cabeza("Ana")
    lista.insertar_cola("Luis")
    lista.insertar_cabeza("Marta")
    lista.insertar_cola("Pedro")
    lista.recorrer_adelante()
    lista.recorrer_atras()
    lista.eliminar_cabeza()
    lista.eliminar_cola()
    lista.recorrer_adelante()

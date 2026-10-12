class NodoDoble:
    """
    Nodo de una lista doblemente enlazada.

    Atributos:
        valor: información que guarda el nodo (aquí, un semestre).
        anterior (NodoDoble): referencia al nodo previo o None.
        siguiente (NodoDoble): referencia al nodo posterior o None.
    """

    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.siguiente = None

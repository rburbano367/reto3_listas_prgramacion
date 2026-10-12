class NodoSimple:
    """
    Nodo de una lista simplemente enlazada.

    Atributos:
        valor: información que guarda el nodo (aquí, un estudiante).
        siguiente (NodoSimple): referencia al siguiente nodo o None.
    """

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

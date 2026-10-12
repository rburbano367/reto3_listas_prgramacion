class NodoCircular:
    """
    Nodo de una lista circular simple.

    Atributos:
        valor: información que guarda el nodo (aquí, un grupo de prácticas).
        siguiente (NodoCircular): referencia al siguiente nodo.
            En el último nodo apunta de nuevo al primero.
    """

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

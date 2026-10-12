def hanoi(n, origen, auxiliar, destino):
    """Mueve n discos de origen a destino usando auxiliar (recursividad múltiple)."""
    # Caso base: mover un solo disco
    if n == 1:
        print(f"  Mover disco 1 de {origen} a {destino}")
        return 1
    # Paso 1: mover n-1 discos al auxiliar
    movimientos = hanoi(n - 1, origen, destino, auxiliar)
    # Paso 2: mover el disco más grande al destino
    print(f"  Mover disco {n} de {origen} a {destino}")
    # Paso 3: mover n-1 discos del auxiliar al destino
    movimientos += hanoi(n - 1, auxiliar, origen, destino)
    return movimientos + 1


total = hanoi(3, "A", "B", "C")
print(f"Total: {total} movimientos (2^3 - 1 = 7)")

"""Prueba de las limitaciones de la recursividad en Python (tema 9.4).

Ejecutar:  python prueba_limites_recursion.py

Demuestra 5 cosas:
  1. El límite por defecto (~1000) y el RecursionError al superarlo.
  2. Que Python NO optimiza la recursión de cola (tail-call).
  3. Qué pasa al subir el límite con sys.setrecursionlimit() (se ejecuta en un
     SUBPROCESO, así si el intérprete se cae no se cae esta prueba).
  4. El costo extra de tiempo de la recursión frente a un bucle.
  5. El impacto en el reto: buscar_recursivo() con demasiados grupos.
"""

import contextlib
import io
import subprocess
import sys
import textwrap
import time


def titulo(t):
    print("\n" + "=" * 64 + f"\n {t}\n" + "=" * 64)


# ------------------------------------------------------------------
# 1. Límite por defecto y RecursionError
# ------------------------------------------------------------------
def contar(n):
    """Recursión simple: profundidad = n."""
    if n == 0:
        return 0
    return 1 + contar(n - 1)


def prueba_1():
    titulo("1. Límite por defecto y RecursionError")
    print(f"sys.getrecursionlimit() = {sys.getrecursionlimit()}")
    for n in (500, 900, 1000, 5000):
        try:
            contar(n)
            print(f"  contar({n:>5}) -> OK")
        except RecursionError as e:
            print(f"  contar({n:>5}) -> RecursionError: {e}")
    print("  Nota: falla un poco antes de 1000 porque la pila ya tiene")
    print("  algunos marcos ocupados (main, prueba_1, etc.).")


# ------------------------------------------------------------------
# 2. Sin optimización de recursión de cola
# ------------------------------------------------------------------
def contar_cola(n, acumulado=0):
    """Versión 'de cola': la llamada recursiva es lo ÚLTIMO que se hace.
    En lenguajes con TCO (Scheme, Scala) esto no crecería la pila.
    En Python sí crece, así que falla igual."""
    if n == 0:
        return acumulado
    return contar_cola(n - 1, acumulado + 1)


def contar_iterativo(n):
    acumulado = 0
    while n > 0:
        acumulado += 1
        n -= 1
    return acumulado


def prueba_2():
    titulo("2. Python NO optimiza la recursión de cola")
    try:
        contar_cola(5000)
        print("  contar_cola(5000) -> OK (habría TCO)")
    except RecursionError:
        print("  contar_cola(5000) -> RecursionError: aunque es recursión de cola,")
        print("                       cada llamada sigue ocupando un marco en la pila.")
    print(f"  contar_iterativo(5000) = {contar_iterativo(5000)}  (el bucle no tiene límite)")


# ------------------------------------------------------------------
# 3. Subir el límite con setrecursionlimit (en un subproceso)
# ------------------------------------------------------------------
CODIGO_HIJO = textwrap.dedent("""
    import sys, resource
    sys.setrecursionlimit(10**7)          # límite "sin control"
    def contar(n):
        return 0 if n == 0 else 1 + contar(n - 1)
    n = int(sys.argv[1])
    contar(n)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024
    print(f"OK, memoria máxima usada ~{rss} MB")
""")

# Recursión que pasa por código C: repr() de una lista enlazada de n nodos.
# Cada nivel consume pila REAL del intérprete (no solo marcos de Python).
CODIGO_HIJO_C = textwrap.dedent("""
    import sys
    sys.setrecursionlimit(10**7)
    class Nodo:
        def __init__(self, sig):
            self.sig = sig
        def __repr__(self):
            return "N" if self.sig is None else "N->" + repr(self.sig)
    cabeza = None
    for _ in range(int(sys.argv[1])):
        cabeza = Nodo(cabeza)
    print(f"OK, repr de {len(repr(cabeza)):,} caracteres")
""")

# En Windows no existe el módulo 'resource': versión sin medición de memoria
CODIGO_HIJO_WIN = CODIGO_HIJO.replace("import sys, resource", "import sys").replace(
    'rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024\n'
    'print(f"OK, memoria máxima usada ~{rss} MB")', 'print("OK")')


def ejecutar_hijo(codigo, valores):
    for n in valores:
        try:
            r = subprocess.run([sys.executable, "-c", codigo, str(n)],
                               capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            print(f"  profundidad {n:>9,}: el proceso tardó demasiado (timeout)")
            continue
        if r.returncode == 0:
            print(f"  profundidad {n:>9,}: {r.stdout.strip()}")
        elif r.returncode < 0 or r.returncode in (3221225725, -1073741571):
            # -11 = SIGSEGV en Linux/macOS; 0xC00000FD = stack overflow en Windows
            print(f"  profundidad {n:>9,}: ¡EL INTÉRPRETE SE CAYÓ! (código {r.returncode}, "
                  "desbordamiento de pila)")
        else:
            ultima = (r.stderr.strip().splitlines() or ["?"])[-1]
            print(f"  profundidad {n:>9,}: error -> {ultima}")


def prueba_3():
    titulo("3. Subir el límite con sys.setrecursionlimit(10**7)")
    print(f"  Versión de Python: {sys.version.split()[0]}")
    print("  a) Recursión Python pura (contar):")
    ejecutar_hijo(CODIGO_HIJO_WIN if sys.platform == "win32" else CODIGO_HIJO,
                  (10_000, 100_000, 1_000_000))
    print("  b) Recursión que pasa por C (repr de una lista enlazada):")
    ejecutar_hijo(CODIGO_HIJO_C, (1_000, 200_000))
    print("  Interpretación:")
    print("   - (a) Desde Python 3.11 las llamadas Python->Python no gastan pila de C:")
    print("     no se cae, pero la memoria crece con cada marco (riesgo de DoS).")
    print("   - (b) Si la recursión pasa por C (repr, str, json, etc.):")
    print("     * Python 3.11 o anterior: el proceso MUERE (Segmentation fault).")
    print("     * Python 3.12+: un límite interno de C lo frena con RecursionError.")


# ------------------------------------------------------------------
# 4. Costo de tiempo: recursión vs bucle
# ------------------------------------------------------------------
def prueba_4():
    titulo("4. Costo de tiempo: recursión vs bucle (n = 900, 2000 repeticiones)")
    rep = 2000
    t0 = time.perf_counter()
    for _ in range(rep):
        contar(900)
    t_rec = time.perf_counter() - t0
    t0 = time.perf_counter()
    for _ in range(rep):
        contar_iterativo(900)
    t_it = time.perf_counter() - t0
    print(f"  Recursivo : {t_rec:.3f} s")
    print(f"  Iterativo : {t_it:.3f} s")
    print(f"  La recursión es ~{t_rec / t_it:.1f} veces más lenta (crear y destruir marcos).")


# ------------------------------------------------------------------
# 5. Impacto en el reto: buscar_recursivo sin el límite MAX_GRUPOS
# ------------------------------------------------------------------
def prueba_5():
    titulo("5. Impacto en el reto: lista circular SIN límite de grupos")
    import lista_circular
    original = lista_circular.MAX_GRUPOS
    lista_circular.MAX_GRUPOS = 10**6          # simulamos que NO hubiera control
    lc = lista_circular.ListaCircular()
    try:
        with contextlib.redirect_stdout(io.StringIO()):   # oculta los mensajes "✅ Grupo..."
            for i in range(5000):               # p. ej. un grupos.json manipulado
                lc.insertar({"nombre_grupo": f"G{i}", "tutor": "T", "tema": ""})
        print("  Se insertaron 5000 grupos sin error")
    except RecursionError:
        print(f"  RecursionError al insertar el grupo #{lc.tamaño + 1}:")
        print("  insertar() llama a buscar_recursivo() para evitar duplicados y la")
        print("  pila se agota -> un archivo grande tumba la importación (DoS).")
    finally:
        lista_circular.MAX_GRUPOS = original
    print(f"  Con el control real MAX_GRUPOS = {original}, el grupo {original + 1} se rechaza")
    print("  con un mensaje claro y el programa sigue funcionando.")


if __name__ == "__main__":
    prueba_1()
    prueba_2()
    prueba_3()
    prueba_4()
    prueba_5()

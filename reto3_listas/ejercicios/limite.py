import sys
def contar(n):
    return 0 if n == 0 else 1 + contar(n - 1)
print("Límite de recursión:", sys.getrecursionlimit())
print("contar(900) =", contar(900))
try:
    contar(5000)
except RecursionError as e:
    print("contar(5000) -> RecursionError:", e)

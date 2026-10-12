"""
Reto 3 - Listas enlazadas para registros académicos.
Menú principal en consola que integra las tres listas y su persistencia.
"""

import os

from lista_simple import ListaSimple
from lista_doble import ListaDoble, convertir_semestre
from lista_circular import ListaCircular

# Carpeta data/ al lado de src/
CARPETA_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
RUTA_INSCRITOS = os.path.join(CARPETA_DATA, "inscritos.csv")
RUTA_HISTORIAL = os.path.join(CARPETA_DATA, "historial.json")
RUTA_GRUPOS = os.path.join(CARPETA_DATA, "grupos.json")

inscritos = ListaSimple()
historial = ListaDoble()
grupos = ListaCircular()


def leer_entero(mensaje):
    """Pide un número entero; si el usuario escribe otra cosa lanza ValueError con un mensaje claro."""
    texto = input(mensaje).strip()
    if not texto.lstrip("-").isdigit():
        raise ValueError(f"'{texto}' no es un número entero")
    return int(texto)


def leer_nota(mensaje):
    """Pide una nota decimal; si no es un número lanza ValueError con un mensaje claro."""
    texto = input(mensaje).strip().replace(",", ".")   # acepta 8,5 o 8.5
    try:
        return float(texto)
    except ValueError:
        raise ValueError(f"'{texto}' no es una nota válida")


def menu_inscritos():
    """Submenú 1: estudiantes inscritos (lista simple)."""
    while True:
        print("\n--- 1. INSCRITOS (Lista Simple) ---")
        print("1) Agregar  2) Eliminar  3) Buscar  4) Mostrar  5) Exportar CSV  6) Importar CSV  0) Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                id_est = input("  id: ")
                nombres = input("  nombres: ")
                correo = input("  correo: ")
                inscritos.insertar_final({"id": id_est, "nombres": nombres, "correo": correo})
            elif opcion == "2":
                inscritos.eliminar(input("  id a eliminar: "))
            elif opcion == "3":
                e = inscritos.buscar(input("  id a buscar: "))
                if e:
                    print(f"  Successful::::: Encontrado: {e['id']} | {e['nombres']} | {e['correo']}")
                else:
                    print("  !!!!!! No encontrado")
            elif opcion == "4":
                inscritos.recorrer()
            elif opcion == "5":
                inscritos.exportar_csv(RUTA_INSCRITOS)
            elif opcion == "6":
                inscritos.importar_csv(RUTA_INSCRITOS)
            elif opcion == "0":
                return
            else:
                print("  Opción no válida")
        except (ValueError, FileNotFoundError) as error:
            print(f"  ⚠ Error: {error}")


def menu_historial():
    """Submenú 2: historial académico (lista doble)."""
    while True:
        print("\n--- 2. HISTORIAL (Lista Doble) ---")
        print("1) Agregar semestre  2) Buscar  3) Recorrer adelante  4) Recorrer atrás  "
              "5) Eliminar  6) Exportar JSON  7) Importar JSON  0) Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                año, term = convertir_semestre(input("  semestre (AAAA-T): "))
                cantidad = leer_entero("  ¿cuántas materias?: ")
                materias = []
                for i in range(cantidad):
                    print(f"  Materia {i + 1}")
                    materias.append({"cod": input("    código: "),
                                     "nombre": input("    nombre: "),
                                     "nota": leer_nota("    nota (0-10): ")})
                historial.insertar_ordenado({"año": año, "term": term, "materias": materias})
            elif opcion == "2":
                s = historial.buscar(input("  semestre (AAAA-T): "))
                if s:
                    historial.mostrar_semestre(s)
                else:
                    print("  !!!!!! No encontrado")
            elif opcion == "3":
                historial.recorrer_adelante()
            elif opcion == "4":
                historial.recorrer_atras()
            elif opcion == "5":
                historial.eliminar(input("  semestre a eliminar (AAAA-T): "))
            elif opcion == "6":
                historial.exportar_json(RUTA_HISTORIAL)
            elif opcion == "7":
                historial.importar_json(RUTA_HISTORIAL)
            elif opcion == "0":
                return
            else:
                print("  Opción no válida")
        except (ValueError, KeyError, FileNotFoundError) as error:
            print(f"  ⚠ Error: {error}")


def menu_grupos():
    """Submenú 3: rotación de grupos de prácticas (lista circular)."""
    while True:
        print("\n--- 3. GRUPOS (Lista Circular) ---")
        print("1) Agregar  2) Eliminar  3) Buscar (recursivo)  4) Rotar  5) Recorrer  "
              "6) Exportar JSON  7) Importar JSON  0) Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                nombre = input("  nombre_grupo: ")
                tutor = input("  tutor: ")
                tema = input("  tema: ")
                grupos.insertar({"nombre_grupo": nombre, "tutor": tutor, "tema": tema})
            elif opcion == "2":
                if grupos.eliminar(input("  nombre_grupo a eliminar: ")):
                    print(f"  ¿El ciclo sigue cerrado? {grupos.es_circular()}")
            elif opcion == "3":
                r = grupos.buscar_recursivo(input("  nombre_grupo a buscar: "))
                if r:
                    print(f"  Successful::::: Encontrado a {r[0]} turno(s) del actual: {r[1]}")
                else:
                    print("  !!!!!! No encontrado")
            elif opcion == "4":
                grupos.rotar(leer_entero("  ¿cuantas posiciones (k)?: "))
            elif opcion == "5":
                vueltas = input("  ¿cuántas vueltas? [1]: ").strip()
                grupos.mostrar()
                if not grupos.esta_vacia():
                    # Si el usuario solo presiona Enter (texto vacío), se usa 1 vuelta.
                    grupos.recorrer(int(vueltas) if vueltas.isdigit() else 1)
            elif opcion == "6":
                grupos.exportar_json(RUTA_GRUPOS)
            elif opcion == "7":
                grupos.importar_json(RUTA_GRUPOS)
            elif opcion == "0":
                return
            else:
                print("  Opción no válida")
        except (ValueError, KeyError, FileNotFoundError, OverflowError) as error:
            print(f"  ⚠ Error: {error}")


def menu_reportes():
    """Opción 4: reportes generales."""
    print("\n--- 4. REPORTES ---")
    historial.top_promedios(3)
    turno = grupos.siguiente_turno()
    if turno:
        print(f"👥 Siguiente grupo en turno: {turno['nombre_grupo']} ({turno['tutor']})")
    else:
        print("👥 Siguiente grupo en turno: no hay grupos")
    print(f"🎓 Cantidad de inscritos: {inscritos.tamaño}")


def main():
    """Muestra el menú principal hasta que el usuario elija Salir."""
    os.makedirs(CARPETA_DATA, exist_ok=True)
    while True:
        print("\n========= RETO 3 - LISTAS ENLAZADAS =========")
        print("1. Inscritos  2. Historial  3. Grupos  4. Reportes  5. Salir")
        opcion = input("Seleccione: ").strip()
        if opcion == "1":
            menu_inscritos()
        elif opcion == "2":
            menu_historial()
        elif opcion == "3":
            menu_grupos()
        elif opcion == "4":
            menu_reportes()
        elif opcion == "5":
            print(">>>>>>> Hasta luego <<<<<<<")
            break
        else:
            print("Opción no válida")



main()

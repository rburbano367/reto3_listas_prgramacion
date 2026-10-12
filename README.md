# Reto 3 - Listas enlazadas para registros academicos

Proyecto hecho por un estudiante de ciberseguridad. Modulo en Python 3 sin librerias externas, pensado con mentalidad
de seguridad: validar toda entrada, no confiar en archivos externos y probar los casos limite antes de que alguien
mas los pruebe por nosotros.

Sigue las convenciones de las clases 11-14 de Programacion II con los nombres exactos de la rubrica: nodos con `valor`,
listas con `head`/`tail`, recorridos con `while`, docstrings (PEP 257), pruebas con `unittest` y persistencia con
`csv` y `json`.

## Enfoque de ciberseguridad
- **Validacion de entrada:** los datos de inscritos, historial y grupos se revisan antes de insertarse.
- **Archivos no confiables:** los CSV y JSON importados se tratan como entrada hostil (archivos manipulados o corruptos).
- **CSV Injection:** se prueban celdas que empiezan con `=`, `+`, `-` o `@` para evitar formulas maliciosas al abrir en hojas de calculo.
- **Limites y robustez:** se prueba la recursividad (riesgo de desbordamiento de pila) y listas vacias o con un solo nodo.
- **Pruebas aleatorias (fuzzing basico):** miles de operaciones al azar comparadas contra un modelo de referencia.

## Estructura
```
reto3_listas/
  src/
    nodo_simple.py  nodo_doble.py  nodo_circular.py
    lista_simple.py        # Inscritos: insertar_final, eliminar, buscar, recorrer
    lista_doble.py         # Historial: insertar_ordenado, recorrer_adelante/atras
    lista_circular.py      # Grupos: buscar_recursivo, rotar, recorrer
    persistencia_csv.py    # inscritos -> data/inscritos.csv
    persistencia_json.py   # historial -> data/historial.json, grupos -> data/grupos.json
    app.py                 # menu principal
    casos_prueba.py        # casos minimos del video
    test_listas.py         # 22 pruebas unitarias (unittest)
    prueba_aleatoria.py    # 36 000 operaciones al azar contra un modelo
    pruebas_seguridad.py   # archivos manipulados / CSV Injection / limites
    prueba_limites_recursion.py
  data/
  ejercicios/              # Hanoi, limite de recursion, ejercicios 10.6, 11.6, 12.6
```

## Como ejecutar
```bash
cd src
python app.py                        # menu interactivo
python casos_prueba.py simple        # (o doble, circular; sin argumento ejecuta los tres)
python -m unittest test_listas -v    # pruebas unitarias
python prueba_aleatoria.py           # prueba aleatoria
python pruebas_seguridad.py          # pruebas de robustez
python prueba_limites_recursion.py   # limites de la recursividad
```

## Que mostrar en el video
1. **Lista simple:** agregar 3 inscritos, buscar y eliminar 1, mostrar, exportar CSV, limpiar, importar y mostrar.
2. **Lista doble:** insertar semestres desordenados y comprobar que quedan ordenados; recorrer adelante/atras; exportar/importar JSON.
3. **Lista circular:** agregar 3 grupos, `buscar_recursivo`, `rotar(2)` y ver el ciclo; eliminar uno y ver que el ciclo se conserva.

## Uso rapido (firmas de la rubrica)
```python
inscritos.insertar_final({"id": "1001", "nombres": "Ana Torres", "correo": "ana@uni.edu.ec"})
historial.insertar_ordenado({"año": 2024, "term": 1, "materias": [{"cod": "MAT201", "nombre": "Discreta", "nota": 7.8}]})
grupos.insertar({"nombre_grupo": "G1", "tutor": "Ing. Rivas", "tema": "Firewall"})
inscritos.exportar_csv("../data/inscritos.csv")      # importar_csv(ruta)
historial.exportar_json("../data/historial.json")   # importar_json(ruta)
```

## Notas finales
Este proyecto es academico. Los datos de ejemplo son ficticios y no deben usarse con informacion personal real
sin antes aplicar cifrado y control de acceso a los archivos de `data/`.

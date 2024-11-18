"""
Este script filtra un archivo CSV llamado 'PopularPlaces.csv' para eliminar filas
cuyo tipo ('type') se encuentre en una lista de tipos especificados en otro archivo
CSV llamado 'types_not_in_markov.csv'. El resultado filtrado se guarda en un nuevo
archivo CSV llamado 'filtered_Popular_Places.csv'.

El proceso consiste en los siguientes pasos:
1. Carga de los archivos CSV: 'PopularPlaces.csv' y 'types_not_in_markov.csv'.
2. Extracción del primer tipo ('type') de cada fila en 'PopularPlaces.csv' antes del
   símbolo '+' (si está presente).
3. Identificación de los tipos ('type') que deben eliminarse utilizando la lista en
   'types_not_in_markov.csv'.
4. Filtrado del DataFrame original para eliminar las filas que contienen los tipos a
   eliminar.
5. Guardado del resultado filtrado en un nuevo archivo CSV.

Excepciones:
- Si ocurre un error al cargar los archivos CSV, el script imprime un mensaje de
  error y finaliza la ejecución.

Archivos de entrada:
- 'PopularPlaces.csv': Contiene una columna llamada 'type'.
- 'types_not_in_markov.csv': Contiene una columna llamada 'type' con los valores
  que deben eliminarse de 'PopularPlaces.csv'.

Archivo de salida:
- 'filtered_Popular_Places.csv': Archivo CSV con los datos filtrados.

"""
import pandas as pd

try:
    # Carga de los archivos CSV
    popular_places = pd.read_csv('PopularPlaces.csv')
    types_not_in_markov = pd.read_csv('types_not_in_markov.csv')
except Exception as e:
    print(f"Error al leer los archivos: {e}")
    exit(1)

# Extrae el primer type antes del '+' en Popular_Places
popular_places['type'] = popular_places['type'].str.split('+').str[0]

# Obtengo los types que voy a eliminar
types_to_remove = types_not_in_markov['type']

# Filtro el DataFrame de Popular_Places para eliminar las filas con esos types
filtered_popular_places = popular_places[~popular_places['type'].isin(types_to_remove)]

# Guardo el resultado en un archivo CSV
filtered_popular_places.to_csv('filtered_Popular_Places.csv', index=False)

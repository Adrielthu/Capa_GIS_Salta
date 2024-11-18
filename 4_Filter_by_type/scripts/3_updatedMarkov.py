"""
Este script toma un archivo CSV llamado 'filtered_Popular_Places.csv' y reemplaza
los valores en la columna 'type' basándose en un mapeo definido en otro archivo
CSV llamado 'places_markov.csv'. El archivo resultante se guarda como
'UpdatedPopularPlaces.csv'.

El proceso sigue los siguientes pasos:
1. Carga de los archivos CSV: 'places_markov.csv' y 'filtered_Popular_Places.csv'.
2. Creación de un diccionario de reemplazo a partir de las columnas
   '# Google_Maps_type' y 'Google_Place_type' en 'places_markov.csv'.
3. Reemplazo de los valores en la columna 'type' del DataFrame de
   'filtered_Popular_Places.csv' utilizando el diccionario de mapeo.
4. Guardado del DataFrame actualizado en un archivo CSV llamado 'UpdatedPopularPlaces.csv'.

Excepciones:
- Si ocurre un error al cargar los archivos CSV, el script imprime un mensaje de
  error y finaliza la ejecución.

Archivos de entrada:
- 'places_markov.csv': Contiene dos columnas, '# Google_Maps_type' y
  'Google_Place_type', que definen el mapeo entre tipos.
- 'filtered_Popular_Places.csv': Contiene una columna llamada 'type' con los
  valores que serán reemplazados.

Archivo de salida:
- 'UpdatedPopularPlaces.csv': Archivo CSV con los valores de la columna 'type'
  reemplazados según el mapeo definido en 'places_markov.csv'.
"""
import pandas as pd

try:
    # Carga de los archivos CSV
    places_markov = pd.read_csv('places_markov.csv')
    popular_places = pd.read_csv('filtered_Popular_Places.csv')
except Exception as e:
    print(f"Error al leer los archivos: {e}")
    exit(1)

# Creo un diccionario a partir de places_markov para hacer el reemplazo
replace_dict = dict(zip(places_markov['# Google_Maps_type'], places_markov['Google_Place_type']))

# Reemplaza los valores en la columna 'type' de Popular_Places según el diccionario
popular_places['type'] = popular_places['type'].replace(replace_dict)

# Guarda el resultado en un archivo CSV
popular_places.to_csv('UpdatedPopularPlaces.csv', index=False)

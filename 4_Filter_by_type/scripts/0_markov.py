"""
Este script compara los tipos de lugares entre dos archivos CSV y filtra aquellos que no están
presentes en un archivo de referencia. Luego, guarda los resultados en un nuevo archivo CSV. Los pasos principales son:

1. Cargar archivos CSV:
   - Se cargan dos archivos: `places_markov.csv` que contiene una columna de tipos de lugares de Google Maps (`Google_Maps_type`), y `PopularPlaces_FilledType.csv` que contiene los tipos de lugares de lugares populares (`type`).

2. Extracción de columnas relevantes:
   - Extrae las columnas relevantes de ambos DataFrames: `Google_Maps_type` de `places_markov` y `type` de `popular_places`.

3. Filtrado de tipos no presentes en Markov:
   - Identifica los tipos de lugares en `popular_places` que no están presentes en `Google_Maps_type` de `places_markov`.

4. Filtrado adicional:
   - Elimina los tipos que contienen el carácter '+' en sus nombres, lo que indica tipos compuestos.

5. Conteo de ocurrencias:
   - Cuenta cuántas veces aparece cada tipo de lugar no presente en el archivo Markov.

6. Renombrado de columnas:
   - Renombra las columnas del DataFrame resultante a 'type' y 'count' para que sean más descriptivas.

7. Guardar resultados:
   - Guarda el DataFrame con los tipos no presentes y su cantidad de ocurrencias en un archivo CSV llamado `types_not_in_markov.csv`.
"""
import pandas as pd

try:
   # Cargar los archivos CSV
   places_markov = pd.read_csv('places_markov.csv')
   popular_places = pd.read_csv('../3_filtro_por_cercania/Divisor_de_csv/PopularPlaces_FilledType.csv')
except Exception as e:
    print(f"Error al leer los archivos: {e}")
    exit(1)


# Obtengo las columnas relevantes de cada DataFrame
place_types_markov = places_markov['# Google_Maps_type']
popular_types = popular_places['type']

# Filtro los types de Popular_Places que no están en Google_Place_type de places_markov
types_not_in_markov = popular_types[~popular_types.isin(place_types_markov)]

# Elimino los types que contienen '+'
types_not_in_markov = types_not_in_markov[~types_not_in_markov.str.contains(r'\+')]

# Cuento las ocurrencias de cada type
type_counts = types_not_in_markov.value_counts().reset_index()

# Renombro las columnas
type_counts.columns = ['type', 'count']

# Guardar el resultado en un archivo CSV
type_counts.to_csv('types_not_in_markov.csv', index=False)
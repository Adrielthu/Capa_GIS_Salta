"""
Este script lee un archivo CSV de entrada y divide sus filas en dos archivos de salida diferentes:
uno para las filas donde la columna específica ('type') está vacía y otro para las filas donde esa columna está llena.

Archivos de entrada y salida:
- INPUT_FILE: Ruta del archivo CSV de entrada.
- OUTPUT_EMPTY_TYPE_FILE: Ruta del archivo CSV de salida para las filas con la columna 'type' vacía.
- OUTPUT_FILLED_TYPE_FILE: Ruta del archivo CSV de salida para las filas con la columna 'type' llena.

El script utiliza `pandas` para leer, filtrar y escribir archivos CSV, y `tqdm` para mostrar una barra de progreso durante el procesamiento.

Pasos del script:
1. Leer el archivo CSV de entrada.
2. Filtrar las filas donde la columna 'type' esté vacía o llena.
3. Guardar los resultados en archivos CSV separados.
"""
import pandas as pd
from tqdm import tqdm

# Archivos de entrada y salida
INPUT_FILE = '../data/input/PopularPlacesFull.csv'
OUTPUT_EMPTY_TYPE_FILE = '../data/filtered/PopularPlaces_EmptyType.csv'
OUTPUT_FILLED_TYPE_FILE = '../data/filtered/PopularPlaces_FilledType.csv'

# Lee el archivo CSV de entrada con pandas
df = pd.read_csv(INPUT_FILE)

# Muestra una barra de progreso usando tqdm
tqdm.pandas(desc="Procesando filas")

# Filtrar filas donde la columna 'type' está vacía y las que no lo están
df_empty_type = df[df['type'].progress_apply(lambda x: pd.isna(x) or str(x).strip() == '')]
df_filled_type = df[df['type'].progress_apply(lambda x: not (pd.isna(x) or str(x).strip() == ''))]

# Guarda los resultados en archivos CSV separados
df_empty_type.to_csv(OUTPUT_EMPTY_TYPE_FILE, index=False, encoding='utf-8')
df_filled_type.to_csv(OUTPUT_FILLED_TYPE_FILE, index=False, encoding='utf-8')

print("Separación completada. Las filas se guardaron en los archivos correspondientes.")

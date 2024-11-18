"""
Este script procesa un archivo JSON con información de lugares cercanos, aplica filtros, eliminando duplicados y elementos redundantes,
basados en coordenadas y nombres, y guarda los resultados en archivos CSV. Utiliza las librerías `geopandas`, `pandas`, `numpy`, y
`Levenshtein` para manejar datos geoespaciales y calcular similitudes entre nombres. Los pasos principales son:

1. Configuración de archivos y constantes:
   - Define rutas de entrada y salida para los archivos.
   - Especifica un encabezado para el archivo CSV de salida y define tipos adicionales que serán filtrados.

2. Inicialización de datos:
   - Inicializa diccionarios y listas para almacenar la información de los lugares y los elementos filtrados.

3. Funciones principales:
   - `save_place_info(df, idx)`: Guarda información de un lugar en la lista de elementos filtrados.
   - `load_file()`: Lee el archivo JSON de entrada, extrae información relevante y la guarda en el diccionario `data`.
Filtra tipos de lugares según la lista `ADDITIONAL_TYPES` y redondea las coordenadas.
   - `save_file(df)`: Guarda un `DataFrame` como archivo CSV.
   - `save_filtered_out_file()`: Guarda los elementos filtrados en un archivo CSV separado.
   - `delete_items(df, indexes)`: Elimina elementos de un `DataFrame` según los índices especificados.
   - `filter_coord(df)`: Filtra lugares que tienen coordenadas repetidas y con pocas calificaciones, eliminando duplicados y
registrándolos en la lista de elementos filtrados.
   - `filter_close_by(df)`: Filtra lugares cercanos entre sí basándose en la distancia (usando la fórmula de distancia Haversine) y
en la similitud de nombres (utilizando la biblioteca `Levenshtein`). Elimina duplicados en función del tipo y las calificaciones.

4. Ejecución del script:
   - Carga los datos desde el archivo de entrada.
   - Aplica filtros de coordenadas y cercanía a los datos cargados.
   - Guarda los datos procesados en el archivo CSV de salida y los elementos filtrados en un archivo separado.
   - Imprime el total de lugares procesados y el número de lugares guardados después del filtrado.
"""


import json
import Levenshtein
import numpy as np
import pandas as pd
from tqdm import tqdm

# Archivos de entrada y salida
INPUT_FILE = '../../2_API_busqueda/nearby-places.txt'
OUTPUT_FILE = '../data/input/PopularPlacesFull.csv'
FO_OUTPUT_FILE = '../data/input/PopularPlacesFull-FO.csv'

CSV_HEADER = ['Name', 'type', 'ratings', 'latitude', 'longitude', 'place_id']

# Constantes
ADDITIONAL_TYPES = [
    'store', 'administrative_area_level_1', 'administrative_area_level_2', 'administrative_area_level_3',
    'administrative_area_level_4', 'administrative_area_level_5', 'archipelago', 'colloquial_area',
    'continent', 'country', 'establishment', 'finance', 'floor', 'food', 'general_contractor',
    'geocode', 'health', 'intersection', 'locality', 'natural_feature', 'neighborhood',
    'place_of_worship', 'point_of_interest', 'political', 'post_box', 'postal_code',
    'postal_code_prefix', 'postal_code_suffix', 'postal_town', 'premise', 'room', 'route',
    'street_address', 'street_number', 'sublocality', 'sublocality_level_1', 'sublocality_level_2',
    'sublocality_level_3', 'sublocality_level_4', 'sublocality_level_5', 'subpremise', 'town_square'
]
MAX_FACTOR = 10.0 ** 7

# Inicialización de listas con numpy y pandas
data = {
    'id': [], 'name': [], 'type': [], 'ratings': [],
    'latitude': [], 'longitude': [], 'coords': []
}
filtered_out = []

def save_place_info(df, idx):
    filtered_out.append(df.iloc[idx].tolist())

def load_file():
    with open(INPUT_FILE, encoding='utf-8') as f:
        results = json.load(f)

    for result in tqdm(results, desc="Cargando datos"):
        if 'business_status' not in result:
            continue

        id_ = result['place_id']
        name = result['name']
        tags = [x for x in result['types'] if x not in ADDITIONAL_TYPES]
        typep = f'{tags[0]}+{tags[1]}' if len(tags) > 1 else (tags[0] if tags else '')

        rating = result.get('user_ratings_total', 0)
        lat = np.round(result['geometry']['location']['lat'], 7)
        lng = np.round(result['geometry']['location']['lng'], 7)
        coord = f'{lat},{lng}'

        data['id'].append(id_)
        data['name'].append(name.replace(",", ";"))
        data['type'].append(typep)
        data['ratings'].append(rating)
        data['latitude'].append(lat)
        data['longitude'].append(lng)
        data['coords'].append(coord)

def save_file(df):
    df.to_csv(OUTPUT_FILE, index=False, header=CSV_HEADER, encoding='utf-8')

def save_filtered_out_file():
    pd.DataFrame(filtered_out, columns=CSV_HEADER).to_csv(FO_OUTPUT_FILE, index=False, encoding='utf-8')

def delete_items(df, indexes):
    return df.drop(indexes, inplace=False)

def filter_coord(df):
    print('Filtrando por sobreposición:', len(df), end='')

    coord_counts = df['coords'].value_counts()
    duplicate_coords = coord_counts[coord_counts > 2].index.tolist()

    rep = df[df['coords'].isin(duplicate_coords) & ((df['type'] == '') | (df['ratings'] < 3))].index

    filtered_out.append(['# COORD REPETIDA'])
    [save_place_info(df, i) for i in rep]

    df = delete_items(df, rep)
    print(' >', len(df))
    return df

def filter_close_by(df):
    def get_km_distance(lat_1, lng_1, lat_2, lng_2):
        d_lat = np.radians(lat_2 - lat_1)
        d_lng = np.radians(lng_2 - lng_1)
        temp = (
            np.sin(d_lat / 2) ** 2
            + np.cos(lat_1)
            * np.cos(lat_2)
            * np.sin(d_lng / 2) ** 2
        )
        return 6373.0 * (2 * np.arctan2(np.sqrt(temp), np.sqrt(1 - temp)))

    print('Filtrando por cercanía y nombre similar:', len(df), end='')

    del_indexes = []
    for i in tqdm(range(len(df) - 1), desc="Filtrando cercanos"):
        if i in del_indexes:
            continue
        name_i = df.iloc[i]['name']
        lat_i, lng_i = df.iloc[i]['latitude'], df.iloc[i]['longitude']

        for j in range(i + 1, len(df)):
            if j in del_indexes:
                continue
            name_j = df.iloc[j]['name']
            lat_j, lng_j = df.iloc[j]['latitude'], df.iloc[j]['longitude']

            distance_kms = get_km_distance(lat_i, lng_i, lat_j, lng_j)
            if distance_kms < 0.1:
                sim_ratio = Levenshtein.ratio(name_i, name_j)
                if sim_ratio >= 0.7 or (sim_ratio >= 0.5 and distance_kms < 0.025):
                    if df.iloc[i]['type'] and not df.iloc[j]['type']:
                        del_indexes.append(j)
                    elif not df.iloc[i]['type'] and df.iloc[j]['type']:
                        del_indexes.append(i)
                        break
                    elif df.iloc[i]['ratings'] > df.iloc[j]['ratings']:
                        del_indexes.append(j)
                    elif df.iloc[i]['ratings'] < df.iloc[j]['ratings']:
                        del_indexes.append(i)
                        break

    filtered_out.append(['# POSIBLES REPETIDOS'])
    [save_place_info(df, i) for i in del_indexes]

    df = delete_items(df, del_indexes)
    print(' >', len(df))
    return df

load_file()
df = pd.DataFrame(data)

full_count = len(df)
df = filter_coord(df)
df = filter_close_by(df)

save_file(df)
save_filtered_out_file()

print('Total:', full_count)
print('Guardados:', len(df))

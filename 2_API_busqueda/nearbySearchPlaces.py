# -*- coding: utf-8 -*-

"""
Script para buscar los places mas "prominentes" (pura mentira) de Google Places.

Para utilizar, asignar en "INPUT_FILES" la lista de archivos con coordenadas.
En "API_KEY" ponr la key que asigna Google por usuario.

En la version anterior filtraba la busqueda por tipo y en un radio mayor. Pero se obtienen mejores resultados sin filtrar.

La salida es un solo archivo JSON con todos los resultados, menos los repetidos.
"""

import json
import requests
import time
import random
import os
from tqdm import tqdm

URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
API_KEY = 'AIzaSyCAVuwD8l_8babtKEr-E4knyDWMYKrdwYc'
LOCATIONS = []
RADIUSES = []
LANGUAGE = 'es-419'  # Spanish (Latin America)

folder_path = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/1_Regiones'
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

INPUT_FILES = csv_files
OUTPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/2_API_busqueda/nearby-places.txt'
PLACES_ID = set()

def load_coords():
    for i, coor_file in enumerate(INPUT_FILES):
        radious = 0
        with open(coor_file, 'r') as fp:
            for line in fp.readlines():
                splited = line.strip().split(',')
                if not radious:
                    if len(splited) < 3:
                        exit('Falta radio')
                    radious = splited[2]
                if len(splited) > 1:
                    LOCATIONS.append(f'{splited[0]},{splited[1]}')
                    RADIUSES.append(radious)
        print(f"Coordenadas cargadas desde {coor_file}")

def remove_duplicates(results):
    for i in reversed(range(len(results))):
        if results[i]['place_id'] not in PLACES_ID:
            PLACES_ID.add(results[i]['place_id'])
        else:
            del results[i]
    return results

def main():
    load_coords()
    print('Total coordenadas:', len(LOCATIONS))
    total_results_count = 0

    full_data = []
    rnd_indexes = list(range(len(LOCATIONS)))
    random.shuffle(rnd_indexes)

    session = requests.Session()  # Crear una sesión persistente

    try:
        for i in tqdm(rnd_indexes, desc="Procesando ubicaciones", ncols=100):
            if total_results_count > 0:
                time.sleep(1)  # 1 segundo de delay por seguridad

            params = {
                'key': API_KEY,
                'location': LOCATIONS[i],
                'radius': RADIUSES[i],
                'language': LANGUAGE
            }

            try:
                resp = session.get(URL, params=params)
                data = resp.json()
            except requests.RequestException as e:
                print(f"Error de red: {e}")
                continue

            if 'results' not in data:
                continue

            results_count = len(data['results'])
            results = remove_duplicates(data['results'])
            if len(results):
                full_data.extend(results)

            while 'next_page_token' in data:
                time.sleep(2)
                params = {
                    'key': API_KEY,
                    'language': LANGUAGE,
                    'pagetoken': data['next_page_token']
                }
                try:
                    resp = session.get(URL, params=params)
                    data = resp.json()
                except requests.RequestException as e:
                    print(f"Error de red: {e}")
                    break

                results_count += len(data['results'])
                results = remove_duplicates(data['results'])
                if len(results):
                    full_data.extend(results)

            total_results_count += results_count

        print('Total:', total_results_count)
        print('Duplicados:', total_results_count - len(full_data))

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
            json.dump(full_data, out_file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error al procesar las ubicaciones: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()

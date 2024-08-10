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

URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
API_KEY = 'AIzaSyCAVuwD8l_8babtKEr-E4knyDWMYKrdwYc'
LOCATIONS = []
RADIUSES = []
LANGUAGE = 'es-419' # Spanish (Latin America)

# Ruta de la carpeta que contiene los archivos .csv
folder_path = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/Regiones'
# Obtiene una lista de archivos en la carpeta que tienen la extensión .csv
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# Se asigna la lista a la variable INPUT_FILES
INPUT_FILES = csv_files # archivos con coordenadas en grados y radio elipsoidal

OUTPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/API/nearby-places.txt'
PLACES_ID = set() # Para almacenar id de places

def load_coords():
    # Coordenadas tienen que estar en grados
    for i, coor_file in enumerate(INPUT_FILES):
        radious = 0
        with open(coor_file, 'r') as fp:
            for line in fp.readlines():
                splited = line[:-1].split(',')
                if not radious:
                    if len(splited) < 3:
                        exit('Falta radio')
                    radious = splited[2]
                if len(splited) > 1:
                    LOCATIONS.append(f'{splited[0]},{splited[1]}')
                    RADIUSES.append(radious)
        print("load_cords",i)

def remove_duplicates(results):
    for i in reversed(range(len(results))):
        if results[i]['place_id'] not in PLACES_ID:
            PLACES_ID.add(results[i]['place_id'])
        else:
            del results[i]
    return results

load_coords()
print('Total coordenadas:', len(LOCATIONS))
total_results_count = 0

full_data = []
# Randomiza el orden de busqueda
rnd_indexes = list(range(len(LOCATIONS)))
random.shuffle(rnd_indexes)
for i in rnd_indexes:
    if total_results_count > 0:
        time.sleep(1) # 1 segundo de delay por las dudas
    #
    params = dict(
        # Required parameters
        key=API_KEY,            # Your application's API key.
        location=LOCATIONS[i],  # This must be specified as latitude,longitude.
        radius=RADIUSES[i],     # Defines the distance (in meters) within which to return place results.
        # Optional parameters
        language=LANGUAGE       # Language code, indicating in which language the results should be returned.
        #rankby='prominence',    # Note that rankby must not be included if radius is specified.
        #type='establishment'    # Restricts the results to places matching the specified type.
    )
    resp = requests.get(URL, params=params)
    data = resp.json()
    if 'results' not in data:
        continue
    else:
        results_count = len(data['results'])
        results = remove_duplicates(data['results'])
        if len(results):
            full_data.extend(results)
        #
        while 'next_page_token' in data:
            time.sleep(2) # delay necesario
            params = dict(
                key=API_KEY,
                language=LANGUAGE,
                pagetoken=data['next_page_token'] # Setting a pagetoken parameter will execute a search with the same parameters used previously
            )
            resp = requests.get(URL, params=params)
            data = resp.json()
            results_count += len(data['results'])
            results = remove_duplicates(data['results'])
            if len(results):
                full_data.extend(results)
    #
    total_results_count += results_count
    print('Results:', results_count)
print('Total:', total_results_count)
print('Duplicados:', total_results_count - len(full_data))

out_file = open(OUTPUT_FILE, 'w', encoding='utf-8')
json.dump(full_data, out_file, ensure_ascii=False, indent=4)
out_file.close()
full_data.clear()

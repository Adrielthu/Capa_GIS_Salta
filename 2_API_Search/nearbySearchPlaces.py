# -*- coding: utf-8 -*-
"""
Script para buscar los places más "prominentes" de Google Places.
Este script realiza una búsqueda de lugares cercanos utilizando la API de Google Places y guarda los resultados en un archivo JSON.
Para utilizar:
1. Asignar en "INPUT_FILES" la lista de archivos con coordenadas.
2. En "API_KEY" poner la key que asigna Google por usuario.
Variables globales:
- URL: URL de la API de Google Places.
- API_KEY: Clave de API proporcionada por Google.
- LOCATIONS: Lista de coordenadas de ubicación.
- RADIUSES: Lista de radios de búsqueda.
- LANGUAGE: Idioma para los resultados de la API.
- folder_path: Dirección de los archivos CSV del paso 1.
- csv_files: Lista de archivos CSV en la carpeta especificada.
- INPUT_FILES: Lista de archivos de entrada con coordenadas.
- OUTPUT_FILE: Nombre del archivo de salida.
- PLACES_ID: Conjunto de IDs de lugares para eliminar duplicados.
Funciones:
- load_coords(): Carga las coordenadas y radios de los archivos CSV especificados en INPUT_FILES.
- remove_duplicates(results): Elimina los resultados duplicados basados en el ID del lugar.
- main(): Función principal que carga coordenadas, realiza solicitudes de búsqueda cercana y guarda los resultados en un archivo JSON.
Notas:
- La función main() usa un retraso entre solicitudes para evitar alcanzar los límites de tasa.
- La función main() asume la existencia de variables globales como API_KEY, LOCATIONS, RADIUSES, LANGUAGE, URL y OUTPUT_FILE.
Excepciones:
- Exception: Si ocurre algún error durante el procesamiento de las ubicaciones.
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

folder_path = './1_Regiones/Archivos/' # Dirección de los archivos CSV del paso 1
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

INPUT_FILES = csv_files
OUTPUT_FILE = 'nearby-places.txt'
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
    """
    Función principal para cargar coordenadas, realizar solicitudes de búsqueda cercana y guardar los resultados.
    Esta función realiza los siguientes pasos:
    1. Carga coordenadas de una fuente predefinida.
    2. Imprime el número total de coordenadas cargadas.
    3. Inicializa un contador de resultados totales y una lista vacía para almacenar todos los datos.
    4. Mezcla la lista de índices de ubicaciones para un procesamiento aleatorio.
    5. Crea una sesión persistente para realizar solicitudes HTTP.
    6. Itera sobre los índices de ubicaciones mezclados y realiza lo siguiente:
        - Realiza una solicitud a la API de búsqueda cercana con los parámetros dados.
        - Maneja los errores de red de manera adecuada.
        - Procesa los resultados, elimina duplicados y los añade a la lista de datos completos.
        - Maneja la paginación realizando solicitudes adicionales si hay un token de página siguiente presente.
    7. Imprime el número total de resultados y el número de duplicados encontrados.
    8. Guarda todos los datos en un archivo de salida en formato JSON.
    9. Cierra la sesión y maneja cualquier excepción que ocurra durante el procesamiento.
    Nota:
        - La función usa un retraso entre solicitudes para evitar alcanzar los límites de tasa.
        - La función asume la existencia de variables globales como API_KEY, LOCATIONS, RADIUSES, LANGUAGE, URL y OUTPUT_FILE.
    Lanza:
        Exception: Si ocurre algún error durante el procesamiento de las ubicaciones.
    """
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

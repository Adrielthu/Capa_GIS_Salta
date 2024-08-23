import requests
import time
import Levenshtein
from tqdm import tqdm
import csv

# Definición del encabezado del CSV de salida
CSV_HEADER = ['Name', 'type', 'ratings', 'latitude', 'longitude', 'place_id']

# Archivos de entrada y salida
INPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/3_filtro_por_cercania/PopularPlaces_EmptyType.csv'
OUTPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/PopularPlacesFull-.csv'

# Parámetros de configuración
MIN_RATINGS = 0  # Mínimo número de reseñas requerido para procesar un lugar
MATCH_GMB_CATEGORIES = True  # Si se debe intentar emparejar categorías de Google My Business (GMB)

# URL base para búsquedas en Google Maps
URL_GMAPS = 'https://www.google.com/maps/search/'

# Diccionarios para almacenar tipos y categorías encontradas
types_found = {}
gcid = []
category = []

def get_google_maps_type(session, place_id, place_name, first_search=False):
    """
    Obtiene el tipo de lugar desde Google Maps usando el place_id y place_name.

    :param session: Sesión de requests persistente.
    :param place_id: ID del lugar en Google Places.
    :param place_name: Nombre del lugar.
    :param first_search: Indica si es la primera búsqueda (sin retraso).
    :return: El tipo de lugar encontrado o una cadena de error.
    """
    try:
        if not first_search:
            time.sleep(30)  # Espera 30 segundos entre consultas para evitar bloqueos.

        params = dict(
            api=1,
            query=place_name,
            query_place_id=place_id,
            hl='en'
        )
        resp = session.get(URL_GMAPS, params=params)
        if 'sorry' in resp.url:
            print('Error Google')
            return 'sorry'

        # Procesa la respuesta HTML para extraer el tipo de lugar
        html_text = resp.text
        find_end = html_text.find('itemprop="description">')
        find_start = html_text.rfind('<meta content=', 0, find_end)

        description = html_text[find_start + len('<meta content=') + 1:find_end - 2]
        items_text = description.split('·')

        if len(items_text) == 2:
            return items_text[1].strip()  # Devuelve el tipo de lugar si es encontrado.
        elif len(items_text) > 2:
            return items_text[2].strip()
        return ''

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return 'error'

def load_gmb_categories():
    """
    Carga las categorías de Google My Business (GMB) desde un archivo de texto.

    :return: None
    """
    try:
        with open('C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/gmb_categories_us.txt') as fp:
            fp.readline()  # Ignora la primera línea del archivo (encabezado).
            for line in fp.readlines():
                splited = line[:-1].split('\t')
                gcid.append(splited[0])
                category.append(splited[1])
    except Exception as e:
        print(f"Error loading GMB categories: {e}")

def main():
    """
    Función principal que procesa el archivo de lugares, consulta Google Maps para obtener los tipos de lugares,
    y guarda los resultados en un archivo CSV.

    :return: None
    """
    first_search = True
    skip_lines = 0

    # Comprueba si el archivo de salida ya existe para evitar reescribir datos
    try:
        with open(OUTPUT_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            skip_lines = sum(1 for _ in reader)
    except FileNotFoundError:
        pass

    with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        if skip_lines == 0:
            writer.writerow(CSV_HEADER)  # Escribe el encabezado si el archivo es nuevo
        else:
            print(f"Saltear {skip_lines} lineas")
            skip_lines -= 1

        if MATCH_GMB_CATEGORIES:
            load_gmb_categories()  # Carga las categorías de Google My Business

        request_session = requests.Session()
        request_session.headers.update({'Accept-Language': 'en-US'})  # Configura el idioma de la sesión

        try:
            with open(INPUT_FILE, encoding='utf-8') as in_file:
                reader = csv.reader(in_file)
                next(reader)  # Salta la primera línea (encabezado)

                # Convertir reader a lista para tqdm
                rows = list(reader)
                for row in tqdm(rows, desc="Procesando lugares"):
                    if skip_lines > 0:
                        skip_lines -= 1
                        continue

                    if len(row) < 6 or int(row[2]) < MIN_RATINGS:
                        continue

                    place_type = row[1]
                    if not place_type:  # Si no se tiene tipo de lugar, se busca en Google Maps
                        place_id = row[5]
                        place_name = row[0]
                        place_type = get_google_maps_type(request_session, place_id, place_name, first_search)
                        first_search = False

                        if not place_type:
                            continue
                        elif place_type == 'sorry' or place_type == 'error':
                            break
                        elif MATCH_GMB_CATEGORIES:  # Empareja categorías con Google My Business si es necesario
                            _ = types_found.get(place_type)
                            if _ is None:
                                type_found = False
                                for i in range(len(category)):
                                    if Levenshtein.ratio(place_type, category[i]) >= 0.9:
                                        type_found = True
                                        types_found[place_type] = gcid[i]
                                        place_type = gcid[i]
                                        del category[i]
                                        del gcid[i]
                                        break
                                if not type_found:
                                    place_type += '***'
                            else:
                                place_type = _

                        writer.writerow([place_name, place_type, row[2], row[3], row[4], place_id])
                    else:
                        writer.writerow(row)
        except Exception as e:
            print(f"Error processing input file: {e}")

if __name__ == "__main__":
    main()
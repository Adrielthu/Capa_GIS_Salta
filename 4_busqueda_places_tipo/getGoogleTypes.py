import requests
import time
import Levenshtein
from bs4 import BeautifulSoup

CSV_HEADER = 'Name,type,ratings,latitude,longitude,place_id\n'  # Header que le gusta a Google Maps

# Archivos de entrada y salida
INPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/PopularPlaces/PopularPlaces_EmptyType_part_01.csv'
OUTPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/PopularPlacesFull---.csv'

MIN_RATINGS = 0  # Cantidad mínima de valoraciones necesarias
MATCH_GMB_CATEGORIES = True  # Si busca el type de category retornada (ahorra CPU en False)

URL_GMAPS = 'https://www.google.com/maps/search/'

types_found = {}
gcid = []
category = []

def get_google_maps_type(session, place_id, place_name, first_search=False):
    if not first_search:
        time.sleep(30)  # 30 segundos mínimo entre consultas
    params = dict(
        api=1,
        query=place_name,
        query_place_id=place_id,
        hl='en'  # Puedes probar con 'es' para ver si hay alguna diferencia
    )
    response = session.get(URL_GMAPS, params=params, timeout=10)
    print(f"Realizando búsqueda en: {response.url}")

    html_text = response.text

    # Imprimir los primeros 2000 caracteres del HTML para depuración
    print(f"HTML de respuesta:\n{html_text[:2000]}")

    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(html_text, 'html.parser')

    # Intentar encontrar la descripción en el meta tag
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        description = meta_description.get('content', '')
        print(f"Descripción encontrada: {description}")
        items_text = description.split('·')
        if len(items_text) >= 2:
            return items_text[1].strip()
        elif len(items_text) > 2:
            return items_text[2].strip()
    else:
        print("No se encontró la descripción en la respuesta HTML.")
        return ''

def load_gmb_categories():
    with open('C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/gmb_categories_us.txt') as fp:
        fp.readline()  # header
        for line in fp.readlines():
            splited = line[:-1].split('\t')  # borrar /n
            gcid.append(splited[0])
            category.append(splited[1])

first_search = True
skip_lines = 0
try:
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        skip_lines = sum(1 for _ in f)
except FileNotFoundError:
    pass

out_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
if skip_lines == 0:
    out_file.write(CSV_HEADER)  # escribe header
else:
    print(f"El archivo de salida ya tiene {skip_lines} líneas.")
    skip_lines -= 1

if MATCH_GMB_CATEGORIES:
    load_gmb_categories()
    print(f"Cargadas {len(gcid)} categorías de GMB.")

# Guardar datos básicos y en el formato CSV para luego importar en Google Maps
request_session = requests.Session()
request_session.headers.update({'Accept-Language': 'en-US'})

in_file = open(INPUT_FILE, encoding='utf-8')
in_file.readline()  # header
for line in in_file.readlines():
    if skip_lines > 0:
        skip_lines -= 1
        continue

    splited = line[:-1].split(',')  # borrar /n
    if len(splited) < 6 or int(splited[2]) < MIN_RATINGS:  # ratings
        continue

    place_type = splited[1]  # type
    if not place_type:
        idp = splited[5]
        name = splited[0]  # no hace falta pasar comas a punto y coma
        place_type = get_google_maps_type(request_session, idp, name, first_search)
        first_search = False

        if not place_type:
            print(f"No se pudo obtener el tipo para el lugar '{name}'. Saltando.")
            continue
        if place_type == 'sorry':
            print("Google ha detectado un bot. Terminando ejecución.")
            break

        if MATCH_GMB_CATEGORIES:
            if place_type in types_found:
                place_type = types_found[place_type]
            else:
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
                    place_type += '***'  # marcar como desconocido para revisión futura

        out_file.write(f'{name},{place_type},{splited[2]},{splited[3]},{splited[4]},{idp}\n')
        out_file.flush()  # Por si muere el script, o correr con -u
    else:
        out_file.write(line)

out_file.close()
in_file.close()

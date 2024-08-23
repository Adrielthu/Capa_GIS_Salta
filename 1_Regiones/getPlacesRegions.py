# -*- coding: utf-8 -*-
import os
import math
import random
import shapefile
from shapely.geometry import Point, Polygon, MultiPolygon

INPUT_SHP_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/1_Regiones/places_regions.shp'
output_folder = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/1_Regiones'

METER_OFFSET_X = 0
METER_OFFSET_Y = 0

def create_region_shp():
    w = shapefile.Writer(INPUT_SHP_FILE, shapeType=5, encoding='utf8') # POLYGON
    w.field('id', 'N', size=8)  # id - 8 dígitos
    w.field('dist', 'N', size=4)  # distancia en metros
    w.close()

def degrees_to_meters(lat, lon):
    x = (lon * 20037508.34) / 180
    y = math.log(math.tan(((90 + lat) * math.pi) / 360)) / (math.pi / 180)
    y = (y * 20037508.34) / 180
    return x, y

def process_polygon(poly, distance, index):
    """
    Función para procesar un solo polígono y guardar la información en un archivo CSV.
    El índice (index) se usa para diferenciar archivos.
    """
    if not distance:
        print("Falta atributo dist!")
        return

    out_file_path = os.path.join(output_folder, f'{distance}_{index}.csv')
    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        # Calcular offsets para X e Y
        global METER_OFFSET_X, METER_OFFSET_Y
        if METER_OFFSET_X == 0:
            _ = degrees_to_meters(poly.bounds[1], poly.bounds[0])
            lon_mts = (_[0] / poly.bounds[0])  # metros lon
            METER_OFFSET_X = 1 / lon_mts
            METER_OFFSET_Y = METER_OFFSET_X

        offset_x = METER_OFFSET_X * distance
        offset_y = METER_OFFSET_Y * distance
        first_line = True
        valid = False
        start_x = poly.bounds[0]

        while start_x < poly.bounds[2]:
            valid = not valid
            start_y = poly.bounds[1]
            if valid:
                start_y -= offset_y / 2
            while start_y < poly.bounds[3]:
                point = Point(start_x, start_y)
                if poly.contains(point):
                    rnd_offset = random.randint(0, 9) * (10 ** -8)
                    output_y = start_y + rnd_offset
                    output_x = start_x + rnd_offset
                    if first_line:
                        out_file.write(f'{output_y:.8f},{output_x:.8f},{distance * 0.535}\n')
                        first_line = False
                    else:
                        out_file.write(f'{output_y:.8f},{output_x:.8f}\n')
                start_y += offset_y
            start_x += offset_x

    print(f'Nuevo archivo: {out_file_path}')

if not os.path.exists(INPUT_SHP_FILE):
    create_region_shp()
    exit("Nuevo shp creado")

polygon_file = shapefile.Reader(INPUT_SHP_FILE, encoding='utf8')

for polygon in polygon_file.shapeRecords():
    coords = polygon.shape.__geo_interface__['coordinates']
    distance = polygon.record['dist']

    # Procesar múltiples polígonos separados (MultiPolygon)
    if isinstance(coords[0], (list, tuple)) and isinstance(coords[0][0], (list, tuple)) and isinstance(coords[0][0][0], (list, tuple)):
        polygons = [Polygon(poly_coords[0]) for poly_coords in coords]
        for i, poly in enumerate(polygons):
            process_polygon(poly, distance, i)

    # Procesar un único polígono (con o sin agujeros)
    elif isinstance(coords[0], (list, tuple)) and isinstance(coords[0][0], (list, tuple)):
        exterior = coords[0]  # El primer anillo es el exterior
        interiors = coords[1:]  # Los anillos restantes son agujeros (si existen)
        poly = Polygon(exterior, interiors)
        process_polygon(poly, distance, 0)

    # Procesar un polígono simple (sin agujeros)
    else:
        poly = Polygon(coords)
        process_polygon(poly, distance, 0)

polygon_file.close()
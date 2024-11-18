# -*- coding: utf-8 -*-
"""
Este script procesa archivos shapefile que contienen regiones poligonales y genera archivos CSV con puntos dentro de estos polígonos.
Módulos:
    os: Proporciona una forma de usar funcionalidades dependientes del sistema operativo.
    math: Proporciona acceso a funciones matemáticas.
    random: Implementa generadores de números pseudoaleatorios para varias distribuciones.
    shapefile: Proporciona soporte de lectura y escritura para archivos Shapefile de ESRI.
    shapely.geometry: Proporciona objetos geométricos y operaciones.
Constantes:
    INPUT_SHP_FILE (str): Ruta al archivo shapefile de entrada que contiene regiones poligonales.
    output_folder (str): Directorio donde se guardarán los archivos CSV de salida.
    METER_OFFSET_X (int): Desplazamiento en metros para la coordenada X.
    METER_OFFSET_Y (int): Desplazamiento en metros para la coordenada Y.
Funciones:
    create_region_shp():
        Crea un nuevo archivo shapefile con los campos 'id' y 'dist' si el archivo shapefile de entrada no existe.
    degrees_to_meters(lat, lon):
        Convierte latitud y longitud a metros usando la proyección de Mercator.
    process_polygon(poly, distance, index):
        Procesa un solo polígono, generando puntos dentro de él y guardándolos en un archivo CSV.
        Args:
            poly (Polygon): El polígono a procesar.
            distance (float): El atributo de distancia del archivo shapefile.
            index (int): Índice para diferenciar archivos de salida.
Ejecución Principal:
    Verifica si el archivo shapefile de entrada existe. Si no, crea un nuevo archivo shapefile y sale.
    Lee el archivo shapefile de entrada y procesa cada polígono, generando archivos CSV con puntos dentro de los polígonos.
"""

import os
import math
import random
import shapefile
from shapely.geometry import Point, Polygon, MultiPolygon

INPUT_SHP_FILE = 'Places_Regions/places_regions.shp'
output_folder = 'data/'

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
    Parámetros:
    poly (Polygon): El polígono a procesar.
    distance (float): La distancia utilizada para calcular los desplazamientos.
    index (int): El índice utilizado para diferenciar los archivos de salida.
    Retorna:
    None
    Esta función procesa un polígono dado calculando desplazamientos y generando puntos dentro del polígono.
    Los puntos se guardan en un archivo CSV nombrado en base a la distancia proporcionada y el índice.
    Si no se proporciona el parámetro de distancia, la función imprimirá un mensaje de error y retornará.
    La función calcula desplazamientos en metros para las coordenadas X e Y basándose en los límites del polígono.
    Luego itera a través de los límites del polígono, generando puntos y escribiéndolos en el archivo CSV.
    Las coordenadas de cada punto se aleatorizan ligeramente para evitar duplicados exactos.
    La primera línea del archivo CSV incluye un valor adicional calculado a partir de la distancia.
    Las líneas subsiguientes contienen solo las coordenadas de los puntos.
    La función imprime la ruta del archivo CSV recién creado al finalizar.
    """
    if not distance:
        print("Falta atributo dist!")
        return

    out_file_path = os.path.join(output_folder, f'{distance}_{index}.csv')
    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        # Calcular offsets para X e Y
        # Si METER_OFFSET_X no ha sido calculado, convertir lat/lon a metros
        global METER_OFFSET_X, METER_OFFSET_Y
        if METER_OFFSET_X == 0:
            _ = degrees_to_meters(poly.bounds[1], poly.bounds[0])
            lon_mts = (_[0] / poly.bounds[0])  # Conversión de longitud a metros
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
                    rnd_offset = random.randint(0, 9) * (10 ** -8) # Aleatorización de coordenadas para evitar duplicados exactos
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

# Si es un MultiPolygon, procesar cada subpolígono por separado.
# Un MultiPolygon está compuesto por múltiples polígonos independientes,
# por lo que se debe iterar sobre cada uno de ellos para generar puntos.
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
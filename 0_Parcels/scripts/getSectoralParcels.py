"""
Script para la generación de puntos que representan casas dentro de polígonos censales.

Este script toma como entrada un archivo shapefile que contiene polígonos correspondientes a sectores censales
y genera puntos (casas) dentro de cada uno de esos polígonos. La cantidad de puntos generados se basa en
la información de densidad de viviendas (campo 'IND01') proporcionada por el archivo de entrada. Los puntos
se distribuyen en forma de cuadrícula, considerando un margen interno para evitar que los puntos caigan
en los bordes del polígono.

El script sigue los siguientes pasos:

1. Carga de archivos: Verifica la existencia del archivo shapefile de entrada y lo carga utilizando GeoPandas.
2. Reproyección de coordenadas: Transforma las coordenadas del sistema original al sistema UTM (EPSG:32719)
   para calcular áreas en metros cuadrados y luego las vuelve a reproyectar a coordenadas geográficas (EPSG:4326).
3. Cálculo de área: Calcula el área en metros cuadrados para cada polígono y la guarda en una nueva columna ('aream2').
4. Generación de puntos: Itera sobre cada polígono para generar puntos según la densidad de viviendas especificada.
   Los puntos se distribuyen en una cuadrícula dentro de un polígono reducido (con un buffer negativo) para crear
   un margen interno.
5. Validación de geometría: Verifica que el polígono reducido sea válido y tenga un área positiva antes de generar puntos.
6. Manejo de errores: En caso de que algún polígono contenga datos inválidos (como áreas o cantidades de casas negativas
   o nulas), el script captura estas excepciones y las reporta sin detener la ejecución.
7. Exportación de resultados: Los puntos generados se guardan en un nuevo archivo shapefile en la ruta especificada.

Parameters:
-----------
- INPUT_SHP_FILE : str
    Ruta relativa al archivo shapefile que contiene los polígonos de entrada.
- OUTPUT_SHP_FILE : str
    Ruta relativa donde se guardará el archivo shapefile con los puntos generados.


Salida:
-------
El script genera un archivo shapefile en la ubicación especificada, que contiene los puntos generados con los atributos:
- `geometry`: La ubicación de cada punto en coordenadas geográficas.
- `id`: Un identificador único para cada punto.
- `area`: El índice del sector censal al que pertenece el punto.
- `NBI`: El nivel de necesidades básicas insatisfechas (NBI) asociado al sector censal.

Notas:
------
- El cálculo del área de cada punto se basa en el total de casas por polígono y el área del polígono para asegurar
  una distribución proporcional.
- El margen aplicado a los polígonos reduce el área en los bordes para evitar errores en la ubicación de las casas.
"""

import os
import geopandas as gpd
from shapely.geometry import Point, Polygon
import random
import math
from tqdm import tqdm  # Barra de progreso

# Ruta del archivo de entrada SHP
INPUT_SHP_FILE = '../data/neighborhood/Radiosprecensales2021(octubre).shp'
# Ruta del archivo de salida SHP
OUTPUT_SHP_FILE = '../data/houses/Houses.shp'

# Verifica si el archivo de entrada existe
if not os.path.exists(INPUT_SHP_FILE):
    exit("El archivo de entrada no existe")

# Lee el archivo de polígonos con geopandas
gdf_poligonos = gpd.read_file(INPUT_SHP_FILE)

# Reproyecta el GeoDataFrame a UTM zona 19S (EPSG:32719)
gdf_poligonos = gdf_poligonos.to_crs(epsg=32719)

# Calcula el área en metros cuadrados y lo guarda en una nueva columna
gdf_poligonos['aream2'] = gdf_poligonos.geometry.area  # Área en m²

gdf_poligonos = gdf_poligonos.to_crs(epsg=4326)

# Crea una lista para almacenar los puntos generados
puntos_generados = []
casas_totales = 0
# Parámetro de margen
MARGEN = 5
id = 1

# Itera sobre cada polígono en el archivo de entrada
for idx, row in gdf_poligonos.iterrows():
    try:
        # Acceso directo a los campos
        area_m2 = row['aream2']  # Área en metros cuadrados
        max_houses = row['IND01']  # Número máximo de casas a generar

        if max_houses > 0 and area_m2 > 0:
            area_por_punto = area_m2 / max_houses  # Área asignada a cada punto
            lado_cuadrado = math.sqrt(area_por_punto)  # Lado del cuadrado que representa el área
            OFFSET_X = lado_cuadrado / 111000  # Convierte el lado a grados
            OFFSET_Y = lado_cuadrado / 111000  # Convierte el lado a grados
        else:
            raise ValueError("Datos inválidos en el polígono.")

        # Crear el polígono de Shapely y aplicar el buffer negativo (para crear el margen)
        poly = row.geometry
        poly_reducido = poly.buffer(-MARGEN / 111000)  # Aplica el buffer negativo (ajustado a grados)

        # Verifica si el polígono reducido es válido y tiene un área positiva
        if poly_reducido.is_valid and not poly_reducido.is_empty and poly_reducido.area > 0:
            sectoral_index = row['sectoral']
            NBI_sectoral = row['NBI']
            first_x = poly_reducido.bounds[0]
            start_y = poly_reducido.bounds[1]
            sw_offsets = False
            houses = 0
            with tqdm(total=max_houses, desc=f"Generando casas del sector {sectoral_index}") as pbar:
                while houses < max_houses:
                    while start_y < poly_reducido.bounds[3]:
                        start_x = first_x
                        while start_x < poly_reducido.bounds[2]:
                            point = Point(start_x, start_y)
                            if poly_reducido.contains(point):
                                puntos_generados.append([point, id, sectoral_index, NBI_sectoral])
                                id += 1
                                houses += 1
                                casas_totales +=1
                                pbar.update(1)  # Actualiza la barra de progreso
                                if houses == max_houses:
                                    start_y = poly_reducido.bounds[3]
                                    break
                            start_x += OFFSET_X
                        start_y += OFFSET_Y
                    start_y = poly_reducido.bounds[1]
                    if not sw_offsets:
                        start_y += OFFSET_Y / 2
                        sw_offsets = True
                    else:
                        first_x += OFFSET_X / 2
                        sw_offsets = False
            print(f"Generadas {houses} de {max_houses} casas del sector {sectoral_index}")
        else:
            print(f"El polígono del sector {row['sectoral']} no es válido después del buffer.")
    except (ValueError, TypeError, AttributeError, KeyError) as e:
        print(f"Error en el polígono con sectoral {row['sectoral']}: {e}")
        continue

# Crear un GeoDataFrame con los puntos generados
gdf_puntos = gpd.GeoDataFrame(
    puntos_generados,
    columns=['geometry', 'id', 'area', 'NBI'],
    crs=gdf_poligonos.crs  # Mantiene el sistema de coordenadas original
)

# Guardar los puntos en un nuevo shapefile
gdf_puntos.to_file(OUTPUT_SHP_FILE)

print(f"Puntos guardados en {OUTPUT_SHP_FILE}")
print("casas totales: ", casas_totales)
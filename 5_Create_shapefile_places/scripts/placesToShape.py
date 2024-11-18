"""
Este script lee un archivo CSV que contiene información sobre lugares populares, filtra las columnas necesarias,
y convierte las coordenadas de latitud y longitud en una geometría de puntos para crear un GeoDataFrame.
Luego, guarda el GeoDataFrame resultante en un archivo shapefile (SHP) para uso en sistemas de información geográfica (GIS).

Variables:
    - CSV_INPUT_FILE (str): ruta del archivo CSV de entrada que contiene la información de los lugares.
    - SHP_OUTPUT_FILE (str): nombre base del archivo SHP de salida que se generará.

Pasos del script:
1. Lee el archivo CSV con pandas y almacena los datos en un DataFrame.
2. Filtra las columnas necesarias: 'Name', 'type', 'ratings', 'latitude', y 'longitude'.
3. Crea una columna de geometría utilizando las coordenadas de latitud y longitud de cada lugar para formar puntos.
4. Elimina las columnas de latitud y longitud originales del DataFrame.
5. Convierte el DataFrame filtrado en un GeoDataFrame utilizando GeoPandas, especificando el sistema de coordenadas CRS 'EPSG:4326'.
6. Guarda el GeoDataFrame como un archivo shapefile (SHP) en la ubicación y con el nombre especificados.
7. Imprime un mensaje confirmando que el archivo SHP se generó correctamente.

"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

CSV_INPUT_FILE = '../../4_filtrar_por_tipo/UpdatedPopularPlaces.csv'
SHP_OUTPUT_FILE = '../places/places.shp'
try:
   # Lee el CSV usando pandas
    df = pd.read_csv(CSV_INPUT_FILE)
except Exception as e:
    print(f"Error al leer los archivos: {e}")
    exit(1)

# Filtra columnas necesarias
df_filtered = df[['Name', 'type', 'ratings', 'latitude', 'longitude']]

# Crea una columna de geometría a partir de las coordenadas de latitud y longitud
geometry = [Point(xy) for xy in zip(df_filtered['longitude'], df_filtered['latitude'])]
df_filtered = df_filtered.drop(['latitude', 'longitude'], axis=1)
gdf = gpd.GeoDataFrame(df_filtered, geometry=geometry, crs='EPSG:4326')

# Guarda el GeoDataFrame en un archivo SHP
gdf.to_file(SHP_OUTPUT_FILE, driver='ESRI Shapefile')
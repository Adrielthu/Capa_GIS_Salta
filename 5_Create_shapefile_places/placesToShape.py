# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

CSV_INPUT_FILE = '../4_filtrar_por_tipo/UpdatedPopularPlaces.csv'
SHP_OUTPUT_FILE = 'places'

# Lee el CSV usando pandas
df = pd.read_csv(CSV_INPUT_FILE)


# Filtra columnas necesarias
df_filtered = df[['Name', 'type', 'ratings', 'latitude', 'longitude']]

# Crea una columna de geometría a partir de las coordenadas de latitud y longitud
geometry = [Point(xy) for xy in zip(df_filtered['longitude'], df_filtered['latitude'])]
df_filtered = df_filtered.drop(['latitude', 'longitude'], axis=1)
gdf = gpd.GeoDataFrame(df_filtered, geometry=geometry, crs='EPSG:4326')

# Guarda el GeoDataFrame en un archivo SHP
gdf.to_file(SHP_OUTPUT_FILE, driver='ESRI Shapefile')

print(f"Archivo SHP '{SHP_OUTPUT_FILE}.shp' generado correctamente.")

"""
Este script lee archivos shapefile que contienen información sobre lugares y áreas con NBI (Necesidades Básicas Insatisfechas),
realiza una unión espacial para asignar atributos de NBI a los lugares y guarda el resultado en un nuevo archivo shapefile.

Pasos del script:
1. Intenta leer dos archivos shapefile usando GeoPandas:
   - `NBI`: Contiene las geometrías y clasificaciones NBI de áreas específicas.
   - `places`: Contiene las geometrías de lugares.
   Si ocurre un error al leer los archivos, se imprime un mensaje de error y el script finaliza.

2. Asegura que ambos GeoDataFrames tengan el mismo sistema de coordenadas (CRS) especificando 'EPSG:4326'.

3. Realiza una unión espacial ('spatial join') para asociar a cada lugar del GeoDataFrame `places` el valor de 'NBI_clas'
   de las áreas de `NBI` en las que se encuentran. La unión se realiza con el método 'within', que verifica si un lugar
   está dentro de un área NBI.

4. Asigna un valor por defecto (`default_value = 2`) a la columna 'NBI_clas' para los lugares que no se encuentran dentro de las áreas NBI.

5. Elimina la columna 'index_right' generada por la operación de unión espacial.

6. Intenta guardar el GeoDataFrame resultante como un nuevo archivo shapefile en la ruta especificada.
   Si ocurre un error durante el guardado, se imprime un mensaje de error y el script finaliza.
"""

import geopandas as gpd

try:
    # Lee los archivos de barrios y lugares
    NBI = gpd.read_file('../../0_Parcelas/NBI/NBI_Clasificados.shp')
    places = gpd.read_file('../places/places.shp')
except Exception as e:
    print(f"Error al leer los archivos: {e}")
    exit(1)

# Me aseguro de que los dos archivos tengan el mismo CRS
NBI = NBI.to_crs("EPSG:4326")
places = places.set_crs("EPSG:4326")

# Realiza una unión espacial para asignar atributos del barrio a los lugares
places_with_NBI = gpd.sjoin(places, NBI[['geometry', 'NBI_clas']], how='left', predicate='within')

# Asigna un valor por defecto para los edificios que están fuera de las áreas NBI
default_value = 2
places_with_NBI['NBI_clas'] = places_with_NBI['NBI_clas'].fillna(default_value)

places_with_NBI = places_with_NBI.drop(columns=['index_right'])

#print(places_with_NBI.columns)
places_with_NBI.to_file("../places/places.shp", driver='ESRI Shapefile')
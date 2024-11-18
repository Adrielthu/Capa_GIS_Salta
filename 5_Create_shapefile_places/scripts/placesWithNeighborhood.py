"""
Este script lee archivos shapefile que contienen información sobre barrios y lugares,
realiza una unión espacial para asignar el nombre del barrio a cada lugar, y guarda el resultado en un nuevo archivo shapefile.

Pasos del script:
1. Lee dos archivos shapefile usando GeoPandas:
   - `barrios`: Contiene las geometrías y nombres de los barrios de Salta.
   - `places`: Contiene las geometrías de los lugares.

2. Asegura que ambos GeoDataFrames tengan el mismo sistema de coordenadas (CRS) especificando 'EPSG:4326'.

3. Inicializa una nueva columna en el GeoDataFrame `places` llamada 'nom_largo' con el valor "Sin barrio" para todos los lugares.

4. Realiza una unión espacial ('spatial join') para asociar a cada lugar del GeoDataFrame `places` el valor de 'nom_largo'
   de los barrios en los que se encuentran. La unión se realiza con el método 'within', que verifica si un lugar está
   dentro de un barrio.

5. Asigna el valor 'Sin barrio' a las filas en la columna 'nom_largo' para aquellos lugares que no tienen un barrio asociado.

6. Elimina las columnas 'nom_largo_right', 'index_right' y 'nom_largo_left', generadas por la operación de unión espacial,
   para limpiar el GeoDataFrame.

7. Guarda el GeoDataFrame resultante como un nuevo archivo shapefile en la ruta especificada.
"""

import geopandas as gpd

try:
    # Lee los archivos de barrios y lugares
   barrios = gpd.read_file('../../0_Parcelas/Barrios/Barrios_Salta.shp')
   places = gpd.read_file('../places/places.shp')
except Exception as e:
    print(f"Error al leer los archivos: {e}")
    exit(1)

# Me aseguro de que los dos archivos tengan el mismo CRS
barrios = barrios.to_crs("EPSG:4326")
places = places.set_crs("EPSG:4326")

places['nom_largo'] = "Sin barrio"

# Realiza una unión espacial para asignar atributos del barrio a los lugares
places_with_barrios = gpd.sjoin(places, barrios[['geometry', 'nom_largo']], how='left', predicate='within')

# Asigna el valor 'Sin barrio' a las filas que no tienen un valor en 'nom_largo_right'
places_with_barrios['nom_largo'] = places_with_barrios['nom_largo_right'].fillna("Sin barrio")

places_with_barrios = places_with_barrios.drop(columns=['nom_largo_right', 'index_right', 'nom_largo_left'])

# Guarda el resultado en un nuevo archivo shapefile
places_with_barrios.to_file("../places/places.shp", driver='ESRI Shapefile')

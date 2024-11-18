"""
Script para asignar atributos de NBI (Necesidades Básicas Insatisfechas) a edificios mediante una unión espacial usando GeoPandas.

Este script carga archivos shapefile de edificios y áreas clasificadas por NBI, y utiliza una unión espacial para
asociar cada edificio con la clasificación NBI correspondiente. En caso de que un edificio no se encuentre dentro
de un área clasificada, se le asigna un valor por defecto (2). Finalmente, se guarda el resultado en un nuevo archivo shapefile.

Pasos del script:
-----------------
1. Lectura de archivos shapefile.

2. Transformación del sistema de coordenadas (CRS).
   - Convierte ambos GeoDataFrames a un sistema de coordenadas común (EPSG:4326) para asegurar compatibilidad en las operaciones espaciales.

3. Unión espacial:
   - Realiza una unión espacial (spatial join) entre los edificios y las áreas NBI para asignar a cada edificio el valor correspondiente de
     la clasificación NBI (`NBI_clas`). La unión se realiza utilizando el predicado 'within' para determinar si el edificio se encuentra
     dentro de un área NBI.

4. Asignación de valor por defecto:
   - Para aquellos edificios que no se encuentran dentro de un área NBI, se les asigna un valor por defecto de 2 en la columna `NBI_clas`.

5. Elimina la columna index_right:

6. Guardado del archivo resultante.

"""

import geopandas as gpd

# Lee los archivos de NBI y edificios
NBI = gpd.read_file("../data/NBI/NBI_Clasificados.shp")
buildings = gpd.read_file("../data/buildings/buildings-2015-3D.shp")

# Me aseguro de que ambos archivos tengan el mismo CRS
NBI = NBI.to_crs("EPSG:4326")
buildings = buildings.to_crs("EPSG:4326")

# Realiza una unión espacial para asignar atributos del barrio a los edificios
buildings_with_nbi = gpd.sjoin(buildings, NBI[['geometry', 'NBI_clas']], how='left', predicate='within')

# Asigna un valor por defecto para los edificios que están fuera de las áreas NBI
default_value = 2
buildings_with_nbi['NBI_clas'] = buildings_with_nbi['NBI_clas'].fillna(default_value)

buildings_with_nbi = buildings_with_nbi.drop(columns=['index_right'])

# Guarda el resultado en un nuevo archivo shapefile
buildings_with_nbi.to_file("../data/buildings/buildings-2015-3D.shp", driver='ESRI Shapefile')

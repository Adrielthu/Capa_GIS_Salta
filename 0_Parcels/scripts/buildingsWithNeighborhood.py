"""
Script para asignar atributos de barrios a edificios mediante una unión espacial usando GeoPandas.

Este script carga archivos shapefile de edificios y barrios de la ciudad de Salta, Argentina, y utiliza una
unión espacial para asociar cada edificio con el barrio correspondiente. En caso de que un edificio no se encuentre
dentro de un barrio, se le asigna un valor por defecto ("Sin barrio"). Finalmente, se guarda el resultado en un
nuevo archivo shapefile.

Pasos del script:
-----------------
1. Lectura de archivos shapefile.

2. Transformación del sistema de coordenadas (CRS).
   - Convierte ambos GeoDataFrames a un sistema de coordenadas común (EPSG:4326) para asegurar compatibilidad en las operaciones espaciales.

3. Unión espacial:
   - Realiza una unión espacial (spatial join) entre los edificios y las áreas barrio para asignar a cada edificio el valor correspondiente de
     la clasificación de barrio (`nom_largo`). La unión se realiza utilizando el predicado 'within' para determinar si el edificio se encuentra
     dentro de un área barrio.

4. Asignación de valor por defecto:
   - Para aquellos edificios que no se encuentran dentro de un área barrio, se les asigna un valor por defecto de "Sin barrio" en la columna `nom_largo`.

5. Elimina la columna index_right:

6. Guardado del archivo resultante.

"""
import geopandas as gpd

# Lee los archivos de barrios y edificios
barrios = gpd.read_file("../data/neighborhood/Barrios_Salta.shp")
buildings = gpd.read_file("../data/buildings/buildings-2015-3D.shp")

# Me aseguro de que ambos archivos tengan el mismo CRS
barrios = barrios.to_crs("EPSG:4326")
buildings = buildings.to_crs("EPSG:4326")

# Realiza una unión espacial para asignar atributos del barrio a los edificios
buildings_with_barrios = gpd.sjoin(buildings, barrios[['geometry', 'nom_largo']], how='left', predicate='within')

# Asigna un valor por defecto para los edificios que están fuera de las áreas NBI
buildings_with_barrios['nom_largo'] = buildings_with_barrios['nom_largo'].fillna("Sin barrio")

buildings_with_barrios = buildings_with_barrios.drop(columns=['index_right'])

# Guarda el resultado en un nuevo archivo shapefile
buildings_with_barrios.to_file("../data/buildings/buildings-2015-3D.shp", driver='ESRI Shapefile')
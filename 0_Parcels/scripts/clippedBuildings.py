"""
Script para filtrar y guardar edificios dentro de un área de interés utilizando Dask y GeoPandas.

Este script lee un archivo CSV que contiene datos de edificios con geometrías en formato WKT (Well-Known Text) y
un archivo shapefile que define el perímetro del área de interés (AOI). Utilizando Dask y Dask-GeoPandas para
manejar datos geoespaciales, el script realiza las siguientes operaciones:

1. Lectura del CSV con Dask.

2. Lectura del shapefile con GeoPandas.

3. Conversión de geometrías:
   Convierte la columna de geometrías en formato WKT del DataFrame de Dask a un GeoDataFrame utilizando la función
   `map_partitions` para aplicar `GeoSeries.from_wkt` de manera distribuida.

4. Ajuste del CRS (Sistema de Referencia de Coordenadas).

5. Clipping (recorte) de edificios:
   Utilizando la función `clip` de Dask-GeoPandas para filtrar los edificios que caen dentro del perímetro del AOI.

6. Exportación del archivo como archivo shapefile.


Entradas:
---------
- Un archivo CSV (`941_buildings.csv`) con una columna 'geometry' que contiene geometrías en formato WKT.
- Un archivo shapefile (`limite_conso.shp`) que define el área de interés.

Salida:
-------
- Un archivo shapefile (`buildings.shp`) que contiene únicamente los edificios que caen dentro del área de interés.

Notas:
------
- Asegurate de que las geometrías en el archivo CSV estén en formato WKT para que puedan ser correctamente convertidas
  a objetos geométricos con GeoPandas.
- Es importante que el CRS de ambos conjuntos de datos sea el mismo (EPSG:4326 en este caso) para que las operaciones
  de clipping se realicen.
"""

import geopandas as gpd
import dask_geopandas
import dask.dataframe as dd

# Lee el archivo CSV como un DataFrame de Dask
ddf = dd.read_csv("../data/941_buildings.csv")
# Lee el shapefile con GeoPandas
aoi = gpd.read_file("../data/perimeter/limite_conso.shp")

# Convierte la columna 'geometry' de WKT a geometrías utilizando map_partitions
gddf = dask_geopandas.from_dask_dataframe(
    ddf,
    geometry=ddf['geometry'].map_partitions(gpd.GeoSeries.from_wkt, meta=gpd.GeoSeries([]))
)

# Resetea el índice del GeoDataFrame
gddf = gddf.reset_index()

# Me aseguro de que ambos archivos tengan el mismo CRS
gddf = gddf.set_crs('EPSG:4326')
aoi = aoi.to_crs('EPSG:4326')

clipped = dask_geopandas.clip(gddf, aoi)

print(clipped.head())

clipped = clipped.compute()
clipped.to_file("../data/buildings/buildings.shp", driver='ESRI Shapefile')
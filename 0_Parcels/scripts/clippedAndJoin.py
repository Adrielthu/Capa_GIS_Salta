"""
Este script utiliza `geopandas` y `pandas` para procesar datos geoespaciales de edificios en formato shapefile (.shp).
El objetivo es combinar un conjunto de edificios recortados por un área de interés (AOI) con otra capa de edificios en 3D.


Pasos del script:
1. Lectura de archivos
   - Carga tres archivos shapefile:
     - `buildings`: Contiene los datos de edificios de Open Buildings.
     - `aoi`: Define el área de interés (AOI) para recortar los edificios.
     - `buildings_2015_3D`: Contiene datos de edificios en 3D de 2015.

2. Reproyección:
   - Asegura que los tres archivos tienen el mismo sistema de referencia de coordenadas (CRS) configurándolos a 'EPSG:4326'.
   - Esto es necesario para garantizar que todas las capas se alineen correctamente en el espacio geográfico.

3. Recorte de la capa de edificios
   - Utiliza el `gpd.clip` para recortar los edificios según el área de interés definida en `aoi`.
   - El resultado es un GeoDataFrame `clipped` que contiene solo los edificios que intersectan con el AOI.

4. Combinación de resultados
   - Combina los edificios en 3D de 2015 (`buildings_2015_3D`) con el GeoDataFrame recortado (`clipped`).
   - La concatenación se realiza con `pd.concat`, ignorando los índices originales para crear un nuevo conjunto de datos unificado.

5. Guardado del resultado
   - Guarda el GeoDataFrame combinado en un nuevo archivo shapefile llamado `buildingsWithMissings.shp`.
"""

import geopandas as gpd
import pandas as pd

buildings = gpd.read_file("../data/buildings/buildings.shp")
aoi = gpd.read_file("../data/perimeter/missing_buildings.shp")
buildings_2015_3D = gpd.read_file("../data/buildings/buildings-2015-3D.shp")

# Me aseguro de que todos los archivos tengan el mismo CRS
buildings = buildings.to_crs('EPSG:4326')
aoi = aoi.to_crs('EPSG:4326')
buildings_2015_3D = buildings_2015_3D.to_crs('EPSG:4326')

# Recorto el GeoDataFrame utilizando el área de interés (AOI)
clipped = gpd.clip(buildings, aoi)

# Combino las áreas recortadas con los edificios en 3D de 2015
result = pd.concat([buildings_2015_3D, clipped], ignore_index=True)

# Guardar el resultado
result.to_file("../data/buildings/buildingsWithMissings.shp")
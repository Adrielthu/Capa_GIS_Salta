# Pasos importantes para la correcta ejecución de los scripts

## Librerías requeridas:
    - GeoPandas: Para el manejo de datos geoespaciales y la conversión de geometrías.
    - Dask y Dask-GeoPandas: Para manejar grandes volúmenes de datos de manera eficiente y en paralelo.
    - Shapely: Para la manipulación y creación de geometrías.
    - tqdm: Para mostrar una barra de progreso durante la generación de puntos.
    - numpy: Para realizar operaciones matemáticas y manejar arreglos multidimensionales.
    - pandas: Para la manipulación y análisis de datos.
    - Levenshtein: Para calcular la distancia de Levenshtein, que mide la diferencia entre dos secuencias de caracteres.
    - requests: Para hacer solicitudes HTTP de manera sencilla.
    - unidecode: Para convertir texto Unicode a ASCII, eliminando acentos y otros caracteres especiales.

## Creación del entorno virtual en Python para Windows:

1. Si tenes Python 3:
```
python -m venv nombre_del_entorno
```
2. Después activala:
```
nombre_del_entorno\Scripts\activate
```
3. Por último, instala las librerias:
```
pip install -r requirements.txt
```
4. Para desactivar el entorno:
```
deactivate
```
# Guía de Configuración y Uso de QGIS

## Descargar QGIS:
[QGIS](https://www.qgis.org/en/site/forusers/download.html)

## Pluguins:
[Multipart Split](https://plugins.qgis.org/plugins/splitmultipart/) para aprender a usarlo mirá el [video](https://www.youtube.com/watch?v=Syas8ajiQ8w), útil para crear las regiones en el paso **1_Regions**.

[Google Maps en QGIS (Instalar complemento QuickMapService)](https://www.youtube.com/watch?v=Uvp5RmsmrSM).

## Agregar XYZ Tile Layers:
Para agregar más mapas a QGIS copia el script del archivo de texto `script_mapas.txt` que está en la carpeta **0_Parcels**.
Después:

1. Abrí QGIS.
2. Abrí la consola de python que está en complementos (o Plugins) y seleccioná Consola Python. Esto va a abrir una ventana donde podés escribir y ejecutar scripts en Python directamente dentro de QGIS.
3. Copia y pega el código del script en la consola directamente y apretá Run Script (ícono de play) en la consola para ejecutarlo.
4. Verificá que se descargaron correctamente haciendo click en el ícono XYZ.
5. Por último, elegí el mapa que necesites haciendo doble click en el mismo.
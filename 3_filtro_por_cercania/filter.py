# -*- coding: utf-8 -*-
import csv
from tqdm import tqdm

# Archivos de entrada y salida
INPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/3_filtro_por_cercania/PopularPlacesFull.csv'
OUTPUT_EMPTY_TYPE_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/3_filtro_por_cercania/PopularPlaces_EmptyType.csv'
OUTPUT_FILLED_TYPE_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/3_filtro_por_cercania/PopularPlaces_FilledType.csv'

# Contar las líneas del archivo de entrada para configurar tqdm
with open(INPUT_FILE, 'r', encoding='utf-8') as infile:
    total_lines = sum(1 for line in infile) - 1  # Restar 1 para no contar el encabezado

# Filtrar las filas y escribirlas en los archivos correspondientes
with open(INPUT_FILE, 'r', encoding='utf-8') as infile, \
     open(OUTPUT_EMPTY_TYPE_FILE, 'w', newline='', encoding='utf-8') as empty_type_outfile, \
     open(OUTPUT_FILLED_TYPE_FILE, 'w', newline='', encoding='utf-8') as filled_type_outfile:

    reader = csv.reader(infile)
    empty_type_writer = csv.writer(empty_type_outfile)
    filled_type_writer = csv.writer(filled_type_outfile)

    header = next(reader)  # Leer el encabezado
    empty_type_writer.writerow(header)  # Escribir el encabezado en el archivo de tipos vacíos
    filled_type_writer.writerow(header)  # Escribir el encabezado en el archivo de tipos completos

    # Usar tqdm para mostrar el progreso
    for row in tqdm(reader, total=total_lines, desc="Procesando filas"):
        if not row[1].strip():  # Si el campo 'type' (columna 1) está vacío
            empty_type_writer.writerow(row)
        else:
            filled_type_writer.writerow(row)

print("Separación completada. Las filas se guardaron en los archivos correspondientes.")

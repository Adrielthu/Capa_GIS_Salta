# -*- coding: utf-8 -*-

import shapefile

CSV_INPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/5_filtrar_por_tipo/PopularPlaces.csv'
SHP_OUTPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/7_crear_shapefile_places/places'

w = shapefile.Writer(SHP_OUTPUT_FILE, shapeType=1, encoding='utf8') # Point
# Crear SHP final
w.field('id',     'N', size=8) # id - 8 digitos
w.field('name',   'C', size=100)
w.field('type',   'C', size=50)
w.field('rating', 'N', size=4)
#
idx = 1
with open(CSV_INPUT_FILE, 'r', encoding='utf8') as fp:
    fp.readline() # Ignoro header
    for line in fp.readlines():
        splited = line[:-1].split(',') # borrar /n
        name = splited[0]
        type = splited[1]
        rating = int(splited[2])
        lat = float(splited[3])
        lon = float(splited[4])
        #
        w.point(lon, lat)
        w.record(idx, name, type, rating)
        idx += 1
w.close()

import os
import shapefile
from shapely.geometry import Point, Polygon
import math
from tqdm import tqdm  # Importa tqdm para la barra de progreso

INPUT_SHP_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/Parcelas/Radiosprecensales2021(octubre).shp'
OUTPUT_SHP_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/Parcelas/Radiosprecensales2021_parcels_1'

if not os.path.exists(INPUT_SHP_FILE):
    exit("El archivo de entrada no existe")

w = shapefile.Writer(OUTPUT_SHP_FILE, shapeType=1, encoding='utf8')
w.field('id',  'N', size=8)
w.field('sec', 'N', size=4)

id = 1
polygon_file = shapefile.Reader(INPUT_SHP_FILE, encoding='utf8')

for polygon in polygon_file.shapeRecords():
    try:
        # Acceso directo a los campos
        area_km2 = polygon.record['SUPERFICIE']
        area_m2 = area_km2 * 1000000
        max_houses = polygon.record['IND01']

        if max_houses > 0 and area_m2 > 0:
            density = max_houses / area_m2
            avg_distance_m = 1 / math.sqrt(density)
            OFFSET_X = avg_distance_m / 111000
            OFFSET_Y = avg_distance_m / 111000
        else:
            raise ValueError("Datos inválidos en el polígono.")

        coords = polygon.shape.__geo_interface__['coordinates'][0]
        coords = [(float(x), float(y)) for x, y in coords]
        poly = Polygon(coords)
        sectoral_index = polygon.record['sectoral']

        houses = 0
        first_x = poly.bounds[0]
        start_y = poly.bounds[1]
        sw_offsets = False

        # Usa tqdm para la barra de progreso
        with tqdm(total=max_houses, desc=f"Generating houses for sector {sectoral_index}") as pbar:
            while houses < max_houses:
                while start_y < poly.bounds[3]:
                    start_x = first_x
                    while start_x < poly.bounds[2]:
                        point = Point(start_x, start_y)
                        if poly.contains(point):
                            w.point(start_x, start_y)
                            w.record(id, sectoral_index)
                            id += 1
                            houses += 1
                            pbar.update(1)  # Actualiza la barra de progreso
                            if houses == max_houses:
                                start_y = poly.bounds[3]
                                break
                        start_x += OFFSET_X
                    start_y += OFFSET_Y
                start_y = poly.bounds[1]
                if not sw_offsets:
                    start_y += OFFSET_Y / 2
                    sw_offsets = True
                else:
                    first_x += OFFSET_X / 2
                    sw_offsets = False

        print(f"Generated {houses} out of {max_houses} houses for sector {sectoral_index}")

    except (ValueError, TypeError, AttributeError, KeyError) as e:
        print(f"Error en el polígono con sectoral {sectoral_index+1}: {e}")
        continue

w.close()

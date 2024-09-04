# -*- coding: utf-8 -*-

from collections import Counter

INPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/5_filtrar_por_tipo/PopularPlaces.csv'
TYPES = []

MARKOV_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/6_verificar_tipos_markov/places-markov.csv'
TYPES_MARKOV = []

OUTPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/6_verificar_tipos_markov/resultados.txt'

if __name__ == '__main__':
    in_file = open(INPUT_FILE, encoding='utf-8')
    in_file.readline()  # header
    for line in in_file.readlines():
        splited = line[:-1].split(',')  # borrar /n
        if len(splited) < 6:
            continue
        type = splited[1]  # type
        TYPES.append(type)
    in_file.close()

    in_file = open(MARKOV_FILE, encoding='utf-8')
    in_file.readline()  # header
    for line in in_file.readlines():
        splited = line[:-1].split(',')  # borrar /n
        type = splited[0]  # type
        TYPES_MARKOV.append(type)
    in_file.close()

    sorted_full = Counter(TYPES)
    sorted_full_mc = sorted_full.most_common()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        out_file.write(f'Total: {len(TYPES)}, Unicos: {len(sorted_full)}\n')
        for i in range(len(sorted_full_mc)):
            if sorted_full_mc[i][0] not in TYPES_MARKOV:
                if '+' not in sorted_full_mc[i][0]:
                    out_file.write(f'{sorted_full_mc[i][1]};{sorted_full_mc[i][0]}\n')

    print(f'Resultados guardados en {OUTPUT_FILE}')

import geopandas as gpd

try:
    # Lee los archivos de barrios y lugares
    NBI = gpd.read_file("../0_Parcelas/NBI/NBI_Clasificados.shp")
    places = gpd.read_file("places/places.shp")
except Exception as e:
    print(f"Error al leer los archivos: {e}")
    exit(1)

# Me aseguro de que los dos archivos tengan el mismo CRS
NBI = NBI.to_crs("EPSG:4326")
places = places.set_crs("EPSG:4326")

# Realiza una unión espacial para asignar atributos del barrio a los lugares
places_with_NBI = gpd.sjoin(places, NBI[['geometry', 'NBI_clas']], how='left', predicate='within')

# Asigna un valor por defecto para los edificios que están fuera de las áreas NBI
default_value = 2
places_with_NBI['NBI_clas'] = places_with_NBI['NBI_clas'].fillna(default_value)

places_with_NBI = places_with_NBI.drop(columns=['index_right'])

#print(places_with_NBI.columns)

try:
    # Guarda el resultado en un nuevo archivo shapefile
    places_with_NBI.to_file("places/places.shp", driver='ESRI Shapefile')
except Exception as e:
    print(f"Error al guardar el archivo: {e}")
    exit(1)
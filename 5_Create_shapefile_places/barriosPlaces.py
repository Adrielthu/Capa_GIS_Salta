import geopandas as gpd

# Lee los archivos de barrios y lugares
barrios = gpd.read_file("../0_Parcelas/Barrios/Barrios_Salta.shp")
places = gpd.read_file("places/places.shp")

# Me aseguro de que los dos archivos tengan el mismo CRS
barrios = barrios.to_crs("EPSG:4326")
places = places.set_crs("EPSG:4326")

places['nom_largo'] = "Sin barrio"

# Realiza una unión espacial para asignar atributos del barrio a los lugares
places_with_barrios = gpd.sjoin(places, barrios[['geometry', 'nom_largo']], how='left', predicate='within')

# Asigna el valor 'Sin barrio' a las filas que no tienen un valor en 'nom_largo_right'
places_with_barrios['nom_largo'] = places_with_barrios['nom_largo_right'].fillna("Sin barrio")

places_with_barrios = places_with_barrios.drop(columns=['nom_largo_right', 'index_right', 'nom_largo_left'])

# Guarda el resultado en un nuevo archivo shapefile
places_with_barrios.to_file("places/places.shp", driver='ESRI Shapefile')

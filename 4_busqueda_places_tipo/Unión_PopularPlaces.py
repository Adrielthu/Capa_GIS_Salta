import pandas as pd

# Archivos CSV de entrada
csv1 = "C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/3_filtro_por_cercania/PopularPlaces_FilledType.csv"
csv2 = "C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/archivo_predicciones.csv"

# Leer los archivos CSV en dataframes
df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

# Unir los dataframes
df_unido = pd.concat([df1, df2])

# Guardar el dataframe unido en un nuevo archivo CSV
df_unido.to_csv("C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/PopularPlacesFull-.csv", index=False)


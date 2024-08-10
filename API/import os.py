import os

# Ruta de la carpeta que contiene los archivos .csv
folder_path = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/Regiones'
# Obtener una lista de archivos en la carpeta que tienen la extensión .csv
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# Imprimir la lista de archivos .csv encontrados
print(csv_files)

# Si quieres asignar la lista a la variable INPUT_FILES
INPUT_FILES = csv_files

import pandas as pd

def count_types(input_csv, output_csv):
    # Lee el archivo CSV
    df = pd.read_csv(input_csv)

    # Contar las ocurrencias de cada valor en la columna 'type'
    type_counts = df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']

    # Guardar los resultados en un nuevo archivo CSV
    type_counts.to_csv(output_csv, index=False)

try:
    # Carga de los archivos CSV
    input_csv = 'UpdatedPopularPlaces.csv'
    output_csv = 'Count_types_popularplaces.csv'
except Exception as e:
    print(f"Error al leer los archivos: {e}")
    exit(1)

count_types(input_csv, output_csv)
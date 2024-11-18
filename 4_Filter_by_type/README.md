# Filtrado de Places por Tipo

En esta sección se procederá al filtrado y tratamiento de los datos de places, eliminando aquellos tipos de lugares irrelevantes para el análisis posterior, basándose en la información contenida en el archivo  `places_markov.csv` dentro de la carpeta `data`.

Los scripts están organizados para facilitar su ejecución en el orden indicado.

1. **Contabilización de Tipos No Registrados:**
    El script `0_markov.py` será ejecutado para contabilizar los tipos de lugares que no están registrados en el archivo `places_markov`.

2. **Filtrado de Places:**
    Se ejecutará el script `1_filterPlacesTypes.py` con el fin de filtrar los places de acuerdo con el archivo `places_markov`.

3. **Descartar Places No Registrados:**
    El script `2_descarteDePlaces.py` se utilizará para descartar aquellos places que no se encuentren en el archivo `places_markov`.

4. **Actualización de Tipos de Places:**
    El script `3_updatedMarkov.py` reemplazará los tipos de lugar en el archivo filtered_Popular_Places con los correspondientes del archivo `places_markov`.

5. **Verificación de Reducción de Tipos:**
    Finalmente, el script `4_countTypes.py` será ejecutado para contabilizar los tipos de lugares en el archivo actualizado y verificar que la cantidad de tipos se ha reducido.
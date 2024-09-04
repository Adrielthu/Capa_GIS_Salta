# Verificar existencia de tipos de Places en archivo de salida de Markov
1. Copiar al mismo directorio, archivo csv de salida del paso anterior y archivo de matriz de salida de estados Markov.
2. Correr script ***filterPlacesTypes.py*** y en consola se listan los tipos de places que no existen en salida de Markov.
3. Agregar tipos nuevos a archivo de salida de Markov, cambiar en places el tipo a uno existente o eliminar places.
4. Volver a correr script ***filterPlacesTypes.py*** hasta que no retorne tipos sin asociar.

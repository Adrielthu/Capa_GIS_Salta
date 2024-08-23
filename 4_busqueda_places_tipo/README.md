# Buscar categorías faltantes de Places
1. Copiar al mismo directorio, archivo csv de salida del paso anterior.
2. **Opcional**: Modificar en ***getGoogleTypes.py*** atributos **MIN_RATINGS** y **MATCH_GMB_CATEGORIES**.
3. **Notas**:
   - Se hace una consulta de type cada 30 segundos, para evitar ser detectado como bot.
   - Mientras corre el script no hacer otras consultas a Google desde la misma IP (principalmente a Google Maps).
   - Se recomienda usar una IP dedicada, alternativamente usar VPS o algún servicio como *pythonanywhere*.
3. Correr script ***getGoogleTypes.py*** y esperar salida.
4. Corregir archivo de salida, con los types no encontrados en la lista de *gmb_categories_us.txt* (indicados por ***).

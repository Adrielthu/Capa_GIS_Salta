# Generar Hogares y Añadir Atributos NBI y Nombre del Barrio
1. **Descarga de Edificios:**
    Se debe acceder a la página de [Google Open Buildings](https://sites.research.google/gr/open-buildings/#open-buildings-download) y descargar los edificios correspondientes al área de interés.

2. **Obtención o Creación del Ejido:**
    El ejido de la zona de interés debe ser descargado como archivo shapefile, KML (buscando "ejido de Salta capital" en Google) o bien crear una nueva capa en QGIS, dibujando un polígono que cubra la zona requerida. Posteriormente, se exportará la capa como archivo shapefile.

![buildings](https://i.imgur.com/2HoCUCn.jpg)

3. **Recorte de los Edificios al Área de Interés:**
    El archivo de edificios descargado será recortado al área específica de interés ejecutando el script `clippedBuildings.py`, lo que generará un archivo de edificios ajustado a dicha área.

![buildings](https://i.imgur.com/4WtNN4J.jpg)

4. **Descarga del Archivo NBI:**
    El archivo _"Total de Población con algún NBI por Fracción Censal 2010"_ deberá ser descargado desde [IDESA](http://www.idesa.gob.ar/geoservicios/) siguiendo las instrucciones para consumir geoservicios a través de QGIS con WMS o WFS.

5. **Incorporación del Atributo NBI a los Edificios:**
    El script `buildingsWithNBI.py` se utilizará para agregar el atributo NBI a cada polígono del archivo de edificios.

![buildings](https://i.imgur.com/2EKwRlq.jpg)

6. **Descarga de los Barrios de la Ciudad de Salta:**
    La capa de _"Barrios de la Ciudad de Salta"_ se descargará utilizando el mismo procedimiento indicado en el paso 4.

![buildings](https://i.imgur.com/n1tjCff.jpg)

7. **Adición del Atributo del Barrio a los Edificios:**
    Se ejecutará el script `buildingsWithNeighborhood.py` para añadir el atributo del barrio correspondiente a cada polígono del archivo de edificios.

![buildings](https://i.imgur.com/MGcajez.jpg)
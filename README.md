# 📌 Sobre el Proyecto

> [!IMPORTANT]
> Este proyecto fue realizado en colaboración con una institución académica y está basado en un caso real de análisis geoespacial sobre la ciudad de **Salta Capital**.  
> Aunque este trabajo se desarrolló con fines académicos y simula una aplicación en un contexto profesional, **el código es libre y puede ser reutilizado o adaptado con fines educativos o personales.**

---

🧠 **¿De qué se trata este proyecto?**  
Se desarrolló un **Sistema de Información Geográfica (GIS)** en Python para modelar la propagación de la tuberculosis. El proceso incluyó recolección, limpieza, normalización y análisis de datos geoespaciales.

🎯 **¿Para qué sirve esta capa GIS?**  
La capa modela la distribución de viviendas, edificios y lugares muy concurridos (restaurantes, gimnasios, etc) en Salta, junto con indicadores socioeconómicos. Esto ayuda a tomar decisiones en base a datos reales.

---

# 🛠️ Tecnologías y Herramientas

<details>
<summary>📦 Librerías y dependencias</summary>

- **GeoPandas**: Para el manejo de datos geoespaciales y la conversión de geometrías.
- **Dask + Dask-GeoPandas**: Para manejar grandes volúmenes de datos en paralelo.
- **Shapely**: Para crear y manipular geometrías.
- **tqdm**: Barra de progreso durante la generación de puntos.
- **NumPy**: Operaciones matemáticas y arrays.
- **Pandas**: Manipulación y análisis de datos.
- **Levenshtein**: Para medir similitudes entre textos.
- **requests**: Para hacer solicitudes HTTP.
- **unidecode**: Limpieza de texto eliminando acentos y caracteres especiales.

</details>

---

# ⚙️ Cómo Ejecutar el Proyecto

<details>
<summary> 🐍 Crear y activar entorno virtual en Windows</summary>

```bash
# Crear entorno
python -m venv nombre_del_entorno

# Activar entorno
nombre_del_entorno\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Desactivar entorno
deactivate
````
</details>

<details>
<summary> 🧭 Guía para Usar QGIS</summary>

## 🔽 Descargar QGIS
👉 [qgis.org/descargar](https://www.qgis.org/en/site/forusers/download.html)

## 🧩 Plugins recomendados

- 🔀 [Multipart Split](https://plugins.qgis.org/plugins/splitmultipart/)  
  👉 [Ver tutorial en YouTube](https://www.youtube.com/watch?v=Syas8ajiQ8w)  
  Útil para crear las regiones en el paso **1_Regions**.

- 🗺️ [QuickMapServices – Google Maps en QGIS](https://www.youtube.com/watch?v=Uvp5RmsmrSM)

## 🗂️ Agregar XYZ Tile Layers

Para agregar más mapas base en QGIS desde el script:

1. Abrí **QGIS**.
2. En el menú superior, andá a **Complementos** → **Consola de Python**.
3. Copiá y pegá el código desde el archivo `0_Parcels/script_mapas.txt`.
4. Hacé clic en **Run Script (▶️)**.
5. Verificá que se agregaron correctamente desde el ícono **XYZ Tiles** en el panel lateral.
6. Hacé doble clic en el mapa que quieras usar para cargarlo al lienzo.

</details>

---

# 🖼️ Ejemplos de salida

## 🏢 Huellas de Edificios

Se generaron a partir de la combinación de datos de **IDEMSA (2015)** y **Google Open Buildings**, para representar la ubicación real de edificaciones en Salta.

📌 Además, a estas huellas se les incorporó el indicador socioeconómico **NBI**, enriqueciendo cada edificio con información clave posterior a la integración de datos.

> [!NOTE]
> El NBI está almacenado como atributo en cada entidad, aunque no se represente visualmente en el mapa mostrado.

![Ejemplo huellas de edificios](https://i.imgur.com/RGkQ29o.png)

---

## 📍 Places de Interés

Se obtuvieron más de **27.000 registros** desde Google Places, incluyendo escuelas, hospitales, comercios y otros lugares clave.  
Después de llevar a cabo un proceso de limpieza y clasificación, se mantuvieron **15.000 registros** con atributos estandarizados.

> [!NOTE]
> La imagen solo visualiza la ubicación de los lugares, pero además, cada uno cuenta con atributos como tipo de lugar (hospital, gimnasio, etc), barrio y NBI.

![Ejemplo places](https://i.imgur.com/YirW3lj.png)

---

# 📚 Recursos Útiles

- [QGIS – Manual Oficial](https://docs.qgis.org/3.28/es/docs/index.html)  
- [Open Buildings Dataset – Google](https://sites.research.google/open-buildings/)  
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview)

---

# 📝 Licencia

📄 Este proyecto está licenciado bajo los términos de la [MIT License](./LICENSE).

---

Hecho con 💻 por [Adriel Starchevich](https://www.linkedin.com/in/tu-linkedin)  
📍 Paraná, Entre Ríos – Argentina

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Cargar los datos
data = pd.read_csv('C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/3_filtro_por_cercania/PopularPlaces_FilledType.csv')

# Preprocesamiento
X = data['Name']
y = data['type']

# Vectorización del texto
vectorizer = TfidfVectorizer()
X_vect = vectorizer.fit_transform(X)

# División de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.05, random_state=42)

# Entrenamiento del modelo SVM
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Evaluación del modelo
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))



# ----------------------------------- Cargar nuevos datos ----------------------------------------------
new_data = pd.read_csv('C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/PopularPlaces_EmptyType_Filtered.csv')

# Preprocesar los nuevos datos (vectorizar)
X_new = new_data['Name']
X_new_vect = vectorizer.transform(X_new)  # Usamos el vectorizador previamente entrenado

# Realizar predicciones
y_new_pred = model.predict(X_new_vect)

# Agregar las predicciones al DataFrame original
new_data['type'] = y_new_pred

# Guardar el resultado en un nuevo archivo CSV
new_data.to_csv('C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/archivo_predicciones.csv', index=False)




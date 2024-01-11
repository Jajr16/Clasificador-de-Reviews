import re
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import seaborn as sns
from sklearn.metrics import confusion_matrix
from unidecode import unidecode  # Agrega esta línea para eliminar acentos

# Descargar recursos de NLTK si no están instalados
nltk.download('punkt')
nltk.download('stopwords')

def preprocesar_texto(texto):
    # Conversión a minúsculas
    texto = texto.lower()
    
    # Eliminación de acentos
    texto = unidecode(texto)
    
    # Eliminación de signos de puntuación y caracteres especiales
    texto = re.sub(r'[^\w\s]', '', texto)
    
    # Tokenización
    tokens = word_tokenize(texto)
    
    # Eliminación de stop words
    stop_words = set(stopwords.words('spanish'))  # Cambia 'spanish' al idioma de tus reseñas
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lematización o stemming
    stemmer = SnowballStemmer('spanish')  # Cambia 'spanish' al idioma de tus reseñas
    tokens = [stemmer.stem(word) for word in tokens]
    
    # Reconstrucción del texto normalizado
    texto_normalizado = ' '.join(tokens)
    
    return texto_normalizado

def entrenar_modelo(X, y):
    # División del conjunto de datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalización del texto
    X_train = [preprocesar_texto(texto) for texto in X_train]
    X_test = [preprocesar_texto(texto) for texto in X_test]

    # Convierte los textos a vectores TF-IDF
    vectorizer = TfidfVectorizer(min_df=3)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Entrenamiento del modelo de Regresión Logística
    model = LogisticRegression()
    model.fit(X_train_tfidf, y_train)

    # Predicciones en el conjunto de prueba
    predictions = model.predict(X_test_tfidf)

    # Evaluar el rendimiento del modelo
    accuracy = accuracy_score(y_test, predictions)
    print(f'Accuracy: {accuracy}')

    reportefinal = classification_report(y_test, predictions)
    print(reportefinal)

    cm = confusion_matrix(y_test, predictions)
    print(cm)
    # Crear un mapa de calor usando seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Matriz de Confusión')
    plt.show()
    with open('./static/csv/calif.txt',"w",encoding="utf-8") as resultados:
        #  Imprime todas las predicciones y etiquetas reales
        resultados.write(f"Oracion{'':<990} | Etiqueta Real   | Predicción\n")
        resultados.write("-"*998 + "| ----------------|---------\n")
        for oracion, real, pred in zip(X_train, y_train, predictions):
            resultados.write(f"{oracion:<1000} | {real:<15} | {pred}\n")

    return model

def normalize_dataset():
    df_notNormalized = pd.read_csv('static/csv/reviews.csv')
    df_notNormalized.dropna(subset=['Phrase'], inplace=True) # Elimina datos NaN (vacíos) con un ''

    df_notNormalized.reset_index(drop=True, inplace=True)

    df_notNormalized.to_csv('static/csv/reviews1.csv', index=False)

normalize_dataset()

df = pd.read_csv('static/csv/reviews1.csv')
# Separar los valores entre frases y calificación
X = df['Phrase']
y = df['Rate']

modelo_entrenado = entrenar_modelo(X, y)


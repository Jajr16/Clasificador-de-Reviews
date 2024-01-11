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
import spacy
from sklearn.metrics import confusion_matrix
from unidecode import unidecode  # Agrega esta línea para eliminar acentos

from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

# Descargar recursos de NLTK si no están instalados
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('es_core_news_sm')



def preprocesar_review(texto):

    # Obtener las stop words
    stop_words = set(stopwords.words('spanish'))

    # Inicializar lematizador
    lemmatizer = WordNetLemmatizer()

    # Tokenizar el texto completo (considerando que ya está tokenizado en palabras)
    palabras = nltk.word_tokenize(texto)

    # Pasar las palabras a minúsculas, remover caracteres que no formen una palabra, remover signos de puntuación y eliminar acentos
    palabras = [unidecode(re.sub(r'\W', '', palabra.lower())) for palabra in palabras]

    # Eliminar stop words y lematizar las palabras
    palabras_procesadas = [lemmatizer.lemmatize(palabra) for palabra in palabras if palabra not in stop_words]

    # Unir las palabras procesadas para obtener el resultado final
    resultado = ' '.join(palabras_procesadas)

    return resultado


def procesar_csv(X):

    for texto in X:

        preprocesar_review(texto)

    return X

def entrenar_modelo(X, y):
    # División del conjunto de datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalización del texto
    X_train = [preprocesar_review(texto) for texto in X_train]
    print(X_train[0])

    X_test = [preprocesar_review(texto) for texto in X_test]
    print(X_test[0])

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
X = procesar_csv(X)
y = df['Rate']

modelo_entrenado = entrenar_modelo(X, y)


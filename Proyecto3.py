import re
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import seaborn as sns
from sklearn.metrics import confusion_matrix
from unidecode import unidecode  # Agrega esta línea para eliminar acentos

from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

# Descargar recursos de NLTK si no están instalados
nltk.download('punkt')
nltk.download('stopwords')

def preprocesar_review(texto):
    stop_words = set(stopwords.words('spanish'))
    lemmatizer = WordNetLemmatizer()

    # print(stop_words)

    palabras = nltk.word_tokenize(texto)
    palabras = [palabra.strip() for palabra in palabras]
    palabras = [unidecode(re.sub(r'\W', '', palabra.lower())) for palabra in palabras]
    palabras_procesadas = [lemmatizer.lemmatize(palabra) for palabra in palabras if palabra not in stop_words]
    resultado = ' '.join(palabras_procesadas)

    return resultado

def entrenar_modelo(X, y, vectorizer):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train = [preprocesar_review(texto) for texto in X_train]
    X_test = [preprocesar_review(texto) for texto in X_test]

    print(X_train[0])

    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    model = LogisticRegression()
    model.fit(X_train_vectorized, y_train)

    predictions = model.predict(X_test_vectorized)

    accuracy = accuracy_score(y_test, predictions)
    print(f'Accuracy: {accuracy}')

    reportefinal = classification_report(y_test, predictions)
    print(reportefinal)

    cm = confusion_matrix(y_test, predictions)
    print(cm)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Matriz de Confusión')
    plt.show()
    
    with open('./static/csv/calif.txt', "w", encoding="utf-8") as resultados:
        resultados.write(f"Oracion{'':<990} | Etiqueta Real   | Predicción\n")
        resultados.write("-" * 998 + "| ----------------|---------\n")
        for oracion, real, pred in zip(X_train, y_train, predictions):
            resultados.write(f"{oracion:<1000} | {real:<15} | {pred}\n")

    return model

def bag_of_words_model(X, y):
    vectorizer = CountVectorizer(min_df=3)
    return entrenar_modelo(X, y, vectorizer)

def tfidf_model(X, y):
    vectorizer = TfidfVectorizer(min_df=2)
    return entrenar_modelo(X, y, vectorizer)

def normalize_dataset():
    df_notNormalized = pd.read_csv('static/csv/reviews.csv')
    df_notNormalized.dropna(subset=['Phrase'], inplace=True)
    df_notNormalized.reset_index(drop=True, inplace=True)
    df_notNormalized.to_csv('static/csv/reviews1.csv', index=False)

normalize_dataset()

df = pd.read_csv('static/csv/reviews1.csv')
X = df['Phrase']
y = df['Rate']

# # Entrenar modelo con Bag of Words
# modelo_entrenado_bow = bag_of_words_model(X, y)

# Entrenar modelo con TF-IDF (también puedes usar este si lo prefieres)
modelo_entrenado_tfidf = tfidf_model(X, y)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
from ast import literal_eval
from preprocessing.limpieza import tokenizar
from sklearn import metrics
from unidecode import unidecode

def normalizar_texto():
    df_notNormalized = pd.read_csv('static/csv/reviews.csv')
    df_notNormalized.dropna(subset=['Phrase'], inplace=True) # Elimina datos NaN (vacíos) con un ''

    # Resetear el index del dataframe
    # Agrega una nueva columna 'Texto_sin_acentos'
    df_notNormalized['Texto_sin_acentos'] = df_notNormalized['Phrase'].apply(lambda x: unidecode(str(x)))
    df_notNormalized.reset_index(drop=True, inplace=True)
    
    # Separar los valores entre frases y calificación
    X_notNormalized = df_notNormalized['Texto_sin_acentos']
    y_notNormalized = df_notNormalized['Rate']

    from csv import writer
    with open('.\static\csv\\reviews1.csv', "w", newline="", encoding="utf-8") as Prueba:
        new_data = writer(Prueba)
        new_data.writerow(['Rate','Texto_sin_acentos'])
        for i, frase in enumerate(X_notNormalized):
            if not frase == '':
                palabra = (tokenizar(frase))
                new_data.writerow([y_notNormalized[i], palabra])


def modelo_entrenamiento():

    df = pd.read_csv('static/csv/reviews.csv',converters={'Phrase': literal_eval})

    X = df['Phrase']
    y = df['Rate']

    #Separamos datos de prueba y entrenamiento
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.33, random_state=42)
    print(X_train.head(10))

    # Convertir las listas de palabras a texto
    X_train_text = X_train.apply(lambda x: ' '.join(x))
    X_test_text = X_test.apply(lambda x: ' '.join(x))

    # Crear un pipeline con preprocesamiento y clasificador
    model = make_pipeline(
        TfidfVectorizer(tokenizer=tokenizar),
        LogisticRegression()
    )

    # Entrenar el modelo
    model.fit(X_train_text, y_train)

    # Predecir con el conjunto de prueba
    y_pred = model.predict(X_test_text)

    # with open('./static/csv/calif.txt',"a",encoding="utf-8") as reporte:
    #     print(reportefinal, file= reporte)

    predictions = model.predict(X_test_text)
    score_pred = metrics.accuracy_score(y_test, predictions)

    with open('./static/csv/calif.txt',"w",encoding="utf-8") as resultados:
        #  Imprime todas las predicciones y etiquetas reales
        resultados.write(f"Oracion{'':<990} | Etiqueta Real   | Predicción\n")
        resultados.write("-"*998 + "| ----------------|---------\n")
        for oracion, real, pred in zip(X_train_text, y_train, predictions):
            resultados.write(f"{oracion:<1000} | {real:<15} | {pred}\n")

    # Evaluar el modelo
    reportefinal = classification_report(y_test, y_pred)
    print(f'\n\nEl accuracy del modelo es: {score_pred}')
    print(reportefinal)
    
normalizar_texto()
modelo_entrenamiento()

# def Clasificar(texto):

#     # Obtén la clase predicha
#     clase_predicha = model.predict([texto])[0]
    
#     # Obtén las probabilidades para cada clase
#     probabilidades = model.predict_proba([texto])[0]
#     print(probabilidades)
    
#     return(clase_predicha)

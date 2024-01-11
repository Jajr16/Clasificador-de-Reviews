import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import spacy

# def correction(text):
#     """
#         Corrección de frases según el idioma
#     """
#     # Detectar lenguaje
#     language = ''
#     try: 
#         language = detect(text)
#     except Exception as e:
#         print(f'No se pudo: {e}')

#     # Corregir según el idioma
#     if language == 'es':
#         spell = Speller(lang='es')
#         corrected_text = spell(text)
#     elif language == 'en':
#         spell = Speller(lang='en')
#         corrected_text = spell(text)
#     else:
#         corrected_text = text

#     return corrected_text, language
# print(correction('Este texto esta mal escwrtio'))

STOPWORDS = set(stopwords.words("spanish"))
stemmer = SnowballStemmer("spanish")
lemmatizer = WordNetLemmatizer()
nlp = spacy.load('es_core_news_sm')

def limpiar_texto(texto):
    """
        Limpieza de textos (quitar caracteres especiales, palabras con un solo caracter, pasar texto a minusculas, etc...)
    """
    # Caracteres especiales
    texto = re.sub(r'\W', ' ', str(texto))
    # Eliminado las palabras que tengo un solo caracter
    texto = re.sub(r'\s+[a-zA-Z]\s+', ' ', texto)
    # Sustituir los espacios en blanco en uno solo
    texto = re.sub(r'\s+', ' ', texto, flags=re.I)
    # Convertimos textos a minusculas
    texto = texto.lower()

    return (texto)

def filtrar_stopwords_digitos(tokens):
    """
    Filtra stopwords y digitos de una lista de tokens.
    """
    return [token for token in tokens if token not in STOPWORDS and not token.isdigit()]

def stematizar(tokens):
    """
        Stematizar textos
    """
    return [stemmer.stem(token) for token in tokens]

def lematizar(tokens):
    """
        Lematizar textos utilizando WordNet.
    """
    texto = " ".join(tokens)
    doc = nlp(texto)
    # Obtener el lema de la palabra
    lema = [token.lemma_ for _, token in enumerate(doc)]

    return lema

def tokenizar(texto):
    texto_limpio = limpiar_texto(texto)
    doc = nlp(texto_limpio)
    tokens = [token.lemma_.lstrip(', ') for token in doc if not token.is_punct]
    tokens = filtrar_stopwords_digitos(tokens)
    textlematizado = lematizar(tokens)

    return textlematizado
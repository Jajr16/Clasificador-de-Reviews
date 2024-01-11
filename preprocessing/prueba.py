import spacy
nlp = spacy.load('es_core_news_sm')
def normalize(text):
    doc = nlp(text)
    words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
    lexical_tokens = [t.lower() for t in words if len(t) > 3 and     
    t.isalpha()]
    return lexical_tokens

import spacy
nlp = spacy.load('es_core_news_sm')
text = 'Son prácticas y muy lindas, espero que a mis hijas les encanten como a mi.'
doc = nlp(text)
lemmas = [tok.lemma_.lower() for tok in doc]
print(lemmas)

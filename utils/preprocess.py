import re
import string
import spacy
import en_core_web_sm

nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords(text):
    cleaned = clean_text(text)
    doc = nlp(cleaned)
    keywords = []
    for token in doc:
        if token.is_stop or token.is_punct or not token.is_alpha:
            continue
        if token.pos_ in {"NOUN", "PROPN", "VERB", "ADJ"}:
            keywords.append(token.lemma_)
    for entity in doc.ents:
        if entity.label_ in {"ORG", "PRODUCT", "TECH", "PERSON", "GPE"}:
            keywords.append(entity.text.lower())
    return " ".join(dict.fromkeys(keywords))

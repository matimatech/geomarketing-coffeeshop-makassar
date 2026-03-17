import re
import pandas as pd

from nlp_id.stopword import StopWord
from nlp_id.lemmatizer import Lemmatizer

stopwords = StopWord()
lemmatizer = Lemmatizer()

def clean_text(text: str):
    text = text.lower()
    # punctuation
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    # remove digit
    text = ''.join(char for char in text if not char.isdigit())
    # remove stopwords
    text = stopwords.remove_stopword(text)  
    return text

def lemmatize_tokens(tokens):
    return " ".join(lemmatizer.lemmatize(word) for word in tokens)

def extract_rating(text: str):
    return int(re.search(r"(\d+)", text).group())
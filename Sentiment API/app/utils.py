from dotenv import load_dotenv
import os
import json
import pandas as pd
import requests
from newspaper import Article
from datetime import datetime
import re
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
from gliner import GLiNER
from app.config import Config
from typing import Optional

load_dotenv()

model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

def input_sentiments_vader(data):
    sent = SentimentIntensityAnalyzer()
    polarity = sent.polarity_scores(data)
    return polarity.get("compound")

def gliner_ner(data):
    ner_dict = {}
    model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
    labels = ["person", "nationality", "religious group", "political group", "facility", "organisation", "country", "city", "state"]
    entities = model.predict_entities(data, labels, threshold=0.5)
    if not entities:
        return None
    for entity in entities:
        if entity["label"] not in ner_dict:
            ner_dict[entity["label"]] = [entity["text"]]
        else:
            if entity["text"] not in ner_dict.get(entity["label"]):
                ner_dict[entity["label"]].append(entity["text"])

    return ner_dict


def extract_actual_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try: 
        response = requests.get(url, headers=headers, timeout=30)
        article = Article(url)
        article.set_html(response.text)

        article.parse()
        article.nlp()
        return article.text
    except: 
        return "NA"
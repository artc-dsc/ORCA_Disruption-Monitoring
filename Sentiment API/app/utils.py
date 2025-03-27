from dotenv import load_dotenv
import requests
from newspaper import Article
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon', quiet=True)
from gliner import GLiNER
from app.config import Config
from typing import Optional, Dict
import gensim
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
import gensim.corpora as corpora
import os
import pickle 
import pyLDAvis.gensim
import pyLDAvis

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
    

def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def remove_stopwords(texts):
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
    return [[word for word in simple_preprocess(str(doc)) 
             if word not in stop_words] for doc in texts]

def generate_pyLDAvis_topics(text, num_topics, num_terms):
    data_words = list(sent_to_words(text))
    data_words = remove_stopwords(data_words)
    id2word = corpora.Dictionary(data_words)
    texts = data_words
    corpus = [id2word.doc2bow(text) for text in texts]
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)
    topics_data: Dict[str, str] = {}
    for topic_num, topic in lda_model.print_topics(num_words=num_terms):
        topics_data[f"Topic {topic_num}"] = str(topic)

    LDAvis_data_filepath = os.path.join('./LDA_visual_Latest/ldavis_prepared_'+str(num_topics))

    LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    with open(LDAvis_data_filepath, 'wb') as f:
        pickle.dump(LDAvis_prepared, f)

    score_data = {}
    score_data["Persplexity"] = lda_model.log_perplexity(corpus)
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words, dictionary=id2word, coherence='c_v')
    score_data["Coherence"] = coherence_model_lda.get_coherence()
    return score_data, topics_data

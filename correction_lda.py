r"""
LDA Model
=========

Introduces Gensim's LDA model and demonstrates its use on the NIPS corpus.

"""
from typing import List,Optional
import sys
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from xml.etree import ElementTree as ET
import argparse


from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import LdaModel
#import pyLDAvis
#import pyLDAvis.gensim_models as gensimvis
from datastructures import name_to_loader, Token
from nltk.corpus import stopwords


def filter_pos(token: Token) -> bool:
    if token.pos in ["ADV", "DET", "AUX", "NUM", "SCONJ", "CCONJ", "PUNCT", "ADP", "PRON"]:
        return False
    return True


def load_corpus(filename, format="json", lemmatize=True): 
    stop_words = set(stopwords.words('french'))
    corpus = name_to_loader[format](filename)
    docs = []
    for article in corpus.articles:
        docs.append([])
        for token in article.tokens:
            if filter_pos(token):
                if lemmatize: 
                    if token.text.isalnum() and not token.text.isnumeric() and len(token.text) > 1 and token.text not in stop_words:
                        docs[-1].append(token.lemma)
                else:
                    if token.text.isalnum() and not token.text.isnumeric() and len(token.text) > 1 and token.text not in stop_words :
                        docs[-1].append(token.text)

    return docs




    

# Add bigrams and trigrams to docs (only ones that appear 20 times or more).

def add_bigrams(docs: List[List[str]], min_count=20):
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
    return docs

def build_lda_model(
        docs: List[List[str]],
        num_topics=10,
        chunksize=20000,
        passes=20,
        iterations=40,
        eval_every=5,
        no_below=20,
        no_above=0.5
        ):


    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)
    docs = add_bigrams(docs, 20)
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    print('Number of unique tokens: %d' % len(dictionary),sys.stderr)
    print('Number of documents: %d' % len(corpus))

    _ = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token

    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every)
    return corpus, dictionary, model

def print_coherence(model, corpus):
    top_topics = model.top_topics(corpus)

# Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    avg_topic_coherence = sum([t[1] for t in top_topics]) / model.num_topics
    print('Average topic coherence: %.4f.' % avg_topic_coherence)

    from pprint import pprint
    pprint(top_topics)



'''def save_html_viz(model, corpus, dictionary, output_path):
    vis_data = gensimvis.prepare(model, corpus, dictionary)
    with open(output_path, "w") as f:
        pyLDAvis.save_html(vis_data, f)'''




def main(corpus_file:str, format: str, num_topics, output_path: Optional[str]=None, show_coherence: bool=False, noabove=0.5, nobelow=20):
    docs = load_corpus(corpus_file, format)
    docs = add_bigrams(docs)
    c, d, m = build_lda_model(docs, num_topics=num_topics, no_above=noabove, no_below=nobelow)
    #if output_path is not None:
        #save_html_viz(m, c, d, output_path)
    if show_coherence:
        print_coherence(m, c)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", help="fichier contenant le corpus à analyser")
    parser.add_argument("-f", default="json", help="format du corpus à charger", choices=["json", "xml", "pickle"])
    parser.add_argument("-n", default=10, type=int, help="nombre de topics (10)")
    parser.add_argument("-o", default=None, help="génère la visualisation ldaviz et la sauvegarde dans le fichier html indiqué")
    parser.add_argument("-c", action="store_true", default=False, help="affiche les topics et leur cohérence")
    parser.add_argument("--nobelow", type=int, default=20, help="ignorer les mots trop peu fréquents")
    parser.add_argument("--noabove", type=float, default=0.5, help="ignorer les mots trop fréquents")
    args = parser.parse_args()
    main(args.json_file, args.f, args.n, args.o, args.c, args.noabove, args.nobelow)

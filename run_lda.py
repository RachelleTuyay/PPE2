r"""
LDA Model
=========

Introduces Gensim's LDA model and demonstrates its use on the NIPS corpus.
"""
import argparse
import logging
import os
import re
import tarfile
import json
import glob
import xml.etree.ElementTree as ET
import spacy
import pickle
from datastructures import Corpus, Article, Token

import smart_open
from nltk.tokenize import RegexpTokenizer
from nltk import download
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases, LdaModel
from gensim.corpora import Dictionary
from pprint import pprint

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

download('wordnet')
download('punkt')
download('stopwords')

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

name_to_loader = {"xml" : Corpus.load_xml,
                  "json": Corpus.load_json,
                  "pickle": Corpus.load_pickle}

def load_and_tokenize(file, format) -> list[Token]:
    """Tokenisation des termes du corpus."""

    stop_words = set(stopwords.words('french'))  # Liste des mots à ignorer

    #Chargement du corpus

    docs = name_to_loader[format](file)

    # Traitement de chaque document

    docs = [article for article in docs.articles] #Transformer l'objet Corpus en liste d'Article

    # Filtrage des mots :
    docs = [article.tokens for article in docs]  #Récupérer chaque liste de tokens de chaque article

    docs = [token for tokens in docs for token in tokens] # Transformer la liste de liste de tokens en liste de tokens
                                                                            # Autrement dit regrouper tous les tokens de tous les articles ensemble
    docs = [token for token in docs if token.text.isalnum() and token.text not in stop_words]  # Garder les mots alphanumériques et non-stopwords

    # Suppression des nombres et des mots d'une seule lettre
    docs = [token for token in docs if not token.text.isnumeric() and len(token.text) > 1]

    return docs

def filter_by_pos(docs, allowed_pos):
    """Filtrer sur les catégories grammaticales"""

    filtered_docs = []

    filtered = [token for token in docs if token.pos in allowed_pos]
    filtered_docs.append(filtered)

    return filtered_docs

def lemmatize(docs):
    """Lemmatisation des documents."""
    
    lemmatized_docs = [[token.lemma for token in doc] for doc in docs]
    return lemmatized_docs

def get_text_tokens(docs):
    """Récupère le mot-forme du token"""
    docs = [[token.text for token in doc] for doc in docs]
    return docs

def bigrams(docs):
    """Ajout des bigrammes aux documents."""
    bigram = Phrases(docs, min_count=20)
    new_docs = []  # Liste pour stocker les documents modifiés

    for doc in docs:
        new_doc = doc + [token for token in bigram[doc] if "_" in token]
        new_docs.append(new_doc)

    return new_docs

def train_lda(docs):
    """Entraîne un modèle LDA."""
    dictionary = Dictionary(docs)
    #dictionary.filter_extremes(no_below=20, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        chunksize=2000,
        alpha='auto',
        eta='auto',
        iterations=400,
        num_topics=10,
        passes=20,
        eval_every=None
    )
    print(f"Taille du dictionnaire après filtrage : {len(dictionary)}")
    print(f"Taille du corpus : {len(corpus)}")

    return model, dictionary, corpus

def main():
    parser = argparse.ArgumentParser(description="Topic modeling")
    parser.add_argument("file", help="Chemin du fichier/dossier contenant le corpus")
    parser.add_argument("format", choices=["json", "xml", "pickle"], help="Format du corpus")
    parser.add_argument("methode", choices=["lemme", "mot-forme"], help="Choix entre lemme ou mot-forme")
    parser.add_argument("-p", "--pos", help="Catégories grammaticales à considérer, en majuscules; exemple : VERB NOUN PRON", nargs="*" )
    args = parser.parse_args()

    docs_tokenized = load_and_tokenize(args.file, args.format)
    if not docs_tokenized:
        raise ValueError("Aucun document extrait. Vérifiez votre fichier/dossier.")

    print("Taille du corpus :", len(docs_tokenized))
    print(f"Methode choisis : {args.methode}")
    #print(docs[0][:500])

    #filtrer sur les catégories grammaticales ( ne prendre que les noms et les verbes par exemple)
    if args.pos :
        docs_processed = filter_by_pos(docs_tokenized, args.pos)

    #Lemmatisation ou extractiond des mots-formes:
    if args.methode == "lemme" :
          docs_processed = lemmatize(docs_processed)
    
    elif args.methode == "mot-forme" :
        docs_processed = get_text_tokens(docs_processed)

    #Bigrammes :
    docs_bigrams = bigrams(docs_processed)

    #Modèle LDA :
    model, dictionary, corpus = train_lda(docs_bigrams)
    if len(dictionary) == 0 or len(corpus) == 0:
        raise ValueError(" !!! Erreur : Le dictionnaire ou le corpus est vide après filtrage !")

    #Affichage des résultats
    top_topics = model.top_topics(corpus)
    avg_topic_coherence = sum([t[1] for t in top_topics]) / 10
    print(f'Average topic coherence: {avg_topic_coherence:.4f}')
    pprint(top_topics)

if __name__ == "__main__":
    main()


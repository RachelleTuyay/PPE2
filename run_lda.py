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

def extract_documents(folder_path, file_format):
    """Extrait les documents depuis un dossier contenant des fichiers XML."""
    if file_format not in {"xml", "json"}:
        raise ValueError(f"Format non pris en charge : {file_format}")

    folder_path = os.path.abspath(folder_path)  # Normaliser le chemin du dossier
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(f".{file_format}")]

    if not files:
        raise FileNotFoundError(f"Aucun fichier {file_format} trouvé dans {folder_path}")

    for file in files:
        yield from read_file(file, file_format)


def read_file(file_path, file_format):
    """Lit un fichier et extrait son contenu selon son format."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if file_format == "json":
            data = json.loads(content)
            if isinstance(data, list):
                yield from data
            elif isinstance(data, dict):
                yield data.get("text", "")

        elif file_format == "xml":
            try:
                tree = ET.parse(file_path)  # Plus robuste que ET.fromstring
                root = tree.getroot()
                yield " ".join(elem.text.strip() for elem in root.iter() if elem.text)
            except ET.ParseError:
                logging.error(f"Erreur d'analyse XML dans {file_path}")


        else:
            raise ValueError(f"Format non pris en charge : {file_format}")

    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier {file_path}: {e}")

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def tokenize(docs):
    """Tokenisation des documents."""
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('french'))  # Liste des mots à ignorer

    # Traitement de chaque document
    for idx in range(len(docs)):
        docs[idx] = docs[idx].lower()
        docs[idx] = tokenizer.tokenize(docs[idx])

        # Filtrage des mots :
        docs[idx] = [
            word for word in docs[idx]  # Parcours de chaque mot
            if word.isalnum() and word not in stop_words  # Garder les mots alphanumériques et non-stopwords
        ]

        # Suppression des nombres et des mots d'une seule lettre
        docs[idx] = [word for word in docs[idx] if not word.isnumeric() and len(word) > 1]

    return docs

def lemmatize(docs):
    """Lemmatisation des documents."""
    lemmatizer = WordNetLemmatizer()
    docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]
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
    dictionary.filter_extremes(no_below=20, no_above=0.5)
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
    parser.add_argument("format", choices=["json", "xml"], help="Format du corpus")
    parser.add_argument("methode", choices=["lemme", "mot-forme"], help="Choix entre lemme ou mot-forme")
    args = parser.parse_args()

    docs = [doc for doc in extract_documents(args.file, args.format)]
    if not docs:
        raise ValueError("Aucun document extrait. Vérifiez votre fichier/dossier.")

    print("Taille du corpus :", len(docs))
    print(f"Methode choisis : {args.methode}")
    #print(docs[0][:500])

    #Tokénisation :
    docs_tokenized = tokenize(docs)

    #Lemmatisation :
    docs_processed = lemmatize(docs_tokenized) if args.methode == "lemme" else docs_tokenized

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


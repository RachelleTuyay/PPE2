# analyzers.py

import spacy
from pathlib import Path
from datastructures import Article, Corpus, Token
from dataclasses import asdict
import json
import argparse

# 1. load modèle de spacy
def load_spacy_model():
    return spacy.load("fr_core_news_sm")

# 2. analyser une texte et retourene List[Token]
def analyze_text_spacy(text: str, nlp) -> list[Token]:
    doc = nlp(text)
    tokens = []
    for token in doc:
        tokens.append(Token(
            text=token.text,
            lemma=token.lemma_,
            pos=token.pos_
        ))
    return tokens

# 3. analyser un Article
def analyze_article_spacy(article: Article, nlp) -> Article:
    article.title_tokens = analyze_text_spacy(article.title, nlp)
    article.description_tokens = analyze_text_spacy(article.description, nlp)
    return article

def main():
    parser = argparse.ArgumentParser(description="Analyse un corpus avec spaCy")
    parser.add_argument("input", type=Path, help="Fichier XML du corpus à analyser")
    parser.add_argument("output", type=Path, help="Fichier XML de sortie")

    args = parser.parse_args()

    print("[INFO] Chargement du modèle spaCy...")
    nlp = load_spacy_model()

    print("[INFO] Chargement du corpus...")
    corpus = Corpus.load_xml(args.input)

    print("[INFO] Analyse des articles...")
    for i, article in enumerate(corpus.articles):
        corpus.articles[i] = analyze_article_spacy(article, nlp)

    print("[INFO] Sauvegarde du corpus enrichi...")
    Corpus.save_xml(corpus, args.output)

if __name__ == "__main__":
    main()

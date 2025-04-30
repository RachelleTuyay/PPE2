import argparse
import os
from datastructures import Corpus, Article, Token
#from trankit import Pipeline
import stanza
from pathlib import Path
import json
import sys

# Cache pour le pipeline Trankit pour éviter de le charger plusieurs fois
_pipeline = None

def get_pipeline():
    """Charge et retourne le pipeline Trankit"""
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline('french', gpu=False)
        _pipeline.add('english')
    return _pipeline

def analyze_with_trankit(article: Article) -> Article:
    """Analyse un article avec Trankit et retourne l'article enrichi avec les tokens analysés"""
    # Combine le titre et la description pour l'analyse
    text = f"{article.title} {article.description}"
    if not text.strip():
        return article  # Si le texte est vide, retourner l'article non modifié
    
    p = get_pipeline()
    try:
        # Analyse le texte avec Trankit
        result = p(text)

        tokens = []
        for sentence in result['sentences']:
            for token_data in sentence['tokens']:
                token = Token(
                    text=token_data['text'],
                    lemma=token_data.get('lemma', None),
                    pos=token_data.get('upos', None)
                )
                tokens.append(token)
        # Ajoute les tokens à l'article
        article.tokens = tokens
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'article {article.id}: {e}")

    return article


def load_spacy():
    import spacy
    return spacy.load("fr_core_news_md")

def load_stanza():
    import stanza
    # stanza.download("fr")  # garder pour la première exécution uniquement
    return stanza.Pipeline("fr", processors="tokenize,pos,lemma")


def analyze_stanza(model, article : Article) -> Article:
    result = model( (article.title or "" ) + "\n" + (article.description or ""))
    output = []
    for sent in result.sentences:
        output.append([])
        for token in sent.words:
            output[-1].append(Token(token.text, token.lemma, token.upos))
    article.tokens = output
    return article

def load_spacy():
    import spacy
    return spacy.load("fr_core_news_md")

def analyze_spacy(model, article : Article) -> Article:
    text = model( (article.title or "" ) + "\n" + (article.description or ""))
    result = model(text)
    analysis = []
    for sentence in result.sents:
        for token in sentence:
            if token.text.strip():
                analysis.append(Token(token.text, token.lemma_, token.pos_))
    article.tokens = analysis
    return article


def main():
    parser = argparse.ArgumentParser(description="Analyse linguistique de corpus avec Trankit")
    parser.add_argument("input_file", help="Input file containing filtered articles corpus")
    parser.add_argument("analyzer", choices=["trankit", "spacy", "stanza"], help="Choice of syntax analyzer to use")
    parser.add_argument("save", choices=["json", "xml", "pickle"], help="Output format for saving the analysis")
    args = parser.parse_args()
    
    # Load corpus based on specified format
    input_path = Path(args.input_file)
    if ".json" in args.input_file:
        corpus = Corpus.load_json(input_path)
    elif ".xml" in args.input_file:
        corpus = Corpus.load_xml(input_path)
    elif ".pickle" in args.input_file:
        corpus = Corpus.load_pickle(input_path)
    
    # Analyze articles with the specified analyzer
    if args.analyzer == "trankit":
        print(f"Analyzing {len(corpus.articles)} articles with Trankit...")
        for i, article in enumerate(corpus.articles):
            if i % 10 == 0:  # Display progress every 10 articles
                print(f"Analyzing article {i+1}/{len(corpus.articles)}")
            analyze_with_trankit(article)

    elif args.analyzer == "stanza" :
        model = load_stanza()
        print(f"Analyzing {len(corpus.articles)} articles with Stanza...")
        for i, article in enumerate(corpus.articles):
            if i % 10 == 0:  # Display progress every 10 articles
                print(f"Analyzing article {i+1}/{len(corpus.articles)}")
            analyze_stanza(model,article)
    
    elif args.analyzer == "spacy" :
        model = load_spacy()
        print(f"Analyzing {len(corpus.articles)} articles with Spacy...")
        for i, article in enumerate(corpus.articles):
            if i % 10 == 0:  # Display progress every 10 articles
                print(f"Analyzing article {i+1}/{len(corpus.articles)}")
            analyze_spacy(model, article)


    # Save the analyzed corpus in specified format
    inputbasename = os.path.splitext(os.path.basename(args.input_file))[0]
    output_filename = f"{inputbasename}_analyzed.{args.save}"
    print(f"Saving analyzed corpus to {output_filename}...")
    
    if args.save == "json":
        corpus.save_json(output_filename)
    elif args.save == "xml":
        corpus.save_xml(output_filename)
    elif args.save == "pickle":
        corpus.save_pickle(output_filename)
    
    print("Analysis completed successfully!")

if __name__ == "__main__":
    main()
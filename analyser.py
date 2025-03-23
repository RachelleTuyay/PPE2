import argparse
import os
from datastructures import Corpus, Article, Token
from trankit import Pipeline
from pathlib import Path
import json
import sys

# Cache pour le pipeline Trankit pour éviter de le charger plusieurs fois
_pipeline = None

def get_pipeline():
    """Charge et retourne le pipeline Trankit (singleton)"""
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

def main():
    parser = argparse.ArgumentParser(description="Analyse linguistique de corpus avec Trankit")
    parser.add_argument("input_file", help="Fichier corpus d'entrée (json, xml ou pickle)")
    parser.add_argument("--output", "-o", help="Fichier de sortie (json, xml ou pickle)", default=None)
    parser.add_argument("--limit", type=int, help="Limite le nombre d'articles à analyser", default=None)
    args = parser.parse_args()
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(args.input_file):
        print(f"Erreur: Le fichier '{args.input_file}' n'existe pas.")
        sys.exit(1)
    
    # Définir le fichier de sortie s'il n'est pas spécifié
    if args.output is None:
        base_name = os.path.splitext(args.input_file)[0]
        args.output = f"{base_name}_analyzed.json"
    
    # Charger le corpus
    input_path = Path(args.input_file)
    extension = input_path.suffix.lower()
    
    if extension == '.json':
        corpus = Corpus.load_json(input_path)
    elif extension == '.xml':
        corpus = Corpus.load_xml(input_path)
    elif extension in ['.pkl', '.pickle']:
        corpus = Corpus.load_pickle(input_path)
    else:
        print(f"Format non supporté: {extension}. Utilisez .json, .xml ou .pickle")
        sys.exit(1)
    
    # Limiter le nombre d'articles à analyser si demandé
    articles_to_analyze = corpus.articles[:args.limit] if args.limit else corpus.articles
    
    print(f"Analyse de {len(articles_to_analyze)} articles...")
    
    # Analyser chaque article
    for i, article in enumerate(articles_to_analyze):
        if i % 10 == 0:  # Afficher une progression tous les 10 articles
            print(f"Analyse de l'article {i+1}/{len(articles_to_analyze)}")
        analyze_with_trankit(article)
    
    # Sauvegarder le corpus analysé
    output_path = Path(args.output)
    extension = output_path.suffix.lower()
    
    print(f"Sauvegarde du corpus analysé dans {args.output}...")
    
    if extension == '.json':
        corpus.save_json(output_path)
    elif extension == '.xml':
        corpus.save_xml(output_path)
    elif extension in ['.pkl', '.pickle']:
        corpus.save_pickle(output_path)
    else:
        print(f"Format de sortie non supporté: {extension}. Utilisation de .json par défaut")
        corpus.save_json(Path(f"{os.path.splitext(args.output)[0]}.json"))
    
    print("Analyse terminée avec succès!")

if __name__ == "__main__":
    main()
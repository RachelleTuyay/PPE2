import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from datastructures import Corpus, Article
import rss_reader

def lire_corpus_glob(dossier_entree):
    """Parcourt récursivement un dossier avec Path.glob() et récupère tous les fichiers XML"""
    dir = Path(dossier_entree)
    fichiers_xml = sorted(dir.glob('**/*.xml'))
    return fichiers_xml

def lire_corpus_os(dossier_entree):
    """Parcourt récursivement un dossier avec os.listdir() et os.path et récupère tous les fichiers XML"""
    fichiers_xml = []

    for element in os.listdir(dossier_entree):
        chemin_complet = os.path.join(dossier_entree, element)
        if os.path.isdir(chemin_complet):
            fichiers_xml.extend(lire_corpus_os(chemin_complet))  
        elif os.path.isfile(chemin_complet) and chemin_complet.endswith(".xml"):
            fichiers_xml.append(chemin_complet)

    return fichiers_xml

def lire_corpus_path(dossier_entree):
    """Fonction pour trouver des fichiers XML et les traiter avec pathlib.Path"""
    path_to_files = Path(dossier_entree)
    xml_files = []

    if not path_to_files.exists():
        print("Le chemin n'est pas valide.")
        return xml_files

    if not path_to_files.is_dir():
        print("Ce n'est pas un dossier, veuillez réessayer avec un autre chemin.")
        return xml_files

    print("C'est effectivement un dossier : le programme peut démarrer.")

    def recursive(current_path):
        for item in current_path.iterdir():
            if item.is_file() and ".xml" in str(item):
                xml_files.append(item)
            elif item.is_dir():
                recursive(item)
    
    recursive(path_to_files)
    return xml_files

def get_output_filename(xml_file, dossier_entree, dossier_sortie):
    """Générer un nom de fichier de sortie basé sur le fichier XML"""
    rel_path = os.path.relpath(xml_file, dossier_entree)  # Chemin relatif
    file_name_simple = os.path.splitext(rel_path)[0]
    return os.path.join(dossier_sortie, file_name_simple + ".txt")

def filtre_date(article, date_debut, date_fin):
    """
    Filtrer les articles par date
    """
    # Analyser la date (si elle existe)
    if article.date != " ":
        try:
            date = datetime.strptime(article.date, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
        except ValueError:
            return True  # En cas d'erreur de format, on garde l'article
    else:
        return True  # Si pas de date, on garde l'article

    if date_debut and date < datetime.strptime(date_debut, "%Y-%m-%d"):
        return False

    if date_fin and date > datetime.strptime(date_fin, "%Y-%m-%d"):
        return False
    
    return True

def filtre_source(article, sources):
    """Filtrer les articles par source"""
    if not sources:
        return True
    
    article_source = article.source.lower()
    
    return any(s.lower() in article_source for s in sources)

def filtre_categories(article, categories):
    """
    Filtrer les articles selon catégories
    """
    if not categories:
        return True
    
    if article.categories:
        return any(cat.lower() in [c.lower() for c in categories] for cat in article.categories)
    
    return False  # Si pas de catégories, on exclut par défaut

def filtrage(corpus, date_debut=None, date_fin=None, sources=None, categories=None):
    """Applique tous les filtres spécifiés au corpus"""
    articles_filtres = []
    id_unique = set()
    
    for article in corpus.articles:
        # Vérifier tous les filtres applicables
        if date_debut is not None or date_fin is not None:
            if not filtre_date(article, date_debut, date_fin):
                continue
        
        if sources:
            if not filtre_source(article, sources):
                continue
        
        if categories:
            if not filtre_categories(article, categories):
                continue
        
        # Si l'article passe tous les filtres et n'est pas un doublon
        if article.id not in id_unique:
            id_unique.add(article.id)
            articles_filtres.append(article)
    
    return Corpus(articles_filtres)

def run_method(method, lecture, dossier_entree):
    """Appelle la méthode sélectionnée avec le fichier XML"""

    lire_func = {"glob": lire_corpus_glob, "os": lire_corpus_os, "path": lire_corpus_path}
    xml_files = lire_func[lecture](dossier_entree)

    method_func = {"regex": rss_reader.lire_rss_regex, 
                  "etree": rss_reader.lire_rss_etree, 
                  "feedparser": rss_reader.lire_rss_feedparser}
    
    if method not in method_func:
        print("Erreur : Méthode invalide. Utilisez 'regex', 'etree' ou 'feedparser'.")
        sys.exit(1)

    articles_total = []
    for file in xml_files:
        try:
            articles = method_func[method](file)
            articles_total.extend(articles)
        except Exception as e:
            print(f"Impossible de traiter le fichier {file}, erreur: {e}")

    return articles_total

def main():
    """Gère l'entrée utilisateur avec des arguments Bash pour le parcours et le filtrage"""
    parser = argparse.ArgumentParser(description="Parcours et filtrage de fichiers RSS.")
    parser.add_argument("dossier_entree", help="Dossier comprenant les fichiers XML d'entrée")
    parser.add_argument("lecture", choices=["glob", "os", "path"], 
                        help="Choisir le module utilisé pour lire le dossier d'entrée")
    parser.add_argument("method", choices=["regex", "etree", "feedparser"], 
                        help="Méthode d'extraction (regex, etree, feedparser)")
    parser.add_argument("--start-date", help="Filtrer les articles publiés après cette date (format YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Filtrer les articles publiés avant cette date (format YYYY-MM-DD)")
    parser.add_argument("--source", nargs="+", help="Filtrer par une ou plusieurs sources")
    parser.add_argument("--categorie", nargs="+", help="Filtrer par une ou plusieurs catégories")
    parser.add_argument("--output", "-o", help="Fichier de sortie (format: json, xml ou txt)", default="output.json")
    args = parser.parse_args()

    if not os.path.isdir(args.dossier_entree):
        print(f"Erreur : Le dossier '{args.dossier_entree}' n'existe pas.")
        sys.exit(1)

    # Collecter tous les articles
    articles = run_method(args.method, args.lecture, args.dossier_entree)
    
    # Convertir en objets Article pour le corpus
    corpus_articles = [Article.from_dict(article) for article in articles]
    corpus = Corpus(corpus_articles)
    
    # Appliquer les filtres si nécessaire
    if args.start_date or args.end_date or args.source or args.categorie:
        corpus = filtrage(corpus, args.start_date, args.end_date, args.source, args.categorie)
    
    # Sérialiser le résultat
    output_format = os.path.splitext(args.output)[1][1:] if '.' in args.output else 'json'
    
    if output_format == 'json':
        corpus.to_json(args.output)
    elif output_format == 'xml':
        corpus.to_xml(args.output)
    elif output_format in ['txt', 'text']:
        corpus.to_text(args.output)
    else:
        print(f"Format de sortie non pris en charge: {output_format}. Utilisation de JSON par défaut.")
        corpus.to_json(args.output)
        
    print(f"Traitement terminé. {len(corpus.articles)} articles ont été écrits dans {args.output}")

if __name__ == "__main__":
    main()
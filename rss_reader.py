import xml.etree.ElementTree as ET  #importe le module ElementTree pour analyser les fichiers XML
from pathlib import Path
import sys  #importe le module sys pour gérer les arguments de la ligne de commande

#R2#
#fonction pour lire et filtrer les articles d'un corpus d'RSS
def filter_rss_source(dossier: str) -> list[dict]:
    all_articles = []
    seen_articles = set()

    #recherche de tous les fichiers XML dans le dossier (et sous-dossiers)
    for fichier in Path(dossier).glob("**/*.xml"):
        articles = rss_reader_etree(fichier)  # Appel de la fonction qui lit un fichier RSS

        for article in articles:
            if article["id"] not in seen_articles:  # Assurer l'unicité des articles
                seen_articles.add(article["id"])
                all_articles.append(article)

    return all_articles  # Retourne une liste de tous les articles uniques


#fonction pour afficher les articles extraits du corpus
def arborescence_rss_etree(dossier):
    path = Path(dossier)

    if not path.exists():
        print(f"Erreur : le dossier {dossier} n'existe pas.")
        return
    
    #lire et filtrer les articles du corpus RSS
    articles = filter_rss_source(dossier)

    # Afficher les articles uniques
    for article in articles:
        print(f"Titre : {article['title']}")
        print(f"Date : {article['pub_date']}")
        print(f"Description : {article['description']}")
        print(f"Category : {', '.join(article['category']) if article['category'] else 'No Category'}")  
        print(f"Source : {article['source']}")
        print("---")


# Adaptation de `main()` pour accepter un dossier en argument
def main():
    if len(sys.argv) != 2:
        print("Utilisation : python rss_reader.py <chemin_du_dossier>")
        sys.exit(1)

    dossier = sys.argv[1]
    arborescence_rss_etree(dossier)


# Vérifie si le script est exécuté directement (et non importé comme module)
if __name__ == "__main__":
    main()

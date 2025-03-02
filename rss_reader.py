## R2 ##
#extrait les métadonnées en utilisant ElementTree

import xml.etree.ElementTree as ET  #importe le module ElementTree pour analyser les fichiers XML
from pathlib import Path
import sys  #importe le module sys pour gérer les arguments de la ligne de commande
import re #nettoyer le texte


def rss_reader_etree(filename: str | Path) -> list[dict]:
    name = Path(filename).name  # Récupère juste le nom du fichier
     # Éviter les fichiers problématiques
    if name.lower() in ("flux.xml", "flux rss.xml"):
        return []
    try: 
        root = ET.parse(filename).getroot()  #récupère l'élément racine du fichier XML
    except ET.ParseError:
        return []

    articles = []  #initialise une liste pour stocker les articles extraits
    #récupérer les catégories générales du flux
    global_categories = set(element.text.strip() for element in root.iterfind("./channel/category") if element.text)
        
         # Vérifier chaque élément avec "is None"
    for item in root.iterfind(".//item"):
        guid_element = item.find("guid")
        dataid = guid_element.text if guid_element is not None else "No ID"
            
        #extrait le titre, ou met "No Title" et nettoyer
        title_element = item.find("title")
        title = nettoyage(title_element.text) if title_element is not None else "No Title"
    
        #extrait la description, ou met "No Description" 
        description_element = item.find("description") 
        #et nettoyer description avec regex
        #description = re.sub(r'<.*?>', '', description).strip() if description else "No Description" 
        #nettoyer avec fonction
        description = nettoyage(description_element.text) if description_element is not None else "No Description"
  

        #extrait la date de publication, ou met "No Date" si la balise est absente
        pubdate_element = item.find("pubDate") or item.find("lastpublished")
        pubdate = nettoyage(pubdate_element.text) if pubdate_element is not None else "No Date"

        #extraire les catégories (globales + locales)
        local_categories = global_categories.copy()
        for category_element in item.iterfind("category"):
            if category_element.text:  #s'il y a des catégories
                local_categories.add(category_element.text.strip())  #réunir en une chaîne


        #ajoute l'article extrait sous forme de dictionnaire dans la liste
        article = {
            "id": dataid,
            "source": name,
            "title": title,
            "description": description,
            "pub_date": pub_date,
            "category": sorted(local_categories),
            }
            
        articles.append(article)
            

    return articles  #retourne la liste des articles extraits

#permet d’appeler méthode depuis bash
def main():
    #vérifie si un argument (le chemin du fichier XML) a été fourni
    if len(sys.argv) != 2:
        print("Utilisation : python rss_reader.py <chemin_du_fichier_rss>")
        sys.exit(1)  #quitte le programme si le fichier XML n'est pas spécifié

    file_path = sys.argv[1]  #récupère le chemin du fichier XML depuis la ligne de commande
    articles = rss_reader_etree(file_path)  #exécute la fonction de parsing RSS

    #affiche les articles extraits
    for article in articles:
        print(f"Titre : {article['title']}")  #affiche titre de l'article
        print(f"Date : {article['pub_date']}")  #affiche date de publication
        print(f"Description : {article['description']}")  #affiche titre de l'article
        print(f"Category : {', '.join(article['category'])}")  #affiche category de l'article
        print("---")  #séparateur entre les articles

#vérifie si le script est exécuté directement (et non importé comme module)
if __name__ == "__main__":
    main()  #appelle la fonction principale pour exécuter le script

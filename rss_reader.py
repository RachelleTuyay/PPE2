import argparse  #pour gérer les arguments en ligne de commande
import re  #pour les expressions régulières
import xml.etree.ElementTree as ET  #importe le module ElementTree pour analyser les fichiers XML
from pathlib import Path
import sys  #importe le module sys pour gérer les arguments de la ligne de commande

import html  #pour html.unescape()
import feedparser

def nettoyage(texte):
    texte_net = re.sub(r"<!\[CDATA\[(.+)\]\]>", r"\1", texte, flags=re.DOTALL)
    #suppression des tags HTML
    texte_net = re.sub(r"<.+?>", "", texte_net)
    texte_net = html.unescape(texte_net)
    #suppression des retours à la ligne
    texte_net = re.sub(r"\n+", " ", texte_net)
    
    #suppression des espaces multiples
    texte_net = texte_net.strip()
    return texte_net

## Fonctions de lecture RSS avec différentes méthodes ##

#fonction utilisant regex
#R1#
def rss_reader_re(filename):
    print(f"Lecture RSS avec regex : {filename}")
    return []

#fonction utilisant etree
#R2#
#extrait les métadonnées en utilisant ElementTree

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
        
    #vérifier chaque élément avec "is None"
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
        pubdate_element = item.find("pubDate") or item.find("lastpublished") or None
        pubdate = nettoyage(pubdate_element.text) if pubdate_element is not None else "No Date"

        #extraire les catégories (globales + locales)
        local_categories = global_categories.copy()
        for category_element in item.iterfind("category"):
            if category_element.text:  #s'il y a des catégories
                local_categories.add(category_element.text.strip())  #chaine


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


#fonction utilisant feedparser
#R3#
def rss_reader_feedparser(filename):
    print(f"Lecture RSS avec feedparser : {filename}")
    return []

## Fonction principale ##

#création de l'argument parser pour appeler méthode depuis bash
def main():
    parser = argparse.ArgumentParser(description="Lire un fichier RSS avec une méthode spécifiée")
    #argument pour choisir la méthode de parsing RSS
    parser.add_argument("methode", choices=["re", "etree", "feedparser"], help="Méthode de parsing RSS")
     #argument pour indiquer le fichier RSS à lire
    parser.add_argument("fichier_rss", help="Le fichier RSS d'entrée")

#récupération des arguments passés en ligne de commande
    args = parser.parse_args()

 #appelle la fonction correspondant à la méthode choisie
    if args.methode == "re":
        items = rss_reader_re(args.fichier_rss)
    elif args.methode == "etree":
        items = rss_reader_etree(args.fichier_rss)
    elif args.methode == "feedparser":
        items = rss_reader_feedparser(args.fichier_rss)
    else:
        raise ValueError("Méthode inconnue")

#affichage des éléments récupérés
    for article in items:
        print(f"Titre : {article['title']}")
        print(f"Date : {article['pub_date']}")
        print(f"Description : {article['description']}")
        print(f"Category : {', '.join(article['category'])}")  
        #print(f"Category : {', '.join(list(article['category'])) if article['category'] else 'No Category'}" #set to list
        print("---")  

#vérifie si le script est exécuté directement (et non importé comme module)
if __name__ == "__main__":
    main() #appelle la fonction principale pour exécuter le script

## R2 ##
#extrait les métadonnées en utilisant ElementTree

import xml.etree.ElementTree as ET  #importe le module ElementTree pour analyser les fichiers XML
import sys  #importe le module sys pour gérer les arguments de la ligne de commande

def parse_rss_etree(file_path):
    try:
        #charge et analyse le fichier XML
        tree = ET.parse(file_path)  
        root = tree.getroot()  #récupère l'élément racine du fichier XML
        
        #trouver le nœud <channel> qui contient les articles
        channel = root.find("channel")
        if channel is None:
            #si la balise <channel> est absente, une erreur est levée
            raise ValueError("Structure RSS invalide : balise <channel> manquante.")

        articles = []  #initialise une liste pour stocker les articles extraits
        
        #parcourt toutes les balises <item> qui représentent des articles pour les récupérer
        for item in channel.findall("item"):
            id = item.find("guid").text 
            source = file_path 
            #extrait le titre, ou met "No Title" si la balise est absente
            title = item.find("title").text 
            #extrait la description, ou met "No Description" si la balise est absente
            description = item.find("description").text  
            #extrait la date de publication, ou met "No Date" si la balise est absente
            pub_date = item.find("pubDate").text
            category = item.findall("category") if item.findall("category") is not None else "[]"

            #ajoute l'article extrait sous forme de dictionnaire dans la liste
            articles.append({
                "id": id,
                "source": source,
                "title": title,
                "description": description,
                "pub_date": pub_date,
                "category": category
            })

        return articles  #retourne la liste des articles extraits

    except ET.ParseError:
        #gère l'erreur si le fichier XML est invalide
        print(f"Erreur: Impossible d'analyser le fichier {file_path}. Vérifiez que c'est un fichier XML valide.")
        return []  #retourne une liste vide en cas d'erreur

#permet d’appeler méthode depuis bash
def main():
    #vérifie si un argument (le chemin du fichier XML) a été fourni
    if len(sys.argv) != 2:
        print("Utilisation : python rss_reader.py <chemin_du_fichier_rss>")
        sys.exit(1)  #quitte le programme si le fichier XML n'est pas spécifié

    file_path = sys.argv[1]  #récupère le chemin du fichier XML depuis la ligne de commande
    articles = parse_rss_etree(file_path)  #exécute la fonction de parsing RSS

    #affiche les articles extraits
    for article in articles:
        print(f"ID : {article['id']}")  #affiche id de l'article
        print(f"Source : {article['source']}")  #affiche source de l'article
        print(f"Titre : {article['title']}")  #affiche titre de l'article
        print(f"Date : {article['pub_date']}")  #affiche date de publication
        print(f"Description : {article['description']}")  #affiche titre de l'article
        print(f"Category : {article['category']}")  #affiche category de l'article
        print("---")  #séparateur entre les articles

#vérifie si le script est exécuté directement (et non importé comme module)
if __name__ == "__main__":
    main()  #appelle la fonction principale pour exécuter le script

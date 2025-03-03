import xml.etree.ElementTree as ET  #importe le module ElementTree pour analyser les fichiers XML
from pathlib import Path
import sys  #importe le module sys pour gérer les arguments de la ligne de commande

#R2#
#ire et afficher tous les fichiers XML dans un dossier avec pathlib.glob()

def arborescence_rss_etree(dossier):
    path = Path(dossier)
    
    if not path.exists():
        print(f"Erreur : le dossier {dossier} n'existe pas.")
        return
    
    #recherche de tous les fichiers XML dans l'arborescence
    fichiers_xml = path.glob("**/*.xml")
    
    for fichier in fichiers_xml:
        print(f"Lecture du fichier : {fichier}")
        #lire les articles du fichier XML
        items = rss_reader_etree(fichier)
        
        
        #affichage des éléments récupérés
        for article in items:
            print(f"Titre : {article['title']}")
            print(f"Date : {article['pub_date']}")
            print(f"Description : {article['description']}")
            print(f"Category : {', '.join(article['category'])}")  
            #print(f"Category : {', '.join(list(article['category'])) if article['category'] else 'No Category'}" #set to list
            print("---") 

#adaptation de main() pour accepter un dossier en argument
def main():
    if len(sys.argv) != 2:
        print("Utilisation : python rss_reader.py <chemin_du_dossier>")
        sys.exit(1)

    dossier = sys.argv[1]
    arborescence_rss_etree(dossier)


#vérifie si le script est exécuté directement (et non importé comme module)
if __name__ == "__main__":
    main() #appelle la fonction principale pour exécuter le script

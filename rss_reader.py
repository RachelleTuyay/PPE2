import argparse  #pour gérer les arguments en ligne de commande
import re  #pour les expressions régulières

#suppression de <![CDATA[...]]>
#texte_net = re.sub(r"<!\[CDATA\[(.+)\]\]>", r"\1", texte, flags=re.DOTALL)

#suppression des balises HTML
#texte_net = re.sub(r"<[^>]+>", "", texte_net)

#suppression des retours à la ligne
#texte_net = re.sub(r"\n", " ", texte_net)
 
#suppression des espaces multiples
#texte_net = re.sub(r"\s+", " ", texte_net).strip()

## Fonctions de lecture RSS avec différentes méthodes ##

#fonction utilisant etree 
def lire_rss_etree(fichier):
    print(f"Lecture RSS avec etree : {fichier}")
    return []

#fonction utilisant regex
def lire_rss_re(fichier):
    print(f"Lecture RSS avec regex : {fichier}")
    return []

#fonction utilisant feedparser
def lire_rss_feedparser(fichier):
    print(f"Lecture RSS avec feedparser : {fichier}")
    return []

## Fonction principale ##

#création de l'argument parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lire un fichier RSS avec une méthode spécifiée")
    #argument pour choisir la méthode de parsing RSS
    parser.add_argument("methode", choices=["re", "etree", "feedparser"], help="Méthode de parsing RSS")
     #argument pour indiquer le fichier RSS à lire
    parser.add_argument("fichier_rss", help="Le fichier RSS d'entrée")

#récupération des arguments passés en ligne de commande
    args = parser.parse_args()

 #appelle la fonction correspondant à la méthode choisie
    if args.methode == "re":
        items = lire_rss_re(args.fichier_rss)
    elif args.methode == "etree":
        items = lire_rss_etree(args.fichier_rss)
    elif args.methode == "feedparser":
        items = lire_rss_feedparser(args.fichier_rss)
    else:
        raise ValueError("Méthode inconnue")

#affichage des éléments récupérés
    for item in items:
        print(item)

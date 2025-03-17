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
	fichiers_xml = list(dir.glob('**/*.xml'))
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

def run_method(method, lecture, dossier_entree):
	"""Appelle la méthode sélectionnée avec les fichiers XML"""
	lire_func = {"glob": lire_corpus_glob, "os": lire_corpus_os, "path": lire_corpus_path}
	
	if lecture not in lire_func:
		print("Erreur : Méthode de lecture invalide. Utilisez 'glob', 'os' ou 'path'.")
		sys.exit(1)
		
	xml_files = lire_func[lecture](dossier_entree)
	print(f"Nombre de fichiers XML trouvés: {len(xml_files)}")

	method_func = {"etree": rss_reader.lire_rss_etree, "feedparser": rss_reader.lire_rss_feedparser}
	
	if method not in method_func:
		print("Erreur : Méthode d'extraction invalide. Utilisez 'etree' ou 'feedparser'.")
		sys.exit(1)

	all_articles = []
	for file in xml_files:
		try:
			articles = method_func[method](file)
			all_articles.extend(articles)
			print(f"Fichier traité: {file} - {len(articles)} articles extraits")
		except Exception as e:
			print(f"Impossible de traiter le fichier {file}, erreur: {e}")

	return all_articles

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
	parser.add_argument("--output", "-o", help="Fichier de sortie (format: json, xml, ou pickle)", default="output.json")
	args = parser.parse_args()

	if not os.path.isdir(args.dossier_entree):
		print(f"Erreur : Le dossier '{args.dossier_entree}' n'existe pas.")
		sys.exit(1)

	# Collecter tous les articles
	articles = run_method(args.method, args.lecture, args.dossier_entree)
	print(f"Total des articles collectés: {len(articles)}")
	
	# Créer le corpus
	corpus = Corpus(articles)
	
	# Appliquer les filtres si nécessaire
	if args.start_date or args.end_date or args.source or args.categorie:
		articles_filtres = rss_reader.filtrage(articles, args.start_date, args.end_date, args.source, args.categorie)
		corpus = Corpus(articles_filtres)
		print(f"Articles après filtrage: {len(articles_filtres)}")
	
	# Sérialiser le résultat
	output_format = os.path.splitext(args.output)[1][1:].lower() if '.' in args.output else 'json'
	
	if output_format == 'json':
		corpus.save_json(args.output)
	elif output_format == 'xml':
		corpus.save_xml(args.output)
	elif output_format in ['pkl', 'pickle']:
		corpus.save_pickle(args.output)
	else:
		print(f"Format de sortie non pris en charge: {output_format}. Utilisation de JSON par défaut.")
		corpus.save_json(args.output)
		
	print(f"Traitement terminé. {len(corpus.articles)} articles ont été écrits dans {args.output}")

if __name__ == "__main__":
	main()
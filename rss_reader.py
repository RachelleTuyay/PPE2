import os
import sys
import argparse
import re
import xml.etree.ElementTree as ET
import feedparser
from pathlib import Path
from datetime import datetime

def lire_corpus_glob(dossier_entree) :
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
	"""Fonction pour trouver des fichiers XML et les traiter"""
	path_to_files = Path(dossier_entree)
	xml_files = []

	if not path_to_files.exists():
		print("Le chemin n'est pas valide.")
		return

	if not path_to_files.is_dir():
		print("Ce n'est pas un dossier, veuillez réessayer avec un autre chemin.")
		return

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


def lire_rss_regex(xml_file):
	"""Méthode R1 : Extraction avec expressions régulières (Regex)"""

	articles = []

	with open(xml_file, 'r', encoding="utf-8") as file:
		content = file.read()

	items = re.findall(r'<item>([\s\S]*?)</item>', content)

	for item in items:
		id_match = re.search(r'<link>(.*?)</link>', item)
		title_match = re.search(r'<title>(.*?)</title>', item)
		desc_match = re.search(r'<description>(.*?)</description>', item)
		date_match = re.search(r'<pubDate>(.*?)</pubDate>', item)
		categories = re.findall(r'<category[^>]*>(.*?)</category>', item)

		id_value = id_match.group(1) if id_match else " "
		title_value = title_match.group(1) if title_match else " "
		desc_value = desc_match.group(1) if desc_match else " "
		date_value = date_match.group(1) if date_match else " "
		categories_value = [", ".join(categories)] if categories else "[]"

		article = {'id': id_value, 'source': str(xml_file), 'title' : title_value, 'description': desc_value, 'date' : date_value, 'categories': categories_value}
		articles.append(article)

	return articles

def lire_rss_etree(xml_file):
	"""Méthode R2 : Extraction avec ElementTree"""

	articles = []
	tree = ET.parse(xml_file)
	root = tree.getroot()


	for item in root.iter("item"):
		id = item.find("link").text if item.find("link") is not None else " "
		categories = [category.text for category in item.findall("category") if category.text]
		if categories == [] :
			for channel in root.iter("channel") :
				for category in channel.findall("category") :
					categories.append(category.text)
		description = item.find("description").text if item.find("description") is not None else " "
		title = item.find("title").text if item.find("title") is not None else " "
		date = item.find("pubDate").text if item.find("pubDate") is not None else " "

		article = {'id': id,  'source' : str(xml_file), 'title': title, 'description': description, 'date' : date, 'categories': categories}
		articles.append(article)

	return articles

def lire_rss_feedparser(xml_file):
	"""Méthode R3 : Extraction avec feedparser"""

	articles = []
	flux = feedparser.parse(xml_file)

	for entry in flux.entries:
		categories = [tag.term for tag in entry.tags] if "tags" in entry else []
		categories_lst = [{', '.join(f'\"{c}\"' for c in categories)}] if categories else "[]"

		article = {'id': entry.link, 'source': str(xml_file), 'title': entry.title, 'description': entry.summary, 'date' : entry.published, 'categories': categories_lst}
		articles.append(article)
		
	return articles

def run_method(method, lecture, dossier_entree):
	"""Appelle la méthode sélectionnée avec le fichier XML"""

	lire_func = {"glob" : lire_corpus_glob, "os" : lire_corpus_os, "path" : lire_corpus_path}
	xml_files = lire_func[lecture](dossier_entree)

	method_func = {"regex" : lire_rss_regex, "etree" : lire_rss_etree, "feedparser" : lire_rss_feedparser}
	if method not in method_func:
		print("Erreur : Méthode invalide. Utilisez 'regex', 'etree' ou 'feedparser'.")
		sys.exit(1)

	articles_total = []
	for file in xml_files:
		try:
			articles = method_func[method](file)
			articles_total.extend(articles)
		except:
			print(f"Impossible de traiter le fichier {file}, fichier XML mal formé")

	return articles_total

def filtre_date(item:dict, date_debut, date_fin):
    """
    Filtrer les articles par date
    """
    # Analyser la date (si elle existe)
    if item.get("date") != " ":
        try:
            date = datetime.strptime(item.get("date"), "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
        except ValueError:
            date = None  # Si l'analyse échoue, définir sur None
    
    if date is None:  
        return True  # Si aucune date, conserver par défaut (peut être changé en False pour exclure)

    if date_debut and date < datetime.strptime(date_debut, "%Y-%m-%d"):
        return False

    if date_fin and date > datetime.strptime(date_fin, "%Y-%m-%d"):
        return False
    
    return True

def filtre_source(item:dict, sources:list) :
	item_source = item.get("source", []).lower()

	for s in sources :
		if s.lower() in item_source :
			return True
		else:
			return False

def filtre_categories(item:dict, categories:list) :
	"""
	filtrer les articles selon catégories
	"""
	if not categories:
		return True
	# On découpe le string du categorie par "," et le stoker dans une list
	article_categories = item.get("categories")
	article_categories = [cat.strip() for items in article_categories for cat in items.split(",")]
	
	if article_categories:
		print(any(cat in categories for cat in article_categories))
		return any(cat in categories for cat in article_categories)
	return False  # Si pas de catégories, on exclut par défaut

def filtrage(filtres, articles):
	articles_filtres = []
	id_unique = set()
	for item in articles :
		keep_item = True
		for f in filtres :
			if not f(item) :
				keep_item = False
				break
		if keep_item :
			id = item.get("id")
			if id not in id_unique :				
				id_unique.add(id)
				articles_filtres.append(item)
	
	return articles_filtres

def main():
	"""Gère l'entrée utilisateur avec des arguments Bash"""
	parser = argparse.ArgumentParser(description="Analyseur RSS avec trois méthodes différentes.")
	parser.add_argument("dossier_entree", help="Dossier comprenant les fichiers XML d'entrée")
	parser.add_argument("lecture", choices=["glob","os","path"], help="Choisir le module utilisé pour lire le dossier d'entrée")
	parser.add_argument("method", choices=["regex", "etree", "feedparser"], help="Méthode d'extraction (r1, r2, r3)")
	parser.add_argument("--start-date", help="Filtrer les articles publiés après cette date (format YYYY-MM-DD)")
	parser.add_argument("--end-date", help="Filtrer les articles publiés avant cette date (format YYYY-MM-DD)")
	parser.add_argument("--source", nargs="+", help="Filtrer par une ou plusieurs sources")
	parser.add_argument("--categorie", nargs="+", help="Filtrer par une ou plisieurs catégories")
	args = parser.parse_args()

	if not os.path.isdir(args.dossier_entree):
		print(f"Erreur : Le dossier '{args.dossier_entree}' n'existe pas.")
		sys.exit(1)

	articles = run_method(args.method, args.lecture, args.dossier_entree)


	filtres = []
	if args.start_date or args.end_date :
		filtres.append(lambda item: filtre_date(item, args.start_date, args.end_date))
	if args.source :
		filtres.append(lambda item: filtre_source(item, args.source))
	if args.categorie :
		filtres.append(lambda item: filtre_categories(item, args.categorie))

	if filtres :
		articles_filtres = filtrage(filtres, articles)
		with open("output.txt", "w") as f:
			for article in articles_filtres :
				f.write(f'id: {article.get('id','')}\n')
				f.write(f'source: {article.get('source','')}\n')
				f.write(f'title: {article.get('title','')}\n')
				f.write(f'description: {article.get('description','')}\n')
				f.write(f'date: {article.get('date','')}\n')
				f.write(f'categories: {article.get('categories', [])}\n')
				f.write('\n')

	else : 
		with open("output.txt", "w") as f:
			for article in articles :
				f.write(f'id: {article.get('id','')}\n')
				f.write(f'source: {article.get('source','')}\n')
				f.write(f'title: {article.get('title','')}\n')
				f.write(f'description: {article.get('description','')}\n')
				f.write(f'date: {article.get('date','')}\n')
				f.write(f'categories: {article.get('categories', [])}\n')
				f.write('\n')


if __name__ == "__main__":
	main() 

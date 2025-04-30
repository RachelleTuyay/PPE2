import os
import sys
import argparse
import re
import xml.etree.ElementTree as ET
import feedparser
from pathlib import Path
from datetime import datetime
from datastructures import Article, Corpus

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

		#article = {'id': id_value, 'source': str(xml_file), 'title' : title_value, 'description': desc_value, 'date' : date_value, 'categories': categories_value}
		article = Article(
			id=id_value,
			source=os.path.basename(xml_file),
			title=title_value,
			description=desc_value,
			date=date_value,
			categories=categories_value
		)
		
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
		description = item.find("description").text if item.find("description") is not None else ""
		if description is None :
			description = ""
		title = item.find("title").text if item.find("title") is not None else " "
		date = item.find("pubDate").text if item.find("pubDate") is not None else " "

		#article = {'id': id,  'source' : str(xml_file), 'title': title, 'description': description, 'date' : date, 'categories': categories}
		article = Article(
			id=id,
			source=os.path.basename(xml_file),
			title=title,
			description=description,
			date=date,
			categories=categories
		)
		
		articles.append(article)
	return articles

def lire_rss_feedparser(xml_file):
	"""Méthode R3 : Extraction avec feedparser"""

	articles = []
	flux = feedparser.parse(xml_file)

	for entry in flux.entries:
		categories = [tag.term for tag in entry.tags] if "tags" in entry else []
		categories_lst = [{', '.join(f'\"{c}\"' for c in categories)}] if categories else "[]"

		#article = {'id': entry.link, 'source': str(xml_file), 'title': entry.title, 'description': entry.summary, 'date' : entry.published, 'categories': categories_lst}
		article = Article(
			id=entry.link if 'link' in entry else "",
			source=os.path.basename(xml_file),
			title=entry.title if 'title' in entry else "",
			description=entry.summary if 'summary' in entry else "",
			date=entry.published if 'published' in entry else "",
			categories=categories_lst
		)
		articles.append(article)
		
	return articles

def run_method(method, xml_file):
	"""Appelle la méthode sélectionnée avec le fichier XML"""

	method_func = {"regex" : lire_rss_regex, "etree" : lire_rss_etree, "feedparser" : lire_rss_feedparser}
	if method not in method_func:
		print("Erreur : Méthode invalide. Utilisez 'regex', 'etree' ou 'feedparser'.")
		sys.exit(1)

	try:
		articles = method_func[method](xml_file)
	except:
		print(f"Impossible de traiter le fichier {xml_file}, fichier XML mal formé")

	return articles


def filtre_date(item:Article, date_debut, date_fin):
	"""
	Filtrer les articles par date
	"""
	# Analyser la date (si elle existe)
	if not item.date or not item.date.strip() :
		return False
		
	try:
		date = datetime.strptime(item.date, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
	except ValueError:
		return False


	if date_debut :
		date_min = datetime.strptime(date_debut, "%Y-%m-%d")
		if date < date_min :
			return False

	if date_fin :
		date_max = datetime.strptime(date_fin, "%Y-%m-%d")
		if date > date_max :
			return False
	
	return True

def filtre_source(item:Article, sources:list) :
	item_source = item.source.lower()

	if not sources:
		return True
	
	return any(s.lower() in item_source for s in sources)

def filtre_categories(item:Article, categories:list) :
	"""
	filtrer les articles selon catégories
	"""
	if not categories:
		return True
	# On découpe le string du categorie par "," et le stoker dans une list
	if len(item.categories) == 1 :
		article_categories = item.categories[0].split(", ")
	else :
		article_categories = item.categories

	if article_categories:
		return any(cat in categories for cat in article_categories)
	return False  # Si pas de catégories, on exclut par défaut

def filtrage(articles, date_debut=None, date_fin=None, sources=None, categories=None):
	"""Applique tous les filtres spécifiés aux articles"""
	articles_filtres = []
	id_unique = set()
	
	for article in articles:
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
	
	return articles_filtres

def main():
	"""Gère l'entrée utilisateur avec des arguments Bash"""
	parser = argparse.ArgumentParser(description="Analyseur RSS avec deux méthodes différentes.")
	parser.add_argument("fichier_entree", help="Fichier XML d'entrée")
	parser.add_argument("method", choices=["regex", "etree", "feedparser"], 
						help="Méthode d'extraction (regex, etree, feedparser)")
	parser.add_argument("--start-date", help="Filtrer les articles publiés après cette date (format YYYY-MM-DD)")
	parser.add_argument("--end-date", help="Filtrer les articles publiés avant cette date (format YYYY-MM-DD)")
	parser.add_argument("--source", nargs="+", help="Filtrer par une ou plusieurs sources")
	parser.add_argument("--categorie", nargs="+", help="Filtrer par une ou plusieurs catégories")
	parser.add_argument("--output", "-o", help="Fichier de sortie (format: json, xml, ou pickle)", default="output.json")
	args = parser.parse_args()

	if not os.path.isfile(args.fichier_entree):
		print(f"Erreur : Le fichier '{args.fichier_entree}' n'existe pas.")
		sys.exit(1)

	articles = run_method(args.method, args.fichier_entree)
	
	# Appliquer les filtres si nécessaire
	if args.start_date or args.end_date or args.source or args.categorie:
		articles_filtres = filtrage(articles, args.start_date, args.end_date, args.source, args.categorie)
	else:
		articles_filtres = articles
	
	corpus = Corpus(articles_filtres)
	
	# Déterminer le format de sortie à partir de l'extension du fichier
	output_format = args.output.split(".")[-1].lower()
	
	if output_format == 'json':
		corpus.save_json(args.output)
	elif output_format == 'xml':
		corpus.save_xml(args.output)
	elif output_format in ['pkl', 'pickle']:
		corpus.save_pickle(args.output)
	else:  # Par défaut, utiliser le format json
		corpus.save_json(args.output)
		
	print(f"Traitement terminé. {len(corpus.articles)} articles ont été écrits dans {args.output}")

if __name__ == "__main__":
	main()
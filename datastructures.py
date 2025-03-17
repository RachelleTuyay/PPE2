from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
import json

@dataclass
class Article:
	id: str
	source: str
	title: str
	description: str
	date: str
	categories: List[str] = field(default_factory=list)
	
	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> 'Article':
		"""Crée un Article à partir d'un dictionnaire"""
		return cls(
			id=data.get('id', ''),
			source=data.get('source', ''),
			title=data.get('title', ''),
			description=data.get('description', ''),
			date=data.get('date', ''),
			categories=data.get('categories', [])
		)
	
	def to_dict(self) -> Dict[str, Any]:
		"""Convertit l'Article en dictionnaire"""
		return {
			'id': self.id,
			'source': self.source,
			'title': self.title,
			'description': self.description,
			'date': self.date,
			'categories': self.categories
		}

@dataclass
class Corpus:
	articles: List[Dict[str, Any]] = field(default_factory=list)

	@classmethod
	def load_json(cls, input_file: Path):
		"""Charge un corpus depuis un fichier JSON"""
		try:
			with open(input_file, 'r', encoding='utf-8') as f:
				data = json.load(f)
			
			articles = [Article.from_dict(article_data) for article_data in data]
			return cls(articles)
		except Exception as e:
			print(f"Erreur lors du chargement du fichier JSON: {e}")
			return cls([])

	def save_json(self, output_file: Path) -> None:
		"""Sauvegarde le corpus dans un fichier JSON"""
		try:
			articles_dict = [article.to_dict() for article in self.articles]
			with open(output_file, 'w', encoding='utf-8') as f:
				json.dump(articles_dict, f, ensure_ascii=False, indent=4)
			print(f"Corpus sauvegardé dans {output_file}")
		except Exception as e:
			print(f"Erreur lors de la sauvegarde en JSON: {e}")

	def load_xml(input_file: Path):
		pass

	def save_xml(self, output_file: Path) -> None:
		pass

	def load_pickle(input_file: Path):
		pass

	def save_pickle(self, output_file: Path) -> None:
		pass

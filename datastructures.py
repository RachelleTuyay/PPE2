from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import xml.etree.ElementTree as ET
import pickle
import json
import argparse

@dataclass
class Token:
    """Common interface for tokens from different analyzers"""
    text: str
    lemma: Optional[str] = None
    pos: Optional[str] = None
    
    def to_dict(self):
        """Convert token to dictionary for serialization"""
        return {
            'text': self.text,
            'lemma': self.lemma,
            'pos': self.pos
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Token from dictionary"""
        return cls(
            text=data.get('text', ''),
            lemma=data.get('lemma'),
            pos=data.get('pos')
        )


@dataclass
class Article:
    id: str
    source: str
    title: str
    description: str
    date: str
    categories: List[str] = field(default_factory=list)
    tokens: list[list[Token]] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Article':
        """Crée un Article à partir d'un dictionnaire"""
        tokens = []
        if 'tokens' in data and isinstance(data['tokens'], list):
            tokens = [Token.from_dict(token_data) for token_data in data['tokens']]

        return cls(
            id=data.get('id', ''),
            source=data.get('source', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            date=data.get('date', ''),
            categories=data.get('categories', []),
            tokens=tokens
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'Article en dictionnaire"""
        return {
            'id': self.id,
            'source': self.source,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'categories': self.categories,
            'tokens': [token.to_dict() for token in self.tokens] if self.tokens else []
        }

@dataclass
class Corpus:
    articles: list[Article] = field(default_factory=list)

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

    @classmethod
    def load_xml(cls, input_file: Path):
        tree = ET.parse(input_file)
        root = tree.getroot()

        articles = []
        for article_elem in root.findall("article"):
            article_data = {}

            for child in article_elem:
                if child.tag == "tokens" and len(child) > 0:
                    article_data["tokens"] = []
                    for token_elem in child.findall("item"):
                        token_data = {}
                        for token_attr in token_elem:
                            token_data[token_attr.tag] = token_attr.text
                        article_data["tokens"].append(token_data)
                elif len(child) > 0:  # Si c'est une liste (ex. categories)
                    article_data[child.tag] = [item.text for item in child.findall("item")]
                else:
                    article_data[child.tag] = child.text

            articles.append(Article.from_dict(article_data))

        return cls(articles)

    def save_xml(self, output_file: Path) -> None:
        """Sauvegarde le Corpus en XML"""
        root = ET.Element("articles")  # créer le root

        for article in self.articles:
            article_elem = ET.SubElement(root, "article")
            article_dict = article.to_dict()
            
            for key, value in article_dict.items():
                if key == "tokens" and value:
                    # Traitement spécial pour les tokens
                    tokens_elem = ET.SubElement(article_elem, "tokens")
                    for token in value:
                        token_elem = ET.SubElement(tokens_elem, "item")
                        for token_key, token_value in token.items():
                            if token_value is not None:  # Ne pas ajouter les attributs None
                                token_attr = ET.SubElement(token_elem, token_key)
                                token_attr.text = str(token_value)
                elif isinstance(value, list):  # Si c'est une liste (catégories)
                    list_elem = ET.SubElement(article_elem, key)
                    for item in value:
                        item_elem = ET.SubElement(list_elem, "item")
                        item_elem.text = str(item)
                else:
                    sub_elem = ET.SubElement(article_elem, key)
                    sub_elem.text = str(value) if value is not None else ""
                
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)


    @classmethod
    def load_pickle(cls, input_file: Path):
        try:
            with open(input_file, 'rb') as f:
                loaded_corpus = pickle.load(f)
                # S'assurer que c'est un objet Corpus
                if isinstance(loaded_corpus, Corpus):
                    return loaded_corpus
                # Sinon, reconstruire un objet Corpus
                elif isinstance(loaded_corpus, list):
                    articles = [
                        Article.from_dict(article) if isinstance(article, dict) else article 
                        for article in loaded_corpus
                    ]
                    return cls(articles)
                else:
                    print("Format de données pickle non reconnu")
                    return cls([])
        except Exception as e:
            print(f"Erreur lors du chargement du fichier pickle: {e}")
            return cls([])

    def save_pickle(self, output_file: Path) -> None:
        """Sauvegarde le corpus dans un fichier pickle"""
        try:
            with open(output_file, 'wb') as f:
                pickle.dump(self, f)
            print(f"Corpus sauvegardé dans {output_file}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde en pickle: {e}")


name_to_saver = {
    "xml": Corpus.save_xml,
    "json": Corpus.save_json,
    "pickle": Corpus.save_pickle
}

name_to_loader = {
    "xml": Corpus.load_xml,
    "json": Corpus.load_json,
    "pickle": Corpus.load_pickle
}


def main(input_file, output_file, loader, saver) :

    Corpus.load = name_to_loader[loader]
    Corpus.save = name_to_saver[saver]


    corpus = Corpus.load(input_file)
    corpus.save(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("(de)serialize some RSS data.")

    parser.add_argument("input_file", help="input serialized RSS file")
    parser.add_argument("output_file", help="output serialized RSS file")
    parser.add_argument("-l", "--loader", choices=("xml", "json", "pickle"), required=True)
    parser.add_argument("-s", "--saver", choices=("xml", "json", "pickle"), required=True)

    args = parser.parse_args()

    main(args.input_file, args.output_file, args.loader, args.saver)

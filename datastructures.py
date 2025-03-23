from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path
import xml.etree.ElementTree as ET
import pickle
import json

@dataclass
class Token:
    text: str         # sa forme
    lemma: str        # son lemme
    pos: str          # sa partie du discours (part of speech, POS, ou catégorie grammaticale).

@dataclass
class Article:
    id: str
    source: str
    title: str
    description: str
    date: str
    categories: List[str] = field(default_factory=list)
    
    # Pour stocker le resultat de analyser
    title_tokens: Optional[List[Token]] = None
    description_tokens: Optional[List[Token]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Article':
        """Crée un Article à partir d'un dictionnaire"""
        return cls(
            id=data.get('id', ''),
            source=data.get('source', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            date=data.get('date', ''),
            categories=data.get('categories', []),

            title_tokens=[Token(**t) for t in data.get('title_tokens', [])] if data.get('title_tokens') else None,
            description_tokens=[Token(**t) for t in data.get('description_tokens', [])] if data.get('description_tokens') else None,
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
            
            'title_tokens': [asdict(t) for t in self.title_tokens] if self.title_tokens else None,
            'description_tokens': [asdict(t) for t in self.description_tokens] if self.description_tokens else None
        }

@dataclass
class Corpus:
    articles: List[Article] = field(default_factory=list)

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
        tree = ET.parse(input_file)
        root = tree.getroot()

        articles = []
        for article_elem in root.findall("article"):
            article = {}

            for child in article_elem:
                if child.tag in ("title_tokens", "description_tokens"): # Si c'est tokens
                    token_list = []
                    for token_elem in child.findall("token"):
                        token_dict = {}
                        for attr in token_elem:
                            token_dict[attr.tag] = attr.text
                        token_list.append(token_dict)
                    article[child.tag] = token_list
                elif len(child) > 0:  # Si c'est une list de categorie
                    article[child.tag] = [item.text for item in child.findall("item")]
                else:
                    article[child.tag] = child.text

            articles.append(article)

        return Corpus([Article.from_dict(a) for a in articles])

    def save_xml(self, output_file: Path) -> None:
        """Sauvgarder le Corpus en xml"""
        root = ET.Element("articles")  # creer le root

        for article in self.articles:  # parcourir chaque article dans le corpus
                article_elem = ET.SubElement(root, "article")  # creer la balise <article> qui contient chanque article
                for key, value in article.to_dict().items():
                    if isinstance(value, list):  
                        if key in ("title_tokens", "description_tokens"):   # Si c'est tokens
                            tokens_elem = ET.SubElement(article_elem, key)
                            for token in value:
                                token_elem = ET.SubElement(tokens_elem, "token")
                                for t_key, t_val in token.items():
                                    sub = ET.SubElement(token_elem, t_key)
                                    sub.text = str(t_val)
                        else:   # Si c'est une list de categorie
                            list_elem = ET.SubElement(article_elem, key)  # creer la balise de liste (categorie)
                            for item in value:
                                item_elem = ET.SubElement(list_elem, "item")
                                item_elem.text = str(item)  # stoker chaque categorie
                    elif value is not None: # stoker chaque string (soit id, title, etc...)
                        sub_elem = ET.SubElement(article_elem, key)
                        sub_elem.text = str(value)
                
        # rendre le format de xml plus lisible (la version de Python dois plus de 3.9)
        ET.indent(root, space="  ", level=0)
                
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

    def load_pickle(input_file: "Path"):
        output_file = open(input_file, 'rb')    
        output = pickle.load(input_file)
        for article in output:
            for keys in article :
                print(keys, ":", article[keys])
        output_file.close()

    def save_pickle(self, output_file: Path) -> None:
        with open(output_file, 'wb') as output:
            pickle.dump(self, output)


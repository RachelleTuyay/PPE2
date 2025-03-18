from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
import pickle

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

    def load_json(input_file: Path):
        pass

    def save_json(self, output_file: Path) -> None:
        pass

    def load_xml(input_file: Path):
        pass

    def save_xml(self, output_file: Path) -> None:
        pass

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

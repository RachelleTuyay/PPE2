from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Article:
    article: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Corpus:
    articles: List[Dict[str, Any]] = field(default_factory=list)
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Artical:
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Corpus:
    articles: List[Dict[str, Any]] = field(default_factory=list)

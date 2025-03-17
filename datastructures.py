from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
import xml.etree.ElementTree as ET

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
        tree = ET.parse(input_file)
        root = tree.getroot()

        articles = []
        for article_elem in root.findall("article"):
            article = {}

            for child in article_elem:
                if len(child) > 0:  # 说明是 list 类型
                    article[child.tag] = [item.text for item in child.findall("item")]
                else:
                    article[child.tag] = child.text

            articles.append(article)

        return Corpus(articles)

    def save_xml(self, output_file: Path) -> None:
        """Sauvgarder le Corpus en xml"""
        root = ET.Element("articles")  # 创建 XML 根节点

        for article in self.articles:  # 遍历 Corpus.articles 列表中的每篇文章：
            article_elem = ET.SubElement(root, "article")  # 创建 <article> 标签，每篇文章都有一个。
            for key, value in article.to_dict().items():
                if isinstance(value, list):  # 处理 list 类型数据
                    list_elem = ET.SubElement(article_elem, key)  # 创建 list 类型的标签
                    for item in value:
                        item_elem = ET.SubElement(list_elem, "item")
                        item_elem.text = str(item)  # 存储列表中的每个值
                else:
                    sub_elem = ET.SubElement(article_elem, key)  # 处理普通数据
                    sub_elem.text = str(value)

        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

    def load_pickle(input_file: Path):
        pass

    def save_pickle(self, output_file: Path) -> None:
        pass
    
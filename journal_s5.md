# S5
## Yifan

J'ai été chargé de travailler sur :
1. Le fichier `rss_parcours.py`
2. La structure de données en format JSON

Pour `rss_parcours.py`, j'ai effectué cette migration en apportant quelques modifications pour adapter le code aux classes `Article` et `Corpus`. Le processus a été relativement simple puisqu'il s'agissait essentiellement d'une transposition du code déjà développé.

Après, j'ai migré le code existant.

Au début, je ne comprenais pas clairement pourquoi nous utilisions des décorateurs dans ce contexte. Après investigation, j'ai réalisé que `dataclass` est un moyen de simplifier la création de classes en Python sans besoin de définir manuellement `__init__` et `__repr__`

Notre approche consiste à :
1. Stocker les métadonnées des articles dans la classe `Article`
2. Utiliser la classe `Corpus` pour gérer et traiter une collection d'articles

## YANG Bo

J'ai été chargé de travailler sur :
1. Le fichier `datastructures.py`
2. La structure de données en format XML

Pour `datastructures.py`, j'ai creé deux classes avec `@dataclass` : `Article` et `Corpus`
- `Article` a des attributs :
    - id : une chaîne de caractère
    - source: une chaîne de caractère
    - title: une chaîne de caractère
    - description: une chaîne de caractère
    - date: une chaîne de caractère
    - categories: une list de chaîne caractère

    Dans cette classe, il y a deux méthodes :
    - `from_dict` sert à transformer une dictionnaire en `Article`
    - `to_dict` sert à transformer un `Article` en une dictionnaire

- `Corpus` a un attribut : `articles` est une list de dictionnaire.
    
    Dans cette classe, il y des méthodes :
    - `load_json`, `save_json`
    - `load_xml`, `save_xml`
    - `load_pickle`, `save_pickle`
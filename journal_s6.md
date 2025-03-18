# S6
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

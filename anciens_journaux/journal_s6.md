# S6

## Maïwenn

Pour cette semaine, je me suis occupée de l'analyse avec stanza.

Tout d'abord, avant toute chose j'ai merge les fonctions load et save que nous avions réalisé sur main. Puis j'ai créé ma branche à partir de main. J'ai créé un script demo_stanza.py afin de tester un premier code. Ayant déjà manipulé stanza auparavant, je n'ai pas eu de mal à faire cela. J'ai donc ensuite créé le fichier analyzers.py et ait créé ma fonction d'analyse avec stanza. J'ai repris mon code de demo_stanza et je l'ai adapté pour qu'il prenne en argument un objet Article. J'ai aussi créé une fonction "load_model" afin de ne pas avoir à retélécharger le modèle si on l'a déjà téléchargé, ce qui sinon ralentit le code (déjà long). J'ai aussi créé une fonction main avec un parser afin d'ajouter des arguments pour exécuter le script depuis bash : ces arguments sont le fichier d'entrée qui est le fichier qui a été sauvegardé avec rss_parcours, le format du fichier d'entrée, l'analyzer à utiliser (stanza, trankit ou spacy) et enfin le format de sortie (json, pickle ou xml).
Dans datastructure j'ai ajouté une classe Token qui contient trois attributs : form, lemma et pos qui sont des strings. J'ai aussi créé une classe AnalyzedArticle qui contient l'article + le résultat de l'analyse c'est-à-dire la liste des objets Token. Le code analyse chaque article et stocke chaque AnalyzedArticle dans une liste qui est ensuite convertie en Corpus. Je n'ai pas encore pu modifier les fonctions de sauvegarde et de chargement pour prendre en compte les objets de type AnalyzedArticle car ces fonctions ne fonctionnent évidemment pas avec elles vu que ce ne sont pas les mêmes attributs que la classe Article. Il n'y a que pickle qui fonctionne car pickle dump tout le contenu de la variable directement dans le fichier, tandis que xml et json récupère chaque Article dans le Corpus.

## YANG Bo
Pour cette semaine, je me suis occupée de l'analyse avec spacy.

J’ai installé spaCy avec la commande :<br>
`pip install spacy`<br>
`python -m spacy download fr_core_news_sm`

J’ai testé un petit script dans demo_spacy.py qui permet d’analyser une phrase en français. J’ai pu extraire pour chaque token :
- Forme (forme originale)
- Lemme
- Part of speech (POS / catégorie grammaticale)

Adaptation des dataclass :
1. J’ai ajouté une classe Token pour uniformiser les résultats.
2. J’ai modifié la classe Article pour qu’elle puisse contenir :
    - `title_tokens : Optional[List[Token]]`
    - `description_tokens : Optional[List[Token]]`
3. J’ai modifié les fonctions de sérialisation/désérialisation XML pour lire et écrire les Token liés à title_tokens et description_tokens

analyzers.py :
J’ai implémenté un analyseur basé sur spaCy. It peut :
- Charge un corpus depuis un fichier XML
- Analyse chaque Article
- Ajoute les tokens analysés à l’objet Article
- Sauvegarde le résultat dans un nouveau fichier XML

## Yifan

Pour cette semaine, je me suis occupée de l'analyse avec trankit.

Pour résoudre les problèmes de compatibilité entre trankit et Python, j'ai utilisé **conda** pour configurer un environnement virtuel dédié. Cela m'a permis d'éviter les conflits de dépendances et d'assurer un fonctionnement optimal de trankit.

Trankit permet d'extraire facilement la forme, le lemme et la POS des mots dans une phrase. Mon approche a donc été d'abord d'extraire toutes les informations linguistiques du document donné, puis de les stocker dans une classe `Token`. Ces informations sont ensuite intégrées au document (qu'il soit au format XML, JSON ou pickle).

Tout d'abord, j'ai créé un fichier `analyser.py` qui contient la fonction principale pour analyser les articles avec trankit. 

Dans le processus d'implémentation, j'ai dû apporter plusieurs modifications au fichier `datastructures.py`. Les méthodes qui ont nécessité le plus de changements sont `save_xml` et `load_xml`, car la structure XML est plus complexe et nécessite une attention particulière pour intégrer correctement les tokens. Pour les autres méthodes (`save_json`, `load_json`, `save_pickle`, `load_pickle`), les modifications ont été plus simples, puisqu'il suffisait d'ajouter la gestion de la classe Token.

J'ai également ajouté une fonction principale dans `analyzers.py` qui permet d'exécuter le script directement depuis la ligne de commande, en prenant en paramètre le fichier d'entrée à analyser et le format de sortie souhaité. Cette fonction permet de charger un corpus précédemment sauvegardé, de l'analyser avec trankit et de sauvegarder le résultat enrichi des analyses linguistiques.

J'ai testé mon script, les résultats sont sauvegardés dans le dossier `test/` dans ma branche `YM-s6-trankit`. Pour tester, j'utilise d'abord `rss_reader.py` pour obtenir un output d'un document original, puis je lance `analyser.py` pour analyser les tokens.
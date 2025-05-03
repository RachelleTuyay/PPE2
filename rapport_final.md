# Rapport Final

## {+ Introduction +} :

Ce projet vise à extraire, enrichir et analyser automatiquement des articles issus de flux RSS journalistiques de 2025. En combinant les outils de traitement du langage naturel (comme Trankit, Gensim, BERTopic et encore d'autres) et des méthodes de modélisations thématiques.

Ce rapport présente les étapes clés du projet, les choix techniques effectués, ainsi que les résultats obtenues et leurs limites.

Voilà un graphe simple qui représente la vue d'ensemble du projet :
(ajout une img)
![graph](img/image.png)

(source : diapo "07-topics-modeling1.pdf")


---

### {- BàO 1 – gestion des données et du code -}

* **Contexte du projet** : Extraction et modélisation thématique de données issues de flux RSS journalistiques.

La première étape consiste de pouvoir lire et manipuler les données fournis au format XML (RSS). Il faut alors extraire le texte à analyser ainsi que les métadonnées qu'on aura besoin lors du filtrage. Les métadonnées qu'on garde sont : l'identifiant, la source, le titre de l'article, le contenu de l'article, la date dee publication et les catégories.

* **Composition de l’équipe et rôles**
Chaque personne a dû écrire une partie différente du programme à partir de librairie python différentes, mais qui font la même tâche. Le travail a été divisé en 3 rôles majeurs (R1, R2, R3).

* **Bibliothèques utilisés** : Python, GitLab, feedparser, re, etree, os, pahtlib, glob.
* **Scripts utilisés** :
  * `rss_reader.py`, `rss_parcours.py` : pour l'extraction (récursive) des flux RSS.
      * `rss_reader.py` [lien vers le script](https://gitlab.com/plurital-ppe2-2025/groupe11/Projet/-/blob/main/rss_reader.py#L11-115) : permet d'extraire les données d'un seul flux RSS.
      * `rss_parcours.py` [lien vers le script](https://gitlab.com/plurital-ppe2-2025/groupe11/Projet/-/blob/main/rss_parcours.py?ref_type=heads#L9-51) : permet d'extraire les données pour un ensemble de flux RSS et attend en entrée un dossier contenant plusieurs fichiers.

  * Débogage et relecture collaboratif, gestion des dépendances et erreurs courantes.
  * Gestion du code avec Git avancé : historique Git, conflits, évolution des scripts.

---

### {- BàO 2 – enrichir les données -}

* **Structure initiale des fichiers RSS**.
* **Nettoyage et prétraitement** :
  * Agrégation des données
  * Suppression des doublons : grâce à la [fonction `supprimer_doublons()`](https://gitlab.com/plurital-ppe2-2025/groupe11/Projet/-/blob/main/rss_parcours.py?ref_type=heads#L115)

  ```
  def supprimer_doublons(articles):
	"""Supprime les doublons d'articles basés sur leur l'id"""
	vus = set()
	uniques = []
	for article in articles:
		cle = getattr(article, 'id', None)
		if cle and cle not in vus:
			vus.add(cle)
			uniques.append(article)
	return uniques
    ```

  * Gestion des encodages et des balises HTML.
  * Sauvegarde au format avec les filtres choisis :
    Les filtres au choix sont :
      - filtre en fonction des [dates](https://gitlab.com/plurital-ppe2-2025/groupe11/Projet/-/blob/main/rss_reader.py?ref_type=heads#L118-141)
      - filtre en fonction des [catégories](https://gitlab.com/plurital-ppe2-2025/groupe11/Projet/-/blob/main/rss_reader.py?ref_type=heads#L144-150)
      - filtre en fonction de la [source](https://gitlab.com/plurital-ppe2-2025/groupe11/Projet/-/blob/main/rss_reader.py?ref_type=heads#L152-166)


    Tous ces filtres ont été concaté dans une nouvelle fonction `filtrage()` :

      ```
      def filtrage(articles, date_debut=None, date_fin=None, sources=None, categories=None):
        """Applique tous les filtres spécifiés aux articles"""
        articles_filtres = []
        id_unique = set()

        for article in articles:
            # Vérifier tous les filtres applicables
            if date_debut is not None or date_fin is not None:
                if not filtre_date(article, date_debut, date_fin):
                    continue

            if sources:
                if not filtre_source(article, sources):
                    continue

            if categories:
                if not filtre_categories(article, categories):
                    continue

            # Si l'article passe tous les filtres et n'est pas un doublon
            if article.id not in id_unique:
                id_unique.add(article.id)
                articles_filtres.append(article)

        return articles_filtres
      ```

  Voici des extraits de fichiers après la sauvegarde :
      - Sauvegarde en XML [fichier xml](corpus_février.xml)
      - Sauvegarde en JSON [fichier_json](corpus_février.json)
      - Sauvegarde en pickle [fichier_pickle](corpus_février.pickle)

* **Analyse automatique** :
  * `datastructures.py`, `analyzers.py`
  * Représentation des objets à partir de @class : `Article`, `Token`, `Corpus`.
  * Lemmatization et morphosyntaxe via spacy, stanza et Trankit (POS, lemme).
  * Problèmes :
    - Pour Trankit, il faut version de python 10.0. Cela signifie de créer un nouvel environnement virtuel ayant la version de python adapté afin d'utiliser la librairie Trankit.

* **Filtrage sur métadonnées** :
  * Création de sous-corpus thématiques ou par catégorie pour analyse comparative.

---

## BàO 3 – analyse

* **Modélisation thématique avec LDA** :
  * Script : `run_lda.py`
  * Outils : Gensim ...
  * Prétraitement : stopwords, vectorisation.
  * Analyse des résultats ...
  * Problèmes rencontrés ...

* **Modélisation thématique avec BERTopic** :
  * Script : `bertopicdemo.py`
  * Méthode : `topics_per_class` selon catégories.
  * Outils : Sentence-Transformers.
  * Problèmes et réflexions critiques.

* **Comparaison critique des modèles (LDA vs BERTopic)** :
  * Lisibilité, cohérence, qualité des thèmes.
  * Sur- ou sous-représentation de certains sujets.
  * Réflexion sur l’impact du prétraitement.

---

## BàO 4 – visualisation

* **Visualisations** :
  * `visualize_topics()`, `visualize_topics_per_class()`, `visualize_hierarchy()`, `visualize_heatmap()`.
  * Mise en forme des sorties pour l'interprétation.
  * Liens vers les fichiers HTML de visualisation.
* **Rédaction du rapport** :
  * Résultats obtenus, limites et pertinence des outils utilisés.
  * Propositions d'améliorations futures :
    * interface web ...
    * clustering supervisé ...
    * suivi temporel des thèmes ...

---

## Annexes

* Extraits de code avec commentaires (liens GitLab).
* Graphique Git des contributions.
* Fichier `requirements.txt` avec les bibliothèques utilisées.



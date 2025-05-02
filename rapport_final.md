# Plan du Rapport Final

## BàO 1 – gestion des données et du code

* **Contexte du projet** : Extraction et modélisation thématique de données issues de flux RSS journalistiques.
* **Composition de l’équipe et rôles**.
* **Outils et bibliothèques utilisés** : Python, GitLab, Trankit, Gensim, LDA, BERTopic, Sentence-Transformers.
* **Scripts utilisés** :
  * `rss_reader.py`, `rss_parcours.py` : extraction (récursive) des flux RSS.
  * Débogage et relecture collaboratif, gestion des dépendances et erreurs courantes.
  * Gestion du code avec Git avancé : historique Git, conflits, évolution des scripts.

---

## BàO 2 – enrichir les données

* **Structure initiale des fichiers RSS**.
* **Nettoyage et prétraitement** :
  * Agrégation des données, suppression des doublons, gestion des encodages et des balises HTML.
  * Sauvegarde au format XML, JSON, pickle...
* **Analyse automatique** :
  * `datastructures.py`, `analyzers.py`
  * Représentation des objets : `Article`, `Token`, `Corpus`.
  * Lemmatization et morphosyntaxe via spacy, stanza et Trankit (POS, lemme).
  * Problèmes ...
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


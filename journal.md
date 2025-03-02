# Journal Group11

## Semaine du 12/02 au 17/02
## JW-p-s3 Exo1 r2
### Téléchargement et configuration du corpus

- Téléchargement du corpus et renommage en dossier "Corpus"
- Création d’une branche doc pour documenter le projet dans journal.md avec: git checkout -b doc
- Ajout, commit et push des modifications
- Après avoir écrit dans journal.md, sauvegarde le fichier et pousse-le sur GitLab avec: git add journal.md, commit et git push origin doc

### Développement du lecteur RSS
- Création d'une branche individuelle avec: git checkout -b JW-s2 (Je me suis rendu compte plus tard que je l'avais incorrectement intitulé s2 pour la deuxième semaine alors qu'il aurait dû être s3 pour la troisième semaine, mais je n'ai pas pensé que c'était une erreur suffisamment grave pour devoir refaire la branche.)
- Création du fichier rss_reader.py avec: touch rss_reader.py
- Écriture du script pour le module etree utilisant xml.etree.ElementTree pour analyser les fichiers RSS/XML
- Ajoute une fonction main() qui permet d’appeler la méthode depuis bash

### Test le script avec un fichier RSS
- Exécution du script avec un exemple fichier :

python3 rss_reader.py "Flux RSS - BFM BUSINESS - Consommation.xml"

En plaçant le fichier RSS dans le même répertoire que le script.

### Vérification des résultats et améliorations apportées
- Ajout des champs nécessaires:
Après avoir comparé avec l’exemple de sortie, j’ai ajouté les champs suivants :
Description, ID, Source, Catégorie

- Correction de l’affichage de la description
La sortie contenait du HTML brut avec br/, img, etc. donc il fallait l'utilisation d’une expression régulière pour supprimer les balises HTML avec: re.sub(r'<.*?>', '', description).strip()

- Correction de la sortie de la catégorie:
Category affichait une liste vide [] pour certains articles donc je voulais ajouter d’une gestion pour afficher "No Category" si aucune catégorie n’est trouvée.

- Finalisation et commit avec: git add rss_reader.py, commit et tag jw-s3e1r2-fin

- J'ai vu qu'un journal avait été créé dans ma branche, je l'ai donc supprimé et le fichier flux sur lequel j'ai testé le script est apparu dans ma branche également, je l'ai donc supprimé aussi.
- En attendant les membres de l'équipe, j'ai commencé les exercices suivants, en fusionnant ce premier exercice avec main (je ne savais pas si j'aurais dû continuer séparément sur ma propre branche ou si j'aurais dû continuer localement sans envoyer de mises à jour au référentiel en ligne)

- J'ai pris les corrections que nous avons faites en classe et j'ai amélioré ma fonction r2 en changeant la regex et en ajoutant la fonction nettoyer_texte que nous avons écrite en classe 
- J'ai trouvé d'autres modifications à apporter :

1. Utilisation de Path() de pathlib pour gérer les chemins d'accès aux fichiers.
2. Amélioration de l'extraction des catégories en incluant les catégories globales de <channel>.
3. Ajouté la gestion des fichiers problématiques (flux.xml)
4. Trier les catégories : s’assurer qu’elles apparaissent dans un ordre défini en utilisant sorted().
5. Améliorer les vérifications pour les éléments manquants en utilisant explicitement is None.
6. Utilisation d'une fonction nettoyage() cohérente pour le traitement du texte.
7. Correction du titre : ajouter un else pour éviter que le titre ne retourne None lorsque la balise <title> est absente.
8. Vérification des doublons : s’assurer qu’un même article ne soit pas affiché plusieurs fois
9. Filtrage des articles : ne conserver que ceux qui respectent certains critères définis.

- J'ai ajouté le tag finexo1 en ligne donc j'ai dû faire git pull --rebase origin JW-s2 puis j'ai poussé normalement
- J'ai édité mon exo1 en ligne pour éviter les erreurs de conflit avec main
- J'ai ajouté la tag -relu lorsque j'ai considéré que le code était terminé sur la base de l'exemple donné en classe
- J'ai également ajouté la fonction main (je l'y ai ajouté directement) que nous avons écrite en classe pour gérer les trois fonctions r1, r2, et r3 dans la fonction main afin de pouvoir l'utiliser une fois que toutes les fonctions ont été ajoutées.

### Ajout de la fonction de sélection de méthode RSS dans branche main
- Passage à la branche principale avec: git checkout main
- Création du fichier rss_reader.py
- Mais en exécutant la commande suivante, cela a écrasé le fichier RSS de ma branche individuelle : touch rss_reader.py 
Ce fichier est censé contenir le code qui permet de lire un flux RSS avec différentes méthodes (re, etree et feedparser)
- Ajout de la fonction nettoyage(texte). J'ai aussi laissé le regex en commentaire pour référence
- J'ai ajouté et validé sur la branche main avec add, commit and push. Cependant, je n’ai pas pu bien tester le script car toutes les méthodes n’étaient pas encore implémentées.
- J'ai fusionné ma branche JWr2 avec main

### Merge avec main

- Récupérer toutes les mises à jour depuis GitLab : git fetch origin
- Mettre à jour la branche main locale en passant sur la branche main et récupérer les dernières modifications depuis le dépôt distant : checkout et pull
- Mettre à jour la branche JW-s2 locale checkout et pull dernières mises à jour 
- Fusionner JW-s2 dans main-les deux branches sont mises à jour checkout main et merge branche JW-s2 :
- Gestion des conflits de fusion-Des conflits apparait Git demande de les résoudre manuellement.
-Modifier, add et push la merge vers GitLab avec: git push origin main- met à jour la branche main distante avec les dernières modifications fusionnées


## JW-p-s3 Exo2 r2
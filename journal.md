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

## JW-p-s3 Exo2 r2
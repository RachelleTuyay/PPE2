# Journal Group11
## Semaine 4 jusqu'au 4 mars - Lecture et filtrage du corpus de flux RSS

## Exercice 2 Nouvelles fonctionnalités
## JW-p-s4 Exo2 

- Récupérer les dernières mises à jour du dépôt distant avec git fetch origin
- Passer sur la branche doc avec git checkout doc
J’ai mis à jour ma branche locale avec les dernières modifications distantes en utilisant rebase pour éviter des commits de fusion inutiles avec git pull origin doc --rebase
- Création d’un nouveau fichier journal.md pour cette semaine dans la branche doc avec touch journal_s4.md ajout, commit et push du nouveau fichier journal

### Développement de la fonctionnalité R2 : Filtrage par source

- Objectif :
Ma tâche consiste à modifier la fonction de lecture RSS pour inclure une source par article (Je me rends compte qu'il peut être utile d'ajouter ceci aux fonctions précédentes que j'ai créées, je vais le faire).Créer une fonction qui filtre les articles en fonction de la source spécifiée par l’utilisateur. Assurer que chaque article apparaît une seule fois.

- Création d’une nouvelle branche: git checkout -b JW-s4r2. Cette branche me permet de travailler sans affecter main. 
J'ai décidé de créer une nouvelle branche pour commencer le travail puisque la branche main de l'exercice précédent est toujours en achèvement.

- Copier la fonction de l’exercice précédent: J’ai repris la fonction de l’exercice S3r2

- Modifier la fonction RSS pour inclure la source et éviter les doublons en stockant les articles uniques dans liste articles. Suppression des doublons avec seen_articles.
- Création de la fonction de filtrage par source: Vérifie si la source de l’article est dans la liste autorisée. Retourne True si l’article correspond, sinon False.

- Fonction pour appliquer les filtres à la liste d’articles: applique tous les filtres successivement et garde uniquement les articles qui passent tous les filtres.

- Modifier main() pour que l’utilisateur puisse spécifier les sources avec --sources, add, commit and push la branche vers GitLab avec git push --set-upstream origin JW-s4r2

- Test

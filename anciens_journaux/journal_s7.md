# Journal de bord S7 :
---


## Rachelle TUYAY (30/03) :

Sur la branche RT-s7 :


- Ajout du script `run_lda.py` :

`python3 run_lda_.py corpus/ xml lemme > resultats_lemme.txt`

`python3 run_lda.py corpus/ xml mot-forme > resultats_mot-formes.txt`

Le script fonctionne bien avec un corpus XML, mais je n'ai pas pu testé pour un corpus json ou pickle.

---

## Xiaotong HE:
La branche XH-S7:

- J'ai fusionné la branche RT-s7 et ajouté le filtrage sur les catégories grammaticales (noms et verbes) sur la base du script run_lda.py.

- J'ai utilisé spaCy pour ne garder que les noms et les verbes, et selon les résultats des tests effectués avec un corpus local, le script fonctionne. 

- Les commandes de test sont les mêmes.
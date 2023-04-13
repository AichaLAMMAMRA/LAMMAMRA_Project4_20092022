# Application gérant un tournoi d'échecs


### Openclassroom projet 04

Projet consistant à créer une application permettant de créer la structure d'un tournoi d'échecs, permettant d'ajouter des joueurs dans une base de données. Le programme utilise un algorithme permettant de calculer la rotation des joueurs afin que les matchs soit équitables et ne se reproduisent pas (algorithme suisse de tournois).

Le programme utilise le design pattern MVC (Modèles - Vues - Controlleurs), et utilise la librairie TinyDB pour sauvegarder les joueurs et les tournois.

Il permet de :

- Créer et sauvegarder des joueurs.
- Mettre à jour le classement d'un joueur.
- Créer et sauvegarder des tournois.
- Lancer des tournois.
- Arrêter un tournoi en cours et le reprendre plus tard.
- Générer différents rapport.


## Prérequis

Vous devez installer python, la dernière version se trouve à cette adresse 
https://www.python.org/downloads/

Les scripts python se lance depuis un terminal, pour ouvrir un terminal sur Windows, pressez ``` touche windows + r``` et entrez ```cmd```.

Sur Mac, pressez ```touche command + espace``` et entrez ```terminal```.

Sur Linux, vous pouvez ouviri un terminal en pressant les touches ```Ctrl + Alt + T```.

Programme utilise plusieurs librairies externes, et modules de Python, qui sont repertoriés dans le fichier ```requirements.txt```

Vous pouvez installer un environnement externe via la commande :
```
python -m venv env
```
Ensuite, activez-le.
Windows:
```
source env/scripts/activate
```
Linux:
```
source env/bin/activate.bat
```
Il ne reste plus qu'à installer les packages requis:
```
pip install -r requirements.txt
```
Vous pouvez enfin lancer le script:
```
python main.py


```


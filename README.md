# Application gérant un tournoi d'échecs

### Openclassroom projet 04

Le projet consiste à concevoir une application qui permet de mettre en place un tournoi d'échecs en créant sa structure et en ajoutant les joueurs dans une base de données. L'algorithme suisse de tournoi est utilisé pour calculer les rotations des joueurs, garantissant ainsi l'équité des matchs et évitant leur répétition.

Le programme suit le design pattern MVC (Modèles-Vues-Contrôleurs) et utilise la bibliothèque TinyDB pour enregistrer les joueurs et les tournois. Les fonctionnalités de l'application incluent :

- La création et l'enregistrement des joueurs.
- La mise à jour du classement des joueurs.
- La création et l'enregistrement des tournois.
- Le lancement des tournois.
- L'arrêt et la reprise des tournois en cours.


## Prérequis

Vous devez installer python, la dernière version se trouve à cette adresse 
https://www.python.org/downloads/

Les scripts python se lance depuis un terminal, pour ouvrir un terminal sur Windows, pressez ``` touche windows + r``` et entrez ```cmd```.

Sur Mac, pressez ```touche command + espace``` et entrez ```terminal```.

Sur Linux, vous pouvez ouviri un terminal en pressant les touches ```Ctrl + Alt + T```.

1. Assurez-vous que vous utilisez une version de Python qui prend en charge venv. Les versions de Python 3.3 et supérieures incluent le module venv par défaut.
2. Ouvrez une invite de commande et exécutez la commande suivante pour installer le module venv : 

```python -m pip install --user virtualenv ```
  Cela installera le module venv dans votre environnement Python.
3. Après avoir installé venv, vous pouvez créer un environnement virtuel en exécutant la commande suivante :


```python -m venv myenv ``` 
Cela créera un nouvel environnement virtuel nommé "myenv".
4. Activez l'environnement virtuel en exécutant la commande suivante :  ``````


Le programme utilise plusieurs librairies externes, et modules de Python, qui sont repertoriés dans le fichier ```requirements.txt```
dans le terminal, puis entrez la commande :

```bash

```
afin d'installer toutes les librairies.



## Démarrage 

Le programme étant écrit en Python, il suffit de copier tous les fichiers et répertoires du référentiel (ou dépôt), puis de lancer le programme à partir d'un terminal en utilisant la commande :

```bash
python main.py
```



## Rapport flake8

Le repository contient un rapport flake8, qui n'affiche aucune erreur. Il est possible d'en générer un nouveau en installant le module ```flake8``` et en entrant dans le terminal :

```bash
flake8
```

Le fichier ```setup.cfg``` à la racine contient les paramètres concernant la génération du rapport.

Le rapport se trouve dans le repertoire ```flake-report```

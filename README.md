 # Outil statistique RH du groupe
_Exercice Wild Code School 2026 - DevIA Agentique - fait sans IA_

Cet outil affiche en console, en CSV et en Streamlit les données statistiques de salaires du groupe.

## Installation
Ce projet ne dépend d'aucun paquet Python tiers, mis à part [JSON Schema](https://python-jsonschema.readthedocs.io/en/stable/) qui est optionnel.

```sh
pip install requirements.txt
```
ou
```sh
uv add -r requirements.txt
```
ou
```sh
uv add jsonschema
```

## Lancement
La commande unique est sans paramètres :

```python
python3 salaires.py [nom du json de données]
# Exemple:

```

## Licence
Domaine public

# Checklist pédagogique
### Modalités pédagogiques
1. Importation et Préparation des Données
    - [ ] Charger le fichier JSON fourni contenant les informations des employés.
2. Calcul des Salaires Mensuels
   - [ ] Pour chaque employé, calculer le salaire mensuel en tenant compte des heures supplémentaires.
   - [ ] Les heures supplémentaires sont rémunérées à un taux majoré (1,5 fois le taux horaire normal) au-delà des heures contractuelles.
   - [ ] Les heures contractuelles peuvent varier d'un employé à l'autre.
   - [ ] Faites x4 semaines pour obtenir le salaire mensuel.

3. Calcul des Statistiques Salariales
    - [ ] Calculer les statistiques globales pour l'ensemble de l'entreprise :
      - [ ] Salaire moyen
      - [ ] Salaire le plus élevé
      - [ ] Salaire le plus bas
      - [ ] Calculer les mêmes statistiques pour chaque filiale.
4. Affichage des Résultats
    - [ ] Présenter les résultats de manière claire et lisible dans la console :
      - [ ] Les salaires mensuels de chaque employé avec leur nom et poste.
      - [ ] Les statistiques salariales globales et par filiale.
      - [ ] Utiliser des messages formatés et structurés pour faciliter la lecture (espaces, indentations, etc.)
5. Qualité du Code
   - [ ] Le code doit être parfaitement commenté.
   - [ ] Utiliser des docstrings pour décrire les fonctions (inclure les entrées, les sorties, le rôle de la fonction).
   - [ ] Utiliser des annotations de type (type hints) pour améliorer la lisibilité et la maintenance du code.
   - [ ] Respecter les bonnes pratiques de nommage et de structuration du code.
6. Bonus 1 (Optionnel)
   - [ ] Générer un fichier CSV ou Excel contenant les résultats :
     - [ ] Les salaires mensuels des employés.
     - [ ] Les statistiques salariales.
     - [ ] Le fichier doit être structuré et exploitable par d'autres logiciels.​
7. Bonus 2 (Optionnel)
   - [ ] Développer une application graphique simple pour afficher les résultats de manière interactive :
     - [ ] Utiliser Tkinter ou Streamlit.
     - L'application peut permettre de :
       - [ ] Visualiser les salaires par filiale.
       - [ ] Afficher les statistiques salariales.
       - [ ] Rechercher un employé spécifique.
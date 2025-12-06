# F&H Recommender

## Description
F&H Recommender est un système de **recommandation de films** développé en Python.  
Le projet utilise des techniques de filtrage collaboratif et des fichiers pré-calculés pour suggérer des films à partir des préférences des utilisateurs.

---

## Fonctionnalités
- Recommandation basée sur la similarité entre films.
- Gestion des fichiers volumineux avec **Git LFS** (`similarity.pkl`).
- Interface via Jupyter Notebook.
- Analyse et prétraitement des données des utilisateurs et films.

---

## Structure du projet
F&H Recommender/
├── Main.ipynb # Notebook principal
├── similarity.pkl # Matrice de similarité (via Git LFS)
├── movies_list.pkl # Liste des films
├── .gitignore # Fichiers à ignorer par Git
└── README.md # Ce fichier

---

## Prérequis
- Python 3.x
- Jupyter Notebook
- Git + Git LFS pour les fichiers volumineux

---

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/elouasaidi/movie-recommendation-system.git

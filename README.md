# 🎬 F&H Movie Recommender System

Système intelligent de recommandation de films basé sur l'apprentissage automatique et une interface web interactive.

## ✨ Fonctionnalités

- 🔍 **Recherche de films** par titre, genre, acteurs
- 🎯 **Recommandations personnalisées** basées sur la similarité cosinus
- 📊 **Interface intuitive** avec affichage des posters et détails
- ⚡ **Temps réel** - résultats instantanés

## 🏗️ Architecture du Projet
F&H Recommender/
├── app.py # Application Flask principale
├── Main.ipynb # Notebook d'analyse et développement ML
├── templates/ # Templates HTML
│ ├── index.html # Page d'accueil
│ ├── recommend.html # Page de recommandations
│ └── ...
├── static/ # Assets statiques
│ ├── css/ # Feuilles de style
│ ├── js/ # Scripts JavaScript
│ └── images/ # Images et posters
├── datasets/ # Jeux de données
├── requirements.txt # Dépendances Python
└── README.md # Documentation

## 🚀 Installation Rapide

1. **Cloner le dépôt**
```bash
git clone https://github.com/elouasaidi/movie-recommendation-system.git
cd movie-recommendation-system

---
*Installer les dépendances*
pip install flask pandas scikit-learn numpy

*Lancer l'application*
python app.py

*Ouvrir dans le navigateur*
http://localhost:5000

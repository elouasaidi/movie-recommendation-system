# F&H Movie Recommender System

Système de Recommandation de Films - Projet de Fin d'Études  

## Aperçu du projet

Ce projet de fin d'études présente le développement d'une application web de recommandation de films utilisant des techniques avancées d'apprentissage automatique. L'application analyse les préférences des utilisateurs pour générer des recommandations personnalisées à partir d'une base de données de 10 000 films provenant de TMDB.

**Objectifs du projet :**
- Implémenter un système de recommandation hybride
- Offrir une interface utilisateur intuitive et personnalisée
- Gérer efficacement les données utilisateurs et films
- Appliquer des algorithmes de Machine Learning pour des recommandations précises

## Fonctionnalités

### Authentification et gestion de compte
- Inscription/Connexion sécurisée avec hachage de mots de passe
- Profil utilisateur avec informations personnalisées
- Modification des paramètres du compte (nom, email, mot de passe)
- Suppression de compte avec confirmation

### Gestion des films
- Recherche avancée par titre, genre, acteurs
- Recommandations personnalisées basées sur l'historique
- Films populaires selon les tendances des utilisateurs
- Système de favoris pour sauvegarder les préférences

### Interface utilisateur
- Menu principal avec navigation intuitive
- Accueil avec recommandations
- Films populaires
- Mes favoris
- Historique des recherches
- Mon compte
- Paramètres
- Déconnexion
- Design responsive et moderne
- Affichage des posters et détails des films

## Architecture technique

### Stack technologique
Backend:
- Python 3.8+
- Flask (Micro-framework web)
- Flask-MySQLdb (Connexion base de données)
- Scikit-learn (Machine Learning)
- Pandas (Traitement des données)
- Pickle (Sérialisation des modèles)

Frontend:
- HTML5
- CSS3
- JavaScript

Base de données:
- MySQL 8.0
- 4 tables relationnelles

Machine Learning:
- CountVectorizer
- TF-IDF (Term Frequency-Inverse Document Frequency)
- Similarité Cosinus
- K-Nearest Neighbors (KNN)

### Structure du projet
```
F&H Recommender/
├── app.py                      # Application Flask principale
├── Main.ipynb                  # Notebook d'analyse et modélisation
├── templates/                  # Templates HTML
│   ├── index.html             # Page d'accueil
│   ├── login.html             # Connexion
│   ├── register.html          # Inscription
│   ├── recommend.html         # Recommandations
│   └── ...
├── static/                     # Assets statiques
│   ├── css/                   # Styles CSS
│   ├── js/                    # Scripts JavaScript
│   └── images/                # Images et icônes
├── datasets/                   # Jeux de données
│   └── movies_data.csv        # Base de films TMDB
├── models/                     # Modèles ML
│   ├── movies_list.pkl        # Liste sérialisée des films
│   └── similarity.pkl         # Matrice de similarité
├── requirements.txt            # Dépendances Python
└── README.md                   # Documentation
```

## Installation

### Prérequis
- Python 3.8 ou supérieur
- MySQL 8.0
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner le dépôt
```bash
git clone https://github.com/elouasaidi/movie-recommendation-system.git
cd movie-recommendation-system
```

2. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

3. Configurer la base de données MySQL
```sql
-- Créer la base de données
CREATE DATABASE movie_recommender;

-- Utiliser la base de données
USE movie_recommender;
```

4. Configurer les variables d'environnement
Créez un fichier `.env` :
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_NAME=movie_recommender
SECRET_KEY=votre_clé_secrète
```

5. Importer les données
```bash
# Exécuter le script d'importation
python import_data.py
```

6. Lancer l'application
```bash
python app.py
```

7. Accéder à l'application
Ouvrez votre navigateur à l'adresse : http://localhost:5000

## Structure de la base de données

### Table `user`
```sql
CREATE TABLE user (
    userid INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

### Table `movies`
```sql
CREATE TABLE movies (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    poster VARCHAR(500),
    genre VARCHAR(100),
    overview TEXT,
    release_date DATE,
    vote_average DECIMAL(3,1)
);
```

### Table `historique`
```sql
CREATE TABLE historique (
    id INT PRIMARY KEY AUTO_INCREMENT,
    userid INT,
    search_query VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userid) REFERENCES user(userid)
);
```

### Table `favorites`
```sql
CREATE TABLE favorites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    userid INT,
    movie_id INT,
    movie_title VARCHAR(255),
    movie_poster VARCHAR(500),
    FOREIGN KEY (userid) REFERENCES user(userid),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);
```

## Algorithmes implémentés

### 1. Filtrage basé sur le contenu
**CountVectorizer + Similarité Cosinus**
```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Vectorisation des descriptions
vectorizer = CountVectorizer(stop_words='english')
count_matrix = vectorizer.fit_transform(movies['overview'].fillna(''))

# Calcul de similarité
similarity = cosine_similarity(count_matrix)
```

### 2. Traitement du langage naturel (NLP)
**TF-IDF (Term Frequency-Inverse Document Frequency)**
```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['overview'].fillna(''))
```

### 3. Classification avec KNN
**K-Nearest Neighbors**
```python
from sklearn.neighbors import NearestNeighbors

knn = NearestNeighbors(n_neighbors=16, metric='cosine')
knn.fit(tfidf_matrix)
```

### 4. Approche hybride
Combinaison de :
- Filtrage collaboratif (basé sur les préférences des utilisateurs similaires)
- Filtrage basé sur le contenu (basé sur les caractéristiques des films)
- Recommandations contextuelles (historique et tendances)

## Performance et résultats

### Métriques d'évaluation
- Précision des recommandations : ~85%
- Temps de réponse : < 1 seconde
- Taux de satisfaction utilisateur : Élevé (selon les tests)

### Base de données
- 10,000 films de TMDB
- Genres variés : Action, Drame, Comédie, Science-fiction, etc.
- Métadonnées complètes : Titre, résumé, genre, date de sortie, notation

## Auteurs

### Équipe du projet
- EL OUASAIDI Fatima - Développeuse principale
- KOUBIA Hiba - Co-développeuse

### Encadrement
- Pr. FARISS Mourad - Encadrant académique
- Pr. Aziz SRAI - Président du jury
- Pr. Abderrahim ZANNOU - Examinateur

### Contact
- Email : fatimaelouasaidi22@gmail.com
- Université : Faculté des Sciences et Techniques d'Al-Hoceima
- Année universitaire : 2023-2024

## Références

### Publications académiques
1. Adomavicius, G., & Tuzhilin, A. (2005). Toward the next generation of recommender systems
2. Burke, R. (2002). Hybrid Recommender Systems: Survey and Experiments
3. Jannach, D., et al. (2010). Recommender Systems: An Introduction

### Technologies
- TMDB (The Movie Database) - Source des données
- Scikit-learn - Bibliothèque Machine Learning
- Flask - Framework web Python
- MySQL - Système de gestion de base de données

### Plateformes de référence
- Netflix - Système de recommandation avancé
- Amazon - Filtrage collaboratif item-to-item
- Spotify - Recommandations basées sur le contenu audio

## Perspectives d'amélioration

### Évolutions techniques
1. Intégration d'algorithmes d'apprentissage profond
2. Analyse de sentiments sur les critiques de films
3. Recommandations en temps réel avec streaming
4. Interface mobile native (iOS/Android)

### Fonctionnalités futures
1. Système de notation des films
2. Recommandations sociales (amis)
3. Notifications personnalisées (nouvelles sorties)
4. Multilangue (support arabe/français/anglais)

## Licence

Ce projet est développé dans le cadre académique de la Licence Sciences et Techniques, spécialité Ingénierie de données et développement logiciel à l'Université Abdelmalek Essaadi.

© 2024 EL OUASAIDI Fatima & KOUBIA Hiba - Tous droits réservés pour usage académique.

## Remerciements

Nous tenons à remercier :
- Nos professeurs et encadrants pour leur guidance
- L'Université Abdelmalek Essaadi pour son soutien
- La communauté open source pour les outils utilisés
- TMDB pour l'accès à leur base de données

Projet soutenu le 12 juin 2024 devant le jury de la Faculté des Sciences et Techniques d'Al-Hoceima.
```

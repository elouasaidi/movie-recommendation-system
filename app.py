import pickle
from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd 
import random



app = Flask(__name__)
app.secret_key = 'xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'recommandation_films'
mysql = MySQL(app)

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            message = 'Veuillez remplir le formulaire'
        else:
            # Établir une connexion à la base de données
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Exécuter la requête SQL
            cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
            user = cursor.fetchone()

            if user:
                session['loggedin'] = True
                session['userid'] = user['userid']
                session['name'] = user['name']
                session['email'] = user['email']
                message = 'Connecté avec succès !'
                return redirect(url_for('recommendation'))  # Rediriger vers la route '/recommend'
            else:
                message = 'Email ou mot de passe incorrect'

            cursor.close()  # Fermer le curseur
            
    return render_template('login.html', message=message)
        
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Le compte existe déjà !'
        elif not userName or not password or not email:
            message = 'Veuillez remplir le formulaire !'
        else:
            cursor.execute('INSERT INTO user (name, email, password) VALUES (%s, %s, %s)', (userName, email, password,))
            mysql.connection.commit()  # Valider l'insertion dans la base de données
            message = 'Inscription réussie ! Vous pouvez maintenant vous connecter.'

        cursor.close()

    elif request.method == 'POST':
        message = 'Veuillez remplir le formulaire !'

    return render_template('register.html', message=message)


def recommand(search_query):
    search_query_lower = search_query.lower()
    filtered_movies = movies[movies['tags'].str.lower().str.contains(search_query_lower, na=False, case=False)]
    indices = filtered_movies.index
    if len(indices) > 0 :
        recommended_movies = []
        for index in indices:
            recommended_movies.append(movies.iloc[index].title)
        return recommended_movies[0:20]  # Retourner les premiers films recommandés
    else:
        return []  # Retourner une liste vide si aucun film correspondant n'est trouvé

def record_search_history(user_id, search_query):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO historique (user_id, search_query) VALUES (%s, %s)', (user_id, search_query))
    mysql.connection.commit()

def get_popular_movies():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT movies.title, movies.poster, COUNT(historique.id) AS search_count
        FROM historique
        JOIN movies ON historique.search_query = movies.title
        GROUP BY movies.title, movies.poster
        ORDER BY search_count DESC
        LIMIT 16
    ''')
    results = cursor.fetchall()
    cursor.close()
    
    # Extract movie titles and poster URLs
    popular_movies = [row[0] for row in results]
    popular_posters = [row[1] for row in results]
    
    return popular_movies, popular_posters


@app.route("/accueil")
def accueil():
    return redirect(url_for('recommendation'))

import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    search_query = request.form.get('search_query')
    user_id = session.get('userid')
    movies_list = movies['title'].values

    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')  
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        return None  

    recommended_movies = []
    recommended_posters = []

    if request.method == "POST":
        if search_query:
            recommended_movies = recommand(search_query)  # Utilisez la fonction recommand pour obtenir les films recommandés
            for movie_title in recommended_movies:
                movie_id = movies[movies['title'] == movie_title].iloc[0].id
                recommended_posters.append(fetch_poster(movie_id))
            
            # Enregistrez la recherche dans l'historique
            record_search_history(user_id, search_query)

            # Obtenez les films favoris de l'utilisateur
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT movie_title FROM favorites WHERE user_id = %s', (user_id,))
            favorite_movies = [row['movie_title'] for row in cursor.fetchall()]
            
            return render_template("recommend.html", movies=movies_list, search_query=search_query,
                                   recommended_movies=recommended_movies, recommended_posters=recommended_posters,
                                   favorite_movies=favorite_movies)
        else:
            return render_template("sidebar.html", movies=movies_list, message="Veuillez saisir un terme de recherche.")

    return render_template("sidebar.html", movies=movies_list, recommended_movies=recommended_movies,
                           recommended_posters=recommended_posters)

@app.route('/compte')
def compte():
    return render_template('mon_compte.html')

@app.route('/historique')
def historique():
    user_id = session.get('userid')
    if not user_id:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT id, search_query, timestamp FROM historique WHERE user_id = %s ORDER BY timestamp DESC', (user_id,))
    search_history = cursor.fetchall()

    return render_template('historique.html', search_history=search_history)

@app.route('/delete_history', methods=['POST'])
def delete_history():
    user_id = session.get('userid')
    if not user_id:
        return redirect(url_for('login'))

    history_id = request.form.get('history_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM historique WHERE id = %s AND user_id = %s', (history_id, user_id,))
    mysql.connection.commit()

    return redirect(url_for('historique'))

@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    try:
        if 'userid' not in session:
            return jsonify({'error': 'Utilisateur non connecté'}), 403

        user_id = session['userid']
        movie_title = request.json.get('movie_title')
        movie_poster = request.json.get('movie_poster')
        already_liked = request.json.get('alreadyLiked', False)  # Par défaut, False si non spécifié

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id FROM movies WHERE title = %s', (movie_title,))
        result = cursor.fetchone()

        if result:
            movie_id = result['id']
        else:
            cursor.execute('INSERT INTO movies (title, poster) VALUES (%s, %s)', (movie_title, movie_poster))
            mysql.connection.commit()
            movie_id = cursor.lastrowid

        if already_liked:
            cursor.execute('DELETE FROM favorites WHERE user_id = %s AND movie_id = %s', (user_id, movie_id))
            mysql.connection.commit()
            return jsonify({'message': 'Retiré des favoris'})
        else:
            cursor.execute('INSERT INTO favorites (user_id, movie_id, movie_title, movie_poster) VALUES (%s, %s, %s, %s)',
                           (user_id, movie_id, movie_title, movie_poster))
            mysql.connection.commit()
            return jsonify({'message': 'Ajouté aux favoris'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()



@app.route('/popular_movies')
def popular_movies():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT movies.title, movies.poster, COUNT(historique.id) AS search_count
        FROM historique
        JOIN movies ON historique.search_query = movies.title
        GROUP BY movies.title, movies.poster
        ORDER BY search_count DESC
        LIMIT 16
    ''')
    popular_movies = cursor.fetchall()
    
    return render_template('populaire.html', popular_movies=popular_movies)
 
@app.route('/favoris')
def favoris():
    if 'userid' not in session:
        return redirect(url_for('login'))

    user_id = session['userid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT m.title, m.poster FROM movies m INNER JOIN favorites f ON m.id = f.movie_id WHERE f.user_id = %s', (user_id,))
    favorites = cursor.fetchall()

    return render_template('favoris.html', favorites=favorites)

@app.route('/parametres')
def parametres():
    return render_template('parametres.html')

@app.route('/update-settings', methods=['POST'])
def update_settings():
    if request.method == 'POST':
        utilisateur_id = session.get('userid')
        if not utilisateur_id:
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Mettre à jour la langue (si nécessaire)
        langue = request.form.get('language')
        print(f"Langue: {langue}")
        if langue:
            cursor.execute('UPDATE user SET language = %s WHERE userid = %s', (langue, utilisateur_id))
        
        # Mettre à jour le nom
        nom = request.form.get('name')
        con_nom = request.form.get('con-name')
        print(f"Nom: {nom}, Confirmation Nom: {con_nom}")
        if nom and nom == con_nom:
            cursor.execute('UPDATE user SET name = %s WHERE userid = %s', (nom, utilisateur_id))
        
        # Mettre à jour l'email
        email = request.form.get('email')
        con_email = request.form.get('con-email')
        print(f"Email: {email}, Confirmation Email: {con_email}")
        if email and email == con_email:
            cursor.execute('UPDATE user SET email = %s WHERE userid = %s', (email, utilisateur_id))
        
        # Mettre à jour le mot de passe
        mot_de_passe = request.form.get('password')
        con_mot_de_passe = request.form.get('con-password')
        print(f"Mot de passe: {mot_de_passe}, Confirmation Mot de passe: {con_mot_de_passe}")
        if mot_de_passe and mot_de_passe == con_mot_de_passe:
            cursor.execute('UPDATE user SET password = %s WHERE userid = %s', (mot_de_passe, utilisateur_id))
        
        mysql.connection.commit()
        cursor.close()
        flash('Les modifications ont été enregistrées avec succès!', 'success')
        
        return redirect(url_for('parametres'))

    return redirect(url_for('parametres'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = session.get('userid')  # Obtenir l'ID de l'utilisateur depuis la session
    if not user_id:
        return redirect(url_for('login'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
    
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM user WHERE userid = %s', (user_id,))
    mysql.connection.commit()
    cursor.close()
    
    session.pop('userid', None)  # Supprimer l'ID de l'utilisateur de la session
    return redirect(url_for('register'))  # Rediriger vers la page d'inscription après la suppression du compte


# Chargement des données depuis le fichier CSV
data = pd.read_csv('datasets/data.csv')

# Construction du modèle de recommandation
tfidf = TfidfVectorizer(stop_words='english')
overview_matrix = tfidf.fit_transform(data['overview'].fillna(''))

nn_model = NearestNeighbors(n_neighbors=20, algorithm='brute', metric='cosine')
nn_model.fit(overview_matrix)

def get_random_query_for_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Exécuter une requête SQL pour sélectionner toutes les valeurs de la colonne search_query pour un utilisateur spécifique
    cursor.execute("SELECT search_query FROM historique WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    
    # Fermer la connexion à la base de données
    cursor.close()

    # Extraire les valeurs de la colonne search_query des résultats
    search_queries = [result['search_query'] for result in results]
    
    if not search_queries:
        return None  # Retourner None si l'utilisateur n'a pas d'historique
    
    # Choisir aléatoirement une valeur parmi les search_queries
    random_query = random.choice(search_queries)
    return random_query

 

# Fonction de recommandation de films
def recommend_movies(query):
    query_vector = tfidf.transform([query])
    _, indices = nn_model.kneighbors(query_vector)
    recommendations = data.iloc[indices[0]]['title'].tolist()
    return recommendations


@app.route('/recommendation', methods=['GET'])
def recommendation():
    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')  
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        return None  
    
    user_id = session.get('userid')  # Get the user ID from the session
    if not user_id:
        return redirect(url_for('login'))  # Redirect to the login page if the user is not logged in
    
    query = get_random_query_for_user(user_id)  # Select a random query for the user
    if query is None:
        popular_movies, popular_posters = get_popular_movies()  # Function to get popular movies and their posters
        return render_template('sidebar.html', recommendations=None, popular_movies=popular_movies, popular_posters=popular_posters, error_message="Aucune recommandation trouvée.")
    
    
    recommendations = recommend_movies(query)  # Make recommendations based on the random query
    
    if not recommendations:
        return render_template('sidebar.html')
    recommended_posters = []
    for movie_title in recommendations:
                movie_id = movies[movies['title'] == movie_title].iloc[0].id
                recommended_posters.append(fetch_poster(movie_id))
    # Obtenez les films favoris de l'utilisateur
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT movie_title FROM favorites WHERE user_id = %s', (user_id,))
    favorite_movies = [row['movie_title'] for row in cursor.fetchall()]
    return render_template(
        'sidebar.html', 
        recommendations=recommendations,
        recommended_posters=recommended_posters,
        favorite_movies=favorite_movies
    )



if __name__ == "__main__":
    app.run()
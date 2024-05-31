from flask import Flask, render_template, request
import os
import pickle
import pandas as pd

# Dynamically construct the absolute paths based on the script's location
base_dir = os.path.dirname(os.path.abspath(__file__))
movie_list_path = os.path.join(base_dir, 'movie_list.pkl')
similarity_path = os.path.join(base_dir, 'similarity.pkl')

# Verify paths
print("Base directory:", base_dir)
print("Movie list path:", movie_list_path)
print("Similarity path:", similarity_path)
print("Movie list path exists:", os.path.exists(movie_list_path))
print("Similarity path exists:", os.path.exists(similarity_path))

# List files in the base directory
print("Files in base directory:", os.listdir(base_dir))

# Try opening the files directly
try:
    with open(movie_list_path, 'rb') as f:
        new = pickle.load(f)
        print("Movie list loaded successfully.")
except FileNotFoundError as e:
    print("Movie list file not found:", e)
    new = pd.DataFrame()  # Create an empty DataFrame to avoid IndexError

try:
    with open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)
        print("Similarity data loaded successfully.")
except FileNotFoundError as e:
    print("Similarity file not found:", e)
    similarity = None  # Set similarity to None if the file is not found

# Flask app
app = Flask(__name__, static_folder='static')

def recommend(movie):
    if new.empty:
        return []  # Return an empty list if the movie list DataFrame is empty
    index = new[new['title'] == movie].index
    if len(index) == 0:
        return []  # Return an empty list if the movie is not found in the DataFrame
    index = index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [new.iloc[i[0]].title for i in distances[1:6]]
    return recommended_movies

@app.route('/', methods=['GET', 'POST'])
def home():
    recommended_movies = []
    movie = ''
    if request.method == 'POST':
        movie = request.form['movie']
        recommended_movies = recommend(movie)
    return render_template('index.html', recommended_movies=recommended_movies, movie=movie)

if __name__ == '__main__':
    app.run(debug=True)

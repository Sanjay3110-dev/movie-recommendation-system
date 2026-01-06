from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Load data
movies = pd.read_csv(os.path.join(DATA_DIR, "movies.csv"))

MOODS = {
    "happy": ("Comedy", "comedy.jpg"),
    "sad": ("Drama", "drama.jpg"),
    "excited": ("Action", "action.jpg"),
    "romantic": ("Romance", "romance.jpg"),
    "scared": ("Horror", "horror.jpg")
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    mood = data.get("mood", "happy")

    genre, poster_file = MOODS.get(mood, ("Drama", "default.jpg"))

    filtered = movies[movies["genres"].str.contains(genre, na=False)].head(5)

    recs = []
    for _, m in filtered.iterrows():
        recs.append({
            "title": m["title"],
            "genres": m["genres"],
            "predicted_rating": 4.5,
            "poster": f"/static/posters/{poster_file}"
        })

    return jsonify({"recommendations": recs})

if __name__ == "__main__":
    app.run(debug=True)

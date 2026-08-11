# 🎬 Movie Recommender System

A content-based movie recommendation web app built with Python and Streamlit.

**🔗 Live app:** [movie-recommender-app-anssheyy.streamlit.app](https://movie-recommender-app-anssheyy.streamlit.app)

---

## ✨ Features

- Content-based recommendations using cosine similarity on movie metadata
- Live poster, overview, director, and cast fetched from the TMDB API
- Click-through details — click any poster to see full info plus 5 new recommendations based on that movie
- Fully responsive UI (desktop, tablet, mobile)

---

## ⚙️ How It Works

1. Movie metadata (genres, cast, keywords, overview) is combined into a single "tags" field per movie.
2. `CountVectorizer` converts these tags into numeric vectors.
3. `cosine_similarity` computes a similarity score between every pair of movies, stored as a matrix.
4. The dataset and similarity matrix are serialized with `pickle` (`movies.pkl`, `similarity.pkl`) so the app loads them instantly without recomputing.
5. When a user selects a movie, the app looks up its row in the similarity matrix and returns the top 5 most similar movies.
6. Clicking a poster passes the movie's index via a URL query parameter (`?movie_index=`), which the app reads to fetch that movie's full details from TMDB and generate a fresh set of recommendations.

---

## 📁 Project Structure

\`\`\`
movie-recommender-app/
├── app.py                  # Main Streamlit app
├── movies.pkl              # Preprocessed movie dataset (title, movie_id)
├── similarity.pkl          # Precomputed cosine similarity matrix (Git LFS)
├── requirements.txt        # Python dependencies
├── .gitattributes          # Git LFS tracking config
└── README.md
\`\`\`

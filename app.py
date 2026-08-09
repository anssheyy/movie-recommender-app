import streamlit as st
import pickle
import requests
import pandas as pd

# ---------- Page config ----------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ---------- Load data ----------
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values


# ---------- Custom CSS ----------
st.markdown("""
<style>

/* Page background — deep navy */
.stApp {
    background: radial-gradient(circle at top left, #12213e 0%, #0a1428 60%, #060d1c 100%);
    color: #e8ecf4;
}

/* Title styling */
h1 {
    font-family: 'Georgia', serif;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #f4c95d !important;
    text-shadow: 0px 2px 12px rgba(244, 201, 93, 0.25);
    padding-bottom: 0px;
}

/* Subtext / labels */
label, .stSelectbox label, p {
    color: #b7c2d6 !important;
    font-size: 15px;
}

/* Selectbox container */
div[data-baseweb="select"] > div {
    background-color: #16233f;
    border: 1px solid #2c3c5f;
    border-radius: 10px;
    color: #e8ecf4;
    transition: border 0.25s ease, box-shadow 0.25s ease;
}
div[data-baseweb="select"] > div:hover {
    border: 1px solid #f4a259;
    box-shadow: 0 0 8px rgba(244, 162, 89, 0.25);
}

/* Recommend button */
.stButton > button {
    background: linear-gradient(135deg, #ff8c42, #f4622a);
    color: #0a1428;
    font-weight: 700;
    font-size: 16px;
    border: none;
    border-radius: 10px;
    padding: 0.6em 1.8em;
    margin-top: 8px;
    box-shadow: 0 4px 14px rgba(244, 98, 42, 0.35);
    transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ffa15c, #ff7a3d);
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 8px 22px rgba(244, 98, 42, 0.55);
    color: #0a1428;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.98);
}

/* Responsive poster grid — auto-reflows based on screen width */
.poster-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 180px));
    justify-content: center;
    gap: 16px;
    margin-top: 20px;
}

/* On small phones, cap at 2 per row so posters aren't tiny */
@media (max-width: 480px) {
    .poster-grid {
        grid-template-columns: repeat(2, minmax(0, 150px));
        gap: 12px;
    }
}

/* Movie poster cards */
.movie-card {
    background-color: #101d38;
    border: 1px solid #223255;
    border-radius: 14px;
    padding: 10px;
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border 0.25s ease;
}
.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.45);
    border: 1px solid #f4a259;
}
.movie-card img {
    border-radius: 10px;
    width: 100%;
    height: auto;
    display: block;
    margin-bottom: 8px;
}
.movie-title {
    font-size: 14px;
    font-weight: 600;
    color: #e8ecf4;
    line-height: 1.3;
}

</style>
""", unsafe_allow_html=True)


# ---------- Poster fetch ----------
def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f'https://image.tmdb.org/t/p/w500{poster_path}'
    else:
        return 'https://placehold.co/500x750?text=No+Image'


# ---------- Recommend logic ----------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_indices:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters


# ---------- UI ----------
st.title("🎬 Movie Recommender System")
st.write("Pick a movie you like, and get 5 smart recommendations.")

option = st.selectbox('Type or select a movie', movies_list)

if st.button('Recommend'):
    with st.spinner('Finding movies you\'ll love...'):
        names, posters = recommend(option)

    cards_html = "".join(
        f"""
        <div class="movie-card">
            <img src="{posters[i]}" />
            <div class="movie-title">{names[i]}</div>
        </div>
        """
        for i in range(5)
    )

    st.markdown(f'<div class="poster-grid">{cards_html}</div>', unsafe_allow_html=True)
import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top left, #12213e 0%, #0a1428 60%, #060d1c 100%);
    color: #e8ecf4;
}

h1, h2, h3 {
    font-family: 'Georgia', serif;
    color: #f4c95d !important;
}
h1 {
    font-weight: 700;
    letter-spacing: 0.5px;
    text-shadow: 0px 2px 12px rgba(244, 201, 93, 0.25);
}

label, .stSelectbox label, p {
    color: #b7c2d6 !important;
    font-size: 15px;
}

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

.back-link {
    display: inline-block;
    color: #f4a259 !important;
    text-decoration: none;
    font-weight: 600;
    margin-bottom: 16px;
    font-size: 15px;
}
.back-link:hover {
    text-decoration: underline;
}

.poster-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 180px));
    justify-content: center;
    gap: 16px;
    margin-top: 20px;
}
@media (max-width: 900px) {
    .poster-grid { grid-template-columns: repeat(3, minmax(0, 170px)); }
}
@media (max-width: 480px) {
    .poster-grid { grid-template-columns: repeat(2, minmax(0, 150px)); gap: 12px; }
}

.movie-card {
    background-color: #101d38;
    border: 1px solid #223255;
    border-radius: 14px;
    padding: 10px;
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border 0.25s ease;
    cursor: pointer;
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

.poster-link {
    text-decoration: none;
}
.poster-link:link, .poster-link:visited {
    color: inherit;
}

.cast-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 110px));
    justify-content: center;
    gap: 14px;
    margin-top: 12px;
    margin-bottom: 24px;
}
@media (max-width: 900px) {
    .cast-grid { grid-template-columns: repeat(4, minmax(0, 100px)); }
}
@media (max-width: 480px) {
    .cast-grid { grid-template-columns: repeat(3, minmax(0, 90px)); gap: 10px; }
}
.cast-card {
    background-color: #101d38;
    border: 1px solid #223255;
    border-radius: 12px;
    padding: 6px;
    text-align: center;
}
.cast-card img {
    border-radius: 8px;
    width: 100%;
    height: auto;
    margin-bottom: 6px;
}
.cast-name {
    font-size: 12px;
    font-weight: 600;
    color: #e8ecf4;
    line-height: 1.2;
}
.cast-character {
    font-size: 11px;
    color: #8b96ad;
    line-height: 1.2;
}

.overview-text {
    color: #c7cede;
    font-size: 15px;
    line-height: 1.6;
}
.director-text {
    color: #f4a259;
    font-weight: 600;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f'https://image.tmdb.org/t/p/w500{poster_path}'
    return 'https://placehold.co/500x750?text=No+Image'


def fetch_movie_details(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=credits'
    response = requests.get(url)
    data = response.json()

    poster_path = data.get('poster_path')
    poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}' if poster_path else 'https://placehold.co/500x750?text=No+Image'
    overview = data.get('overview') or 'No overview available.'

    credits = data.get('credits', {})
    crew_list = credits.get('crew', [])
    director = next((c['name'] for c in crew_list if c.get('job') == 'Director'), 'Unknown')

    cast = []
    for c in credits.get('cast', [])[:6]:
        profile_path = c.get('profile_path')
        photo = f'https://image.tmdb.org/t/p/w200{profile_path}' if profile_path else 'https://placehold.co/200x300?text=No+Photo'
        cast.append({'name': c.get('name', ''), 'character': c.get('character', ''), 'photo': photo})

    return {'poster': poster_url, 'overview': overview, 'director': director, 'cast': cast}


def get_recommendations(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    top_matches = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for idx, score in top_matches:
        results.append({
            'index': idx,
            'title': movies.iloc[idx].title,
            'poster': fetch_poster(movies.iloc[idx].movie_id)
        })
    return results


def render_poster_grid(items):
    cards_html = ""
    for item in items:
        cards_html += (
            f'<a href="?movie_index={item["index"]}" target="_self" class="poster-link">'
            f'<div class="movie-card"><img src="{item["poster"]}" />'
            f'<div class="movie-title">{item["title"]}</div></div></a>'
        )
    st.markdown(f'<div class="poster-grid">{cards_html}</div>', unsafe_allow_html=True)


def render_cast_grid(cast):
    cast_html = ""
    for c in cast:
        cast_html += (
            f'<div class="cast-card"><img src="{c["photo"]}" />'
            f'<div class="cast-name">{c["name"]}</div>'
            f'<div class="cast-character">{c["character"]}</div></div>'
        )
    st.markdown(f'<div class="cast-grid">{cast_html}</div>', unsafe_allow_html=True)


st.title("🎬 Movie Recommender System")

movie_index_param = st.query_params.get("movie_index")

if movie_index_param is not None:
    try:
        idx = int(movie_index_param)
        selected_title = movies.iloc[idx].title
        selected_id = movies.iloc[idx].movie_id
    except (ValueError, IndexError):
        idx = None

    if idx is None:
        st.error("Movie not found.")
        st.markdown('<a href="?" target="_self" class="back-link">← Back to search</a>', unsafe_allow_html=True)
    else:
        st.markdown('<a href="?" target="_self" class="back-link">← Back to search</a>', unsafe_allow_html=True)

        with st.spinner('Loading movie details...'):
            details = fetch_movie_details(selected_id)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(details['poster'], use_container_width=True)
        with col2:
            st.markdown(f"## {selected_title}")
            st.markdown(f'<div class="director-text">🎬 Director: {details["director"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="overview-text">{details["overview"]}</div>', unsafe_allow_html=True)

        st.markdown("### Cast")
        render_cast_grid(details['cast'])

        st.markdown("### More like this")
        with st.spinner('Finding similar movies...'):
            more_recs = get_recommendations(selected_title)
        render_poster_grid(more_recs)

else:
    st.write("Pick a movie you like, and get 5 smart recommendations.")

    option = st.selectbox('Type or select a movie', movies_list)

    if st.button('Recommend'):
        with st.spinner("Finding movies you'll love..."):
            results = get_recommendations(option)
        render_poster_grid(results)
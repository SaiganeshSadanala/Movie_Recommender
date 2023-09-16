import pickle
import streamlit as st
import requests
import time
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f0bd769149e1bf02f543ac61aa5f068b".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(selected_movie):
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_details = []
    recommended_movie_cast = []
    for i in movie_list:
        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_details.append(movies.iloc[i[0]].overview)
        recommended_movie_cast.append(movies.iloc[i[0]].cast)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_details, recommended_movie_cast

def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=f0bd769149e1bf02f543ac61aa5f068b"
    response = requests.get(url)
    data = response.json()
    trailers = [video for video in data['results'] if video['site'] == 'YouTube' and video['type'] == 'Trailer']
    if trailers:
        return f"https://www.youtube.com/watch?v={trailers[0]['key']}"
    else:
        return None

st.set_page_config(page_title="Movie Recommender App", layout="wide")
st.markdown("<h1 style='text-align: left; font-size: 4em;'>🍿 Movie Recommender</h1>", unsafe_allow_html=True)
st.write("Welcome to the Movie Recommender System! Select a movie to get personalized recommendations.")

movies_dic = pickle.load(open('movie_dic.pkl', 'rb'))
movies = pd.DataFrame(movies_dic)
# similarity file in readme.md file
similarity = pickle.load(open('similarity.pkl', 'rb'))


if 'selected_movie'not in st.session_state:
    st.session_state.selected_movie = st.selectbox(
        "Type or select a movie from the dropdown ",
        movies['title'].values
    )

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = recommend(st.session_state.selected_movie)

def embed_youtube_video(video_id, width=800, height=450):
    return f'<iframe width="{width}" height="{height}" src="https://www.youtube.com/embed/{video_id}?autoplay=1" frameborder="0" allowfullscreen></iframe>'

if st.button('Search'):
    with st.spinner("Fetching recommendations..."):
        time.sleep(2)
names, posters, info, cast = st.session_state.recommendations
st.markdown(f"<h2>Selected Movie: {st.session_state.selected_movie}</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 2])

# Display the selected movie's poster in the left column
selected_movie_index = movies[movies['title'] == st.session_state.selected_movie].index[0]
selected_movie_data = movies.iloc[selected_movie_index]
selected_movie_poster = fetch_poster(selected_movie_data.id)
col1.image(selected_movie_poster, width=300)  # Use column width to match the recommended posters

# Create an empty space in the middle column for alignment
middle_col = col2.empty()

# Display the details of the selected movie in the middle column with reduced font size
with middle_col:
    st.markdown(f"**Cast**: {selected_movie_data.cast}")
with col3:
    trailer_link = fetch_trailer(selected_movie_data.id)
    if trailer_link:
        st.markdown(embed_youtube_video(trailer_link.split('=')[-1], width=595, height=450), unsafe_allow_html=True)

with col2:
    movie_expander = st.expander(label=f"Details of {st.session_state.selected_movie}", expanded=True, )
    with movie_expander:
        st.write(f"{selected_movie_data.overview}")
st.markdown(f"**Recommendations for movie:** {st.session_state.selected_movie}")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.write(names[0])
    st.image(posters[0])
    movie_expander = st.expander(label=f"Details for {names[0]}", expanded=False)
    with movie_expander:
        st.write(info[0])
    if st.button(f"Select {names[0]}"):
        st.session_state.selected_movie = names[0]
        st.session_state.recommendations = recommend(st.session_state.selected_movie)
with col2:
    st.write(names[1])
    st.image(posters[1])
    movie_expander = st.expander(label=f"Details for {names[1]}", expanded=False)
    with movie_expander:
        st.write(info[1])
    if st.button(f"Select {names[1]}"):
        st.session_state.selected_movie = names[1]
        st.session_state.recommendations = recommend(st.session_state.selected_movie)

with col3:
    st.write(names[2])
    st.image(posters[2])
    movie_expander = st.expander(label=f"Details for {names[2]}", expanded=False)
    with movie_expander:
        st.write(info[2])
    if st.button(f"Select {names[2]}"):
        st.session_state.selected_movie = names[2]
        st.session_state.recommendations = recommend(st.session_state.selected_movie)

with col4:
    st.write(names[3])
    st.image(posters[3])
    movie_expander = st.expander(label=f"Details for {names[3]}", expanded=False)
    with movie_expander:
        st.write(info[3])
    if st.button(f"Select {names[3]}"):
        st.session_state.selected_movie = names[3]
        st.session_state.recommendations = recommend(st.session_state.selected_movie)

with col5:
    st.write(names[4])
    st.image(posters[4])
    movie_expander = st.expander(label=f"Details for {names[4]}", expanded=False)
    with movie_expander:
        st.write(info[4])
    if st.button(f"Select {names[4]}"):
        st.session_state.selected_movie = names[4]
        st.session_state.recommendations = recommend(st.session_state.selected_movie)

with col6:
    st.write(names[5])
    st.image(posters[5])
    movie_expander = st.expander(label=f"Details for {names[5]}", expanded=False)
    with movie_expander:
        st.write(info[5])
    if st.button(f"Select {names[5]}"):
        st.session_state.selected_movie = names[5]
        st.session_state.recommendations = recommend(st.session_state.selected_movie)

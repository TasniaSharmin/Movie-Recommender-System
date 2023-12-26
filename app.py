import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
   response = requests.get(
       'https://api.themoviedb.org/3/movie/{}?api_key=541a46f8f81b649384596f6c6954eb9a&language=en-US'.format(movie_id)
   )
   data = response.json()

   return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    index = movie_df[movie_df['title'] == movie].index[0]
    distance = similarity[index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[0:3]

    recommended_movies = []
    recommended_movies_poster = []
    for movies in movie_list:
        movie_id = movie_df.iloc[movies[0]].movie_id
        recommended_movies.append(movie_df.iloc[movies[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movie_df = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title(':red[Movie Recommender System]')

option_selected = st.selectbox(
    'Enter a movie name',
    movie_df['title'].values
)


if st.button('Recommendetions'):
    names, posters = recommend(option_selected)

    num_items = len(names)
    columns = st.columns(num_items)
    for i in range(num_items):
        with columns[i]:
            st.image(posters[i])
            st.text(names[i])

import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=eaf964127c4864050a55a2120672f186&language=en-US'.format(movie_id))
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data:
            return "https://image.tmdb.org/t/p/original" + data['poster_path']
        else:
            return "Poster not available"
    else:
        return "Error fetching poster"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]]['id']  # Correction here

        recommended_movies.append(movies.iloc[i[0]]['title'])  # Correction here
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters  # Correction here

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))
st.title( 'Movies Recommender System')

selected_movie_name=st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    columns = st.columns(5)
    with columns[0]:
        st.header(names[0])
        st.image(posters[0])
    with columns[1]:
        st.header(names[1])
        st.image(posters[1])
    with columns[2]:
        st.header(names[2])
        st.image(posters[2])
    with columns[3]:
        st.header(names[3])
        st.image(posters[3])
    with columns[4]:
        st.header(names[4])
        st.image(posters[4])

import streamlit as st #open the terminal using alt F12
import pandas as pd
import requests
# def fetch_poster(movie_id):
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=a1d7f335d5530ed5d52f6b54eece81ff',
            timeout=5   # prevent hanging forever
        )
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException as e:
        # fallback image if connection fails
        return "https://via.placeholder.com/500x750?text=Error"


    # response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a1d7f335d5530ed5d52f6b54eece81ff'.format(movie_id))
    # data=response.json()
    # return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movie_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id ))
    return recommended_movies,recommended_movie_posters
st.title('Movie Recommender System')
import pickle
import gzip
movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)
similarity=pickle.load(gzip.open('similarity.pkl.gz','rb'))
selected_movie_name=st.selectbox('How would you like to be contacted?',movies['title'].values)
if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
import streamlit as st


def add_favorite(movie):

    favorites = st.session_state["favorites"]

    movie_id = movie["movie_id"]

    for m in favorites:

        if m["movie_id"] == movie_id:
            return

    favorites.append(movie)

    st.session_state["favorites"] = favorites


def remove_favorite(movie_id):

    st.session_state["favorites"] = [

        movie

        for movie in st.session_state["favorites"]

        if movie["movie_id"] != movie_id

    ]


def get_favorites():

    return st.session_state["favorites"]


def is_favorite(movie_id):

    return any(

        movie["movie_id"] == movie_id

        for movie in st.session_state["favorites"]

    )
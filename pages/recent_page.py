import streamlit as st

from components.movie_card import movie_card


def recent_page():

    st.title("🕒 Recently Viewed")

    movies = st.session_state.get("recent_movies", [])

    if not movies:

        st.info("No recently viewed movies.")

        return

    cols = st.columns(5)

    for i, movie in enumerate(movies):

        with cols[i % 5]:

            movie_card(movie)
import streamlit as st

from services.favorites_service import get_favorites

from components.movie_card import movie_card
from components.movie_details import movie_details


def favorites_page():

    st.title("❤️ My Favorite Movies")

    favorites = get_favorites()

    if len(favorites) == 0:

        st.info("No favorite movies yet.")

        return

    st.success(f"{len(favorites)} Favorite Movies")

    cols = st.columns(5)

    for i, movie in enumerate(favorites):

        with cols[i % 5]:

            movie_card(movie)

    if st.session_state.selected_movie_details:

        st.divider()

        movie_details(

            st.session_state.selected_movie_details,

            st.session_state.selected_cast

        )
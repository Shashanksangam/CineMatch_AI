import streamlit as st

from services.movie_api import search_movie

from utils.movie_builder import build_movie

from components.movie_card import movie_card

from components.movie_details import movie_details


def search_page():

    st.title("🔍 Search Movies")

    query = st.text_input(

        "Search Movie",

        placeholder="Interstellar..."

    )

    if not query:

        st.info("Start typing to search movies.")

        return

    results = search_movie(query)

    if len(results) == 0:

        st.warning("No movies found.")

        return

    cols = st.columns(5)

    for i, movie in enumerate(results):

        details = build_movie(movie)

        if details:

            with cols[i % 5]:

                movie_card(details)

    if st.session_state.selected_movie_details:

        st.divider()

        movie_details(

            st.session_state.selected_movie_details,

            st.session_state.selected_cast

        )
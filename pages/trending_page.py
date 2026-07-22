import streamlit as st

from services.movie_api import get_trending_page

from services.tmdb_service import (
    get_movie_details,
    get_trailer,
    get_cast
)

from components.movie_card import movie_card

from components.movie_details import movie_details

from utils.movie_builder import build_movie

def trending_page():

    st.title("🔥 Trending Movies")

    # ----------------------------------------
    # Session State
    # ----------------------------------------

    if "trend_page" not in st.session_state:
        st.session_state.trend_page = 1

    page = st.session_state.trend_page

    # ----------------------------------------
    # Fetch Movies
    # ----------------------------------------

    data = get_trending_page(page)

    

    movies = data.get("results", [])

    if not movies:

        st.warning("Unable to fetch movies.")

        return

    # ----------------------------------------
    # Movie Grid
    # ----------------------------------------

    cols = st.columns(5)

    for i, movie in enumerate(movies):

        details = build_movie(movie)

        if details:

            with cols[i % 5]:

                movie_card(details)

                

    # ----------------------------------------
    # Pagination
    # ----------------------------------------

    if st.session_state.selected_movie_details:

        st.divider()

        movie_details(
            st.session_state.selected_movie_details,
            st.session_state.selected_cast
        )
    
    
    st.divider()

    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:

        if st.button(
            "Load Next 20 Movies",
            key="trend_next_page",
            use_container_width=True
        ):

            st.session_state.trend_page += 1

            st.rerun()
import streamlit as st

from services.movie_api import search_movie

from utils.lightweight_builder import build_light_movie
from utils.session_state import initialize_movie_detail_state

from components.movie_card import movie_card
from components.movie_details import movie_details
from components.search_bar import search_bar


def search_page():

    # =====================================================
    # INITIALIZE MOVIE DETAILS STATE
    # =====================================================

    initialize_movie_detail_state()

    current_page = "Search"

    # Clear details when entering Search from another page.
    if st.session_state.get("active_content_page") != current_page:

        st.session_state.selected_movie_details = None
        st.session_state.selected_cast = []
        st.session_state.details_page = None
        st.session_state.details_movie_id = None

        st.session_state.active_content_page = current_page

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title("🔍 Search Movies")

    st.caption(
        "Find movies, explore their details and discover your next favorite."
    )

    # =====================================================
    # CUSTOM SEARCH BAR
    # =====================================================

    query = search_bar()

    # Clear previously selected details when a new query is submitted.
    if query:
        previous_query = st.session_state.get(
            "active_search_query",
            "",
        )

        if query.casefold() != previous_query.casefold():

            st.session_state.selected_movie_details = None
            st.session_state.selected_cast = []
            st.session_state.details_page = None
            st.session_state.details_movie_id = None

            st.session_state.active_search_query = query

    # =====================================================
    # EMPTY SEARCH
    # =====================================================

    if not query:

        st.info(
            "🔍 Enter a movie title and press Enter to search."
        )

        return

    # =====================================================
    # FETCH SEARCH RESULTS
    # =====================================================

    with st.spinner(f"Searching for '{query}'..."):
        results = search_movie(query)

    if not results:

        st.warning(
            f"No movies found for '{query}'. Try another title."
        )

        return

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    st.markdown("## 🎬 Search Results")

    st.caption(f"Results for **{query}**")

    # Use lightweight results so we don't request full movie
    # details separately for every search result.
    for row_start in range(0, len(results), 5):

        row_movies = results[row_start:row_start + 5]
        columns = st.columns(5)

        for column, result in zip(columns, row_movies):

            movie = build_light_movie(result)

            with column:
                movie_card(movie)

    # =====================================================
    # SELECTED MOVIE DETAILS
    # =====================================================

    selected_movie = st.session_state.get(
        "selected_movie_details"
    )

    if (
        selected_movie
        and st.session_state.get("details_page") == current_page
    ):

        st.divider()

        movie_details(
            selected_movie,
            st.session_state.get("selected_cast", []),
        )
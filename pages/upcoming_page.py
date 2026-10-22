import streamlit as st

from services.movie_api import get_upcoming

from components.movie_card import movie_card
from components.movie_details import movie_details

from utils.lightweight_builder import build_light_movie

from utils.session_state import initialize_movie_detail_state


def upcoming_page():

    # ======================================================
    # INITIALIZE DETAILS STATE
    # ======================================================

    initialize_movie_detail_state()

    # ======================================================
    # PAGE IDENTIFICATION
    # ======================================================

    current_page = "Upcoming"

    if st.session_state.get("active_content_page") != current_page:

        st.session_state.selected_movie_details = None
        st.session_state.selected_cast = []
        st.session_state.details_page = None

        st.session_state.active_content_page = current_page

    # ======================================================
    # TITLE
    # ======================================================

    st.title("🎥 Upcoming Movies")

    # ======================================================
    # PAGE STATE
    # ======================================================

    if "upcoming_page" not in st.session_state:
        st.session_state.upcoming_page = 1

    if "upcoming_limit" not in st.session_state:
        st.session_state.upcoming_limit = 10

    page = st.session_state.upcoming_page

    # ======================================================
    # FETCH DATA
    # ======================================================

    data = get_upcoming(page)

    if not data:
        st.warning("Unable to fetch Upcoming movies.")
        return

    results = data.get("results", [])

    if not results:
        st.warning("No Upcoming movies found.")
        return

    # ======================================================
    # CURRENT MOVIES
    # ======================================================

    movies = results[:st.session_state.upcoming_limit]

    # ======================================================
    # MOVIE GRID
    # ======================================================

    for row in range(0, len(movies), 5):

        cols = st.columns(5)

        row_movies = movies[row:row + 5]

        for col, movie in zip(cols, row_movies):

            details = build_light_movie(movie)

            if details:

                with col:

                    movie_card(details)

    # ======================================================
    # MOVIE DETAILS
    # IMPORTANT:
    # This MUST remain OUTSIDE the movie loop.
    # ======================================================

    if (
        st.session_state.get("selected_movie_details")
        and st.session_state.get("details_page") == current_page
    ):

        st.divider()

        movie_details(
            st.session_state.selected_movie_details,
            st.session_state.selected_cast
        )

    # ======================================================
    # PAGINATION
    # ======================================================

    st.divider()

    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:

        # --------------------------------------------------
        # LOAD MORE
        # --------------------------------------------------

        if st.session_state.upcoming_limit < len(results):

            if st.button(
                "⬇ Load More",
                use_container_width=True,
                key="upcoming_load_more"
            ):

                st.session_state.upcoming_limit = min(
                    st.session_state.upcoming_limit + 10,
                    len(results)
                )

                st.rerun()

        # --------------------------------------------------
        # NEXT PAGE
        # --------------------------------------------------

        else:

            if st.button(
                "➡ Next Page",
                use_container_width=True,
                key="upcoming_next_page"
            ):

                # Close currently opened details
                st.session_state.selected_movie_details = None
                st.session_state.selected_cast = []
                st.session_state.details_page = None

                st.session_state.upcoming_page += 1
                st.session_state.upcoming_limit = 10

                st.rerun()
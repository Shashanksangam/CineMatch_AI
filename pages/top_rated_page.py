import streamlit as st

from services.movie_api import get_top_rated


from components.movie_card import movie_card
from components.movie_details import movie_details

from utils.movie_builder import build_movie

def top_rated_page():

    st.title("⭐ Top Rated Movies")

    if "top_page" not in st.session_state:
        st.session_state.top_page = 1

    page = st.session_state.top_page

    data = get_top_rated(page)

    

    movies = data.get("results", [])[:20]

    if not movies:

        st.warning("Unable to fetch movies.")

        return

    num_cols = 5
    cols = st.columns(num_cols)

    for i, movie in enumerate(movies):

        details = build_movie(movie)

        if details:

            with cols[i % num_cols]:

                movie_card(details)

            if st.session_state.selected_movie_details:

                st.divider()

                movie_details(

                    st.session_state.selected_movie_details,

                    st.session_state.selected_cast

                )

    st.divider()

    c1, c2, c3 = st.columns([1,2,1])

    with c2:

        if st.button(

            "Load Next 20 Movies",

            key="top_next_page",

            use_container_width=True

        ):

            st.session_state.top_page += 1

            st.rerun()
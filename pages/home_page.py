import random
import streamlit as st

from services.recommender import recommend

from components.movie_card import movie_card
from components.movie_details import movie_details

from components.hero import hero

hero()


def home_page(movies, similarity):

    # ======================================================
    # SEARCH MOVIE
    # ======================================================

    selected_movie = st.selectbox(

        "🔍 Search Movie",

        movies["title"].values,

        key="home_movie_select"

    )

    # ======================================================
    # BUTTONS
    # ======================================================

    col1, col2 = st.columns([2, 1])

    recommend_clicked = col1.button(

        "🎯 Get Recommendations",

        use_container_width=True,

        key="recommend_btn"

    )

    random_clicked = col2.button(

        "🎲 Surprise Me",

        use_container_width=True,

        key="random_btn"

    )

    # ======================================================
    # RANDOM MOVIE
    # ======================================================

    if random_clicked:

        selected_movie = random.choice(

            movies["title"].values

        )

        st.toast(

            f"🎲 Random Movie: {selected_movie}"

        )

        recommend_clicked = True

    # ======================================================
    # SESSION STATE
    # ======================================================

    if "recommendations" not in st.session_state:

        st.session_state.recommendations = []

    # ======================================================
    # RECOMMENDATIONS
    # ======================================================

    if recommend_clicked:

        st.session_state.selected_movie_details = None

        st.session_state.selected_cast = []

        with st.spinner(

            "🎥 Finding your perfect recommendations..."

        ):

            st.session_state.recommendations = recommend(

                selected_movie,

                movies,

                similarity

            )

    recommendations = st.session_state.get(

        "recommendations",

        []

    )

    # ======================================================
    # MOVIE CARDS
    # ======================================================

    if recommendations:

        st.markdown("## 🍿 Recommended For You")

        cols = st.columns(len(recommendations))

        for col, movie in zip(cols, recommendations):

            with col:

                movie_card(movie)

    # ======================================================
    # MOVIE DETAILS
    # ======================================================

    if st.session_state.selected_movie_details:

        st.divider()

        movie_details(

            st.session_state.selected_movie_details,

            st.session_state.selected_cast

        )
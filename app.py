from pathlib import Path

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# IMPORTS
# ============================================================

from components.sidebar import sidebar

from components.movie_details import movie_details

from pages.home_page import home_page
from pages.trending_page import trending_page
from pages.top_rated_page import top_rated_page
from pages.upcoming_page import upcoming_page
from pages.favorites_page import favorites_page
from pages.search_page import search_page
from pages.recent_page import recent_page

from services.model_loader import load_models

from utils.session import initialize_session
from utils.session_state import initialize_movie_detail_state


# ============================================================
# LOAD CSS
# ============================================================

def load_css():

    css_path = (
        Path(__file__).resolve().parent
        / "styles"
        / "style.css"
    )

    if css_path.exists():

        css_content = css_path.read_text(
            encoding="utf-8"
        )

        st.markdown(
            f"<style>{css_content}</style>",
            unsafe_allow_html=True,
        )

    else:

        st.warning(
            "The stylesheet styles/style.css could not be found."
        )


load_css()


# ============================================================
# INITIALIZE SESSION
# ============================================================

initialize_session()
initialize_movie_detail_state()


if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# CUSTOM SIDEBAR
# ============================================================

sidebar()


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.get("page", "Home")


# ============================================================
# HOME
# ============================================================

if page == "Home":

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🎬 Movies", "4,800+")
    c2.metric("⭐ Genres", "20+")
    c3.metric("🤖 AI", "Cosine Similarity")
    c4.metric("⚡ Speed", "Instant")

    st.divider()

    movies, similarity = load_models()

    home_page(
        movies,
        similarity,
    )


# ============================================================
# SEARCH
# ============================================================

elif page == "Search":

    search_page()


# ============================================================
# TRENDING
# ============================================================

elif page == "Trending":

    trending_page()


# ============================================================
# TOP RATED
# ============================================================

elif page == "Top Rated":

    top_rated_page()


# ============================================================
# UPCOMING
# ============================================================

elif page == "Upcoming":

    upcoming_page()


# ============================================================
# FAVORITES
# ============================================================

elif page == "Favorites":

    favorites_page()


# ============================================================
# RECENTLY VIEWED
# ============================================================

elif page == "Recently Viewed":

    recent_page()

    selected_movie = st.session_state.get(
        "selected_movie_details"
    )

    if (
        selected_movie
        and st.session_state.get("details_page")
        == "Recently Viewed"
    ):

        st.divider()

        movie_details(
            selected_movie,
            st.session_state.get(
                "selected_cast",
                [],
            ),
        )


# ============================================================
# INVALID PAGE FALLBACK
# ============================================================

else:

    st.session_state.page = "Home"

    st.info(
        "Page not found. Returning to Home."
    )

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <hr>

    <div class="footer">
        © 2026 CineMatch AI
        <br>
        Built with ❤️ by Shashank Sangam
        <br><br>
        Powered by Python • Streamlit • Scikit-learn • TMDB
    </div>
    """,
    unsafe_allow_html=True,
)
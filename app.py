import streamlit as st


from components.navbar import navbar

from pages.home_page import home_page
from pages.trending_page import trending_page
from pages.top_rated_page import top_rated_page
from pages.upcoming_page import upcoming_page
from pages.favorites_page import favorites_page
from pages.search_page import search_page

from services.model_loader import load_models

from utils.session import initialize_session

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="🎬 CineMatch AI",
    page_icon="🎬",
    layout="wide"
)

# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ============================================================
# SESSION
# ============================================================

initialize_session()

# ============================================================
# LOAD MODELS
# ============================================================

movies, similarity = load_models()

# ============================================================
# NAVBAR
# ============================================================

navbar()


# ============================================================
# HERO
# ============================================================



# ============================================================
# PAGE ROUTER
# ============================================================

page = st.session_state.page

if page == "Home":


     # Statistics only on Home
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🎬 Movies", "4,800+")
    c2.metric("⭐ Genres", "20+")
    c3.metric("🤖 AI", "Cosine Similarity")
    c4.metric("⚡ Speed", "Instant")

    st.divider()


    home_page(
        movies,
        similarity
    )

elif page == "Trending":

    trending_page()

elif page == "Top Rated":

    top_rated_page()

elif page == "Upcoming":

    upcoming_page()

elif page == "Favorites":

    favorites_page()

elif page == "Search":

    search_page()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 CineMatch AI")

    st.markdown("""
🎬 Content Based Recommendation

🖼️ TMDB Posters

⚡ Fast Recommendation

🤖 Machine Learning Powered

🌟 Netflix Inspired UI

Version 7.6
""")

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
unsafe_allow_html=True
)

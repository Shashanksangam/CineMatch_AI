import streamlit as st


def initialize_session():

    defaults = {

        # Navigation
        "page": "Home",

        # Recommendation System
        "recommendations": [],

        # Selected Movie
        "selected_movie_details": None,

        "selected_cast": [],

        # Pagination
        "trend_page": 1,

        "top_page": 1,

        "upcoming_page": 1,

        # Favorites
        "favorites": [],

        # Search
        "search_results": [],

        # Analytics

        "analytics_loaded": False

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value
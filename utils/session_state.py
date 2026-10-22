import streamlit as st


def clear_movie_details():
    """
    Completely closes the currently opened movie details.
    """

    st.session_state.selected_movie_details = None
    st.session_state.selected_cast = []
    st.session_state.details_page = None
    st.session_state.details_movie_id = None


def initialize_movie_detail_state():
    """
    Initializes movie-detail session state safely.
    """

    if "selected_movie_details" not in st.session_state:
        st.session_state.selected_movie_details = None

    if "selected_cast" not in st.session_state:
        st.session_state.selected_cast = []

    if "details_page" not in st.session_state:
        st.session_state.details_page = None

    if "details_movie_id" not in st.session_state:
        st.session_state.details_movie_id = None


def initialize_search_state():

    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

    if "search_history" not in st.session_state:
        st.session_state.search_history = []
    
    if "search_submitted" not in st.session_state:

        st.session_state.search_submitted = False

    # Keep only the latest 10 searches
    st.session_state.search_history = (
        st.session_state.search_history[:10]
    )
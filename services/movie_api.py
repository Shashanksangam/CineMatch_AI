import requests
import streamlit as st

from services.tmdb_service import (
    BASE_URL,
    API_KEY,
    session,
    tmdb_request
)


# ==========================================================
# SEARCH MOVIES
# ==========================================================

@st.cache_data(
    ttl=900,
    show_spinner=False
)
def search_movie(query):

    query = query.strip()

    if not query:
        return []

    data = tmdb_request(
        "/search/movie",
        {
            "query": query
        }
    )

    if not data:
        return []

    return data.get(
        "results",
        []
    )


# ==========================================================
# TRENDING
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_trending():

    data = tmdb_request(
        "/trending/movie/week"
    )

    if not data:
        return []

    return data.get(
        "results",
        []
    )


# ==========================================================
# TRENDING PAGE
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_trending_page(page=1):

    data = tmdb_request(
        "/trending/movie/week",
        {
            "page": page
        }
    )

    if not data:
        return {}

    return data


# ==========================================================
# NOW PLAYING
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_now_playing():

    data = tmdb_request(
        "/movie/now_playing"
    )

    if not data:
        return []

    return data.get(
        "results",
        []
    )


# ==========================================================
# TOP RATED
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_top_rated(page=1):

    data = tmdb_request(
        "/movie/top_rated",
        {
            "page": page
        }
    )

    if not data:
        return {}

    return data


# ==========================================================
# UPCOMING
# ==========================================================

@st.cache_data(
    ttl=900,
    show_spinner=False
)
def get_upcoming(page=1):

    data = tmdb_request(
        "/movie/upcoming",
        {
            "page": page
        }
    )

    if not data:
        return {}

    return data
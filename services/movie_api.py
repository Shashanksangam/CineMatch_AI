import requests
import streamlit as st

from services.tmdb_service import (
    BASE_URL,
    API_KEY,
    session,
    tmdb_request
)






# ==========================================================
# SEARCH MOVIE
# ==========================================================


@st.cache_data(show_spinner=False)
def search_movie(query):

    url = f"{BASE_URL}/search/movie"

    params = {

        "api_key": API_KEY,

        "language": "en-US",

        "query": query

    }

    try:

        response = session.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json().get("results", [])

    except Exception as e:

        st.error(e)

        return {}
    

# ==========================================================
# TRENDING
# ==========================================================

@st.cache_data(show_spinner=False)
def get_trending():

    data = tmdb_request("/trending/movie/week")

    if not data:

        return []

    return data.get("results", [])


# ==========================================================
# NOW PLAYING
# ==========================================================

@st.cache_data(show_spinner=False)
def get_now_playing():

    data = tmdb_request("/movie/now_playing")

    if not data:

        return []

    return data.get("results", [])



@st.cache_data(show_spinner=False)
def get_trending_page(page=1):

    url = f"{BASE_URL}/trending/movie/week"

    params = {

        "api_key": API_KEY,

        "language": "en-US",

        "page": page

    }

    try:

        response = session.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(e)

        return {}
    



# ==========================================================
# GET_TOP_RATED MOVIES
# ==========================================================

@st.cache_data(show_spinner=False)
def get_top_rated(page=1):

    url = f"{BASE_URL}/movie/top_rated"

    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "page": page
    }

    try:

        response = session.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(e)

        return {}
    



# ==========================================================
# UPCOMING MOVIES
# ==========================================================

@st.cache_data(show_spinner=False)
def get_upcoming(page=1):

    url = f"{BASE_URL}/movie/upcoming"

    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "page": page
    }

    try:

        response = session.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(e)

        return {}
import requests
import streamlit as st

# ==========================================================
# TMDB CONFIG
# ==========================================================

API_KEY = "98afe88a15d00a4fa4be42a36fd842f3"

BASE_URL = "https://api.themoviedb.org/3"

IMAGE_URL = "https://image.tmdb.org/t/p/w500"

PLACEHOLDER = (
    "https://via.placeholder.com/500x750?text=No+Poster"
)

session = requests.Session()


# ==========================================================
# INTERNAL REQUEST FUNCTION
# ==========================================================

@st.cache_data(show_spinner=False)
def tmdb_request(endpoint: str):

    url = f"{BASE_URL}{endpoint}"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
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

        return None


# ==========================================================
# GET MOVIE DETAILS
# ==========================================================

@st.cache_data(show_spinner=False)
def get_movie_details(movie_id):

    data = tmdb_request(f"/movie/{movie_id}")

    if not data:
        return None

    return {

        "id": movie_id,

        "title": data.get("title", "Unknown"),

        "overview": data.get(
            "overview",
            "No description available."
        ),

        "poster": (
            IMAGE_URL + data["poster_path"]
            if data.get("poster_path")
            else PLACEHOLDER
        ),

        "backdrop": (
            "https://image.tmdb.org/t/p/original"
            + data["backdrop_path"]
            if data.get("backdrop_path")
            else None
        ),

        "rating": round(
            data.get("vote_average", 0),
            1
        ),

        "votes": data.get(
            "vote_count",
            0
        ),

        "runtime": data.get(
            "runtime",
            0
        ),

        "release_date": data.get(
            "release_date",
            ""
        ),

        "status": data.get(
            "status",
            ""
        ),

        "tagline": data.get(
            "tagline",
            ""
        ),

        "budget": data.get(
            "budget",
            0
        ),

        "revenue": data.get(
            "revenue",
            0
        ),

        "homepage": data.get(
            "homepage",
            ""
        ),

        "language": data.get(
            "original_language",
            ""
        ),

        "genres": [

            genre["name"]

            for genre in data.get(
                "genres",
                []
            )

        ],

        "companies": [

            company["name"]

            for company in data.get(
                "production_companies",
                []
            )

        ]

    }


# ==========================================================
# POSTER ONLY
# ==========================================================

@st.cache_data(show_spinner=False)
def get_poster(movie_id):

    details = get_movie_details(movie_id)

    print(movie_id)
    print(details)

    return details.get("poster", PLACEHOLDER)


# ==========================================================
# TRAILER
# ==========================================================

@st.cache_data(show_spinner=False)
def get_trailer(movie_id):

    data = tmdb_request(f"/movie/{movie_id}/videos")

    if not data:

        return None

    for video in data.get("results", []):

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
        ):

            return (
                "https://www.youtube.com/watch?v="
                + video["key"]
            )

    return None


# ==========================================================
# CAST
# ==========================================================

@st.cache_data(show_spinner=False)
def get_cast(movie_id, limit=5):

    data = tmdb_request(f"/movie/{movie_id}/credits")

    if not data:

        return []

    cast = []

    for actor in data.get("cast", [])[:limit]:

        cast.append(

            {

                "name": actor["name"],

                "character": actor["character"],

                "photo":

                (
                    IMAGE_URL + actor["profile_path"]

                    if actor.get("profile_path")

                    else None

                )

            }

        )

    return cast


# ==========================================================
# DIRECTOR
# ==========================================================

@st.cache_data(show_spinner=False)
def get_director(movie_id):

    data = tmdb_request(f"/movie/{movie_id}/credits")

    if not data:

        return "Unknown"

    for crew in data.get("crew", []):

        if crew.get("job") == "Director":

            return crew.get("name")

    return "Unknown"



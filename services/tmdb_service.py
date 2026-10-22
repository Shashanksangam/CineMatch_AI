import requests
import streamlit as st


# ==========================================================
# TMDB CONFIG
# ==========================================================

API_KEY = "98afe88a15d00a4fa4be42a36fd842f3"

BASE_URL = "https://api.themoviedb.org/3"

IMAGE_URL = "https://image.tmdb.org/t/p/w500"

BACKDROP_URL = "https://image.tmdb.org/t/p/original"

PLACEHOLDER = (
    "https://placehold.co/500x750?text=No+Poster"
)

session = requests.Session()


# ==========================================================
# INTERNAL REQUEST
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def tmdb_request(endpoint: str, params=None):

    url = f"{BASE_URL}{endpoint}"

    request_params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    if params:
        request_params.update(params)

    try:

        response = session.get(
            url,
            params=request_params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None

    except Exception:

        return None


# ==========================================================
# MOVIE DETAILS
#
# ONE REQUEST:
# details + videos + credits
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_movie_details(movie_id):

    data = tmdb_request(
        f"/movie/{movie_id}",
        {
            "append_to_response": "videos,credits"
        }
    )

    if not data:
        return None

    # ------------------------------------------------------
    # GENRES
    # ------------------------------------------------------

    genres = [
        genre.get("name", "")
        for genre in data.get("genres", [])
        if genre.get("name")
    ]

    # ------------------------------------------------------
    # PRODUCTION COMPANIES
    # ------------------------------------------------------

    companies = [
        company.get("name", "")
        for company in data.get(
            "production_companies",
            []
        )
        if company.get("name")
    ]

    # ------------------------------------------------------
    # TRAILER
    # ------------------------------------------------------

    trailer = None

    videos = data.get(
        "videos",
        {}
    ).get(
        "results",
        []
    )

    for video in videos:

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
        ):

            trailer = (
                "https://www.youtube.com/watch?v="
                + video.get("key", "")
            )

            break

    # ------------------------------------------------------
    # CAST
    # ------------------------------------------------------

    cast = []

    tmdb_cast = data.get(
        "credits",
        {}
    ).get(
        "cast",
        []
    )

    for actor in tmdb_cast[:5]:

        profile_path = actor.get(
            "profile_path"
        )

        photo = (
            IMAGE_URL + profile_path
            if profile_path
            else None
        )

        cast.append(
            {
                "name": actor.get(
                    "name",
                    "Unknown"
                ),

                "character": actor.get(
                    "character",
                    "Unknown"
                ),

                "photo": photo
            }
        )

    # ------------------------------------------------------
    # RETURN STANDARD MOVIE OBJECT
    # ------------------------------------------------------

    return {

        "id": movie_id,

        "movie_id": movie_id,

        "title": data.get(
            "title",
            "Unknown"
        ),

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
            BACKDROP_URL + data["backdrop_path"]
            if data.get("backdrop_path")
            else None
        ),

        "rating": round(
            data.get(
                "vote_average",
                0
            ),
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

        "genres": genres,

        "companies": companies,

        "trailer": trailer,

        "cast": cast

    }


# ==========================================================
# POSTER
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_poster(movie_id):

    details = get_movie_details(movie_id)

    if not details:
        return PLACEHOLDER

    return details.get(
        "poster",
        PLACEHOLDER
    )


# ==========================================================
# TRAILER
#
# IMPORTANT:
# NO NEW API REQUEST
#
# Uses cached movie details.
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_trailer(movie_id):

    details = get_movie_details(movie_id)

    if not details:
        return None

    return details.get(
        "trailer"
    )


# ==========================================================
# CAST
#
# IMPORTANT:
# NO NEW API REQUEST
#
# Uses cached movie details.
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_cast(movie_id, limit=5):

    details = get_movie_details(movie_id)

    if not details:
        return []

    return details.get(
        "cast",
        []
    )[:limit]


# ==========================================================
# DIRECTOR
#
# Uses the credits already included in movie details.
# ==========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_director(movie_id):

    data = tmdb_request(
        f"/movie/{movie_id}",
        {
            "append_to_response": "credits"
        }
    )

    if not data:
        return "Unknown"

    crew = data.get(
        "credits",
        {}
    ).get(
        "crew",
        []
    )

    for person in crew:

        if person.get("job") == "Director":

            return person.get(
                "name",
                "Unknown"
            )

    return "Unknown"


@st.cache_data(ttl=1800, show_spinner=False)
def get_watch_providers(movie_id, country_code="IN"):
    """
    Get streaming, free, rental and purchase options
    for a movie in the requested country.
    """
    data = tmdb_request(
        f"/movie/{movie_id}/watch/providers"
    )

    if not data:
        return None

    country_data = (
        data.get("results", {}).get(country_code.upper())
    )

    if not country_data:
        return {
            "link": None,
            "flatrate": [],
            "free": [],
            "ads": [],
            "rent": [],
            "buy": [],
        }

    categories = {}

    for category in (
        "flatrate",
        "free",
        "ads",
        "rent",
        "buy",
    ):
        categories[category] = country_data.get(
            category, []
        ) or []

    return {
        "link": country_data.get("link"),
        **categories,
    }

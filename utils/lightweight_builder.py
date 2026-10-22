from services.tmdb_service import IMAGE_URL, PLACEHOLDER


def build_light_movie(movie):

    poster = (
        IMAGE_URL + movie["poster_path"]
        if movie.get("poster_path")
        else PLACEHOLDER
    )

    backdrop = (
        "https://image.tmdb.org/t/p/original"
        + movie["backdrop_path"]
        if movie.get("backdrop_path")
        else None
    )

    return {

        "movie_id": movie["id"],

        "title": movie.get("title", ""),

        "poster": poster,

        "backdrop": backdrop,

        "overview": movie.get("overview", ""),

        "rating": round(
            movie.get("vote_average", 0),
            1
        ),

        "votes": movie.get("vote_count", 0),

        "release_date": movie.get(
            "release_date",
            ""
        ),

        "language": movie.get(
            "original_language",
            ""
        ),

        "runtime": None,

        "genres": [],

        "homepage": "",

        "trailer": None,

        "cast": []

    }
from services.tmdb_service import (
    get_movie_details,
    get_trailer,
    get_cast
)


def build_movie(movie):

    movie_id = movie["id"]

    details = get_movie_details(movie_id)

    if not details:

        return None

    details["movie_id"] = movie_id

    details["title"] = movie.get(
        "title",
        details.get("title")
    )

    details["release_date"] = movie.get(
        "release_date",
        ""
    )

    details["trailer"] = get_trailer(movie_id)

    details["cast"] = get_cast(movie_id)

    return details
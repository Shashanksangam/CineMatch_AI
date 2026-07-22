import streamlit as st

from services.tmdb_service import (
    get_movie_details,
    get_trailer,
    get_cast
)


def recommend(

    movie,

    movies,

    similarity

):

    try:
        movie_index = movies[
            movies["title"] == movie
        ].index[0]

    except IndexError:

        st.error("Movie not found.")
        return []

    distances = similarity[movie_index]

    movies_list = sorted(

        list(enumerate(distances)),

        reverse=True,

        key=lambda x: x[1]

    )[1:6]

    recommendations = []

    for item in movies_list:

        index = item[0]

        movie_id = movies.iloc[index].movie_id

        details = get_movie_details(movie_id)

        if details:

            details["title"] = movies.iloc[index].title

            details["movie_id"] = movie_id

            details["trailer"] = get_trailer(movie_id)

            details["cast"] = get_cast(movie_id)

            recommendations.append(details)

    return recommendations
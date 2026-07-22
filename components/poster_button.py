import streamlit as st


def poster_button(movie):

    clicked = st.button(

        "",

        key=f"poster_{movie['movie_id']}",

        use_container_width=True,

        help=f"View details of {movie['title']}"

    )

    st.image(

        movie["poster"],

        use_container_width=True

    )

    return clicked
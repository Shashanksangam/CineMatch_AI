import streamlit as st

from services.favorites_service import (
    add_favorite,
    remove_favorite,
    is_favorite
)



def movie_card(movie):

    # -------------------------------------------------------
    # Poster
    # -------------------------------------------------------

    poster = movie.get("poster")

    if poster:
        st.image(poster, use_container_width=True)
    else:
        st.image(
        "https://placehold.co/500x750?text=No+Poster",
        use_container_width=True
    )

    # -------------------------------------------------------
    # Title
    # -------------------------------------------------------

    st.markdown(
        f"""
        <h4 style="
            text-align:center;
            margin-top:10px;
            margin-bottom:5px;
            color:white;
        ">
        {movie['title']}
        </h4>
        """,
        unsafe_allow_html=True
    )


    favorite = is_favorite(movie["movie_id"])

    if favorite:

        if st.button(
            "💔 Remove",
            key=f"remove_{movie['movie_id']}",
            use_container_width=True
        ):

            remove_favorite(movie["movie_id"])
            st.rerun()

    else:

        if st.button(
            "❤️ Favorite",
            key=f"fav_{movie['movie_id']}",
            use_container_width=True
        ):

            add_favorite(movie)
            st.rerun()

    # -------------------------------------------------------
    # Rating • Year • Runtime
    # -------------------------------------------------------

    rating = movie.get("rating", "N/A")

    release_date = movie.get("release_date", "")

    year = release_date if release_date else "Unknown"

    runtime = movie.get("runtime", "N/A")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric("⭐", rating)

    with c2:

        st.metric("📅", year)

    with c3:

        st.metric("⏱", runtime)

    # -------------------------------------------------------
    # Genres
    # -------------------------------------------------------

    genres = movie.get("genres", [])

    if genres:

        genre_text = " ".join(

            [f"`{g}`" for g in genres[:3]]

        )

        st.markdown(genre_text)

    # -------------------------------------------------------
    # Overview
    # -------------------------------------------------------

    overview = movie.get("overview", "")

    if overview:

        if len(overview) > 180:

            overview = overview[:180] + "..."

        with st.expander("📖 Story"):

            st.write(overview)

    # -------------------------------------------------------
    # Votes
    # -------------------------------------------------------

    votes = movie.get("votes", "")

    if votes:

        st.caption(f"👥 {votes:,} votes")

    # -------------------------------------------------------
    # Trailer
    # -------------------------------------------------------

    trailer = movie.get("trailer")

    if trailer:

        st.link_button(

            "▶ Watch Trailer",

            trailer,

            use_container_width=True

        )

    # -------------------------------------------------------
    # Homepage
    # -------------------------------------------------------

    homepage = movie.get("homepage")

    if homepage:

        st.link_button(
        "🌐 Official Website",
        homepage,
        use_container_width=True
    )

    else:

        st.caption("🌐 No Official Website")


#===========================================================
# DETAILS BUTTON
# ==========================================================
    
    
import streamlit as st


def movie_details(movie, cast=None):

    if cast is None:
        cast = []

    # -----------------------------------------------------
    # BACKDROP
    # -----------------------------------------------------

    backdrop = movie.get("backdrop")

    if backdrop:

        st.image(
            backdrop,
            use_container_width=True
        )

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    st.markdown(
        f"""
        <h1 style="
        margin-top:20px;
        color:white;
        ">
        {movie['title']}
        </h1>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # TAGLINE
    # -----------------------------------------------------

    if movie.get("tagline"):

        st.markdown(
            f"### *{movie['tagline']}*"
        )

    st.write("")

    # -----------------------------------------------------
    # MAIN INFO
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "⭐ Rating",
        movie.get("rating")
    )

    c2.metric(
        "⏱ Runtime",
        f"{movie.get('runtime')} min"
    )

    c3.metric(
        "📅 Release",
        movie.get("release_date")
    )

    c4.metric(
        "🌍 Language",
        movie.get("language", "").upper()
    )

    st.divider()

    # -----------------------------------------------------
    # GENRES
    # -----------------------------------------------------

    st.subheader("🎭 Genres")

    genres = movie.get("genres", [])

    if genres:

        st.markdown(
            " ".join(
                [
                    f"`{g}`"
                    for g in genres
                ]
            )
        )

    st.divider()

    # -----------------------------------------------------
    # STORY
    # -----------------------------------------------------

    st.subheader("📖 Story")

    st.write(movie.get("overview"))

    st.divider()

    # -----------------------------------------------------
    # BUDGET
    # -----------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "💰 Budget",
            f"${movie.get('budget',0):,}"
        )

    with c2:

        st.metric(
            "💵 Revenue",
            f"${movie.get('revenue',0):,}"
        )

    st.divider()

    # -----------------------------------------------------
    # PRODUCTION
    # -----------------------------------------------------

    companies = movie.get("companies", [])

    if companies:

        st.subheader("🏢 Production")

        for company in companies:

            st.write("•", company)

    st.divider()

    # -----------------------------------------------------
    # CAST
    # -----------------------------------------------------

    if cast:

        st.subheader("🎭 Top Cast")

        cols = st.columns(5)

        for col, actor in zip(cols, cast):

            with col:

                if actor["photo"]:

                    st.image(
                        actor["photo"],
                        use_container_width=True
                    )

                st.markdown(
                    f"**{actor['name']}**"
                )

                st.caption(
                    actor["character"]
                )

    st.divider()

    # -----------------------------------------------------
    # LINKS
    # -----------------------------------------------------

    if movie.get("homepage"):

        st.link_button(
            "🌐 Official Website",
            movie["homepage"],
            use_container_width=True
        )

    if movie.get("trailer"):

        st.link_button(
            "▶ Watch Trailer",
            movie["trailer"],
            use_container_width=True
        )

import streamlit as st

from components.movie_watch_providers import movie_watch_providers


def movie_details(movie, cast=None):
    if cast is None:
        cast = []

    # =====================================================
    # BACKDROP AND TITLE
    # =====================================================

    backdrop = movie.get("backdrop")

    if backdrop:
        st.image(
            backdrop,
            width="stretch",
        )

    st.markdown(
        f"""
        <h1 style="margin-top:20px;color:white;">
            {movie.get('title', 'Unknown Movie')}
        </h1>
        """,
        unsafe_allow_html=True,
    )

    if movie.get("tagline"):
        st.markdown(f"### *{movie['tagline']}*")

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    rating = movie.get("rating", 0)
    runtime = movie.get("runtime")
    release_date = movie.get("release_date", "")
    language = movie.get("language", "")

    c1.metric("⭐ Rating", rating if rating else "N/A")
    c2.metric(
        "⏱ Runtime",
        f"{runtime} min" if runtime else "N/A",
    )
    c3.metric(
        "📅 Release",
        release_date if release_date else "N/A",
    )
    c4.metric(
        "🌍 Language",
        language.upper() if language else "N/A",
    )

    # =====================================================
    # GENRES
    # =====================================================

    genres = movie.get("genres", [])

    if genres:
        st.divider()
        st.subheader("🎭 Genres")
        st.markdown(" ".join(f"`{genre}`" for genre in genres))

    # =====================================================
    # STORY
    # =====================================================

    st.divider()
    st.subheader("📖 Story")
    st.write(
        movie.get("overview")
        or "No description available."
    )

    # =====================================================
    # BUDGET AND REVENUE
    # =====================================================

    budget = movie.get("budget", 0)
    revenue = movie.get("revenue", 0)

    if budget or revenue:
        st.divider()

        c1, c2 = st.columns(2)

        c1.metric(
            "💰 Budget",
            f"${budget:,}" if budget else "N/A",
        )

        c2.metric(
            "💵 Revenue",
            f"${revenue:,}" if revenue else "N/A",
        )

    # =====================================================
    # PRODUCTION COMPANIES
    # =====================================================

    companies = movie.get("companies", [])

    if companies:
        st.divider()
        st.subheader("🏢 Production")

        st.write(" • ".join(companies))

    # =====================================================
    # CAST
    # =====================================================

    if cast:
        st.divider()
        st.subheader("🎭 Top Cast")

        cols = st.columns(min(5, len(cast)))

        for index, actor in enumerate(cast):
            with cols[index % len(cols)]:
                photo = actor.get("photo")

                if photo:
                    st.image(
                        photo,
                        width="stretch",
                    )

                st.markdown(
                    f"**{actor.get('name', 'Unknown')}**"
                )

                st.caption(
                    actor.get("character", "Unknown")
                )

    # =====================================================
    # TRAILER AND OFFICIAL WEBSITE
    # =====================================================

    homepage = movie.get("homepage")
    trailer = movie.get("trailer")

    if homepage or trailer:
        st.divider()
        st.subheader("🔗 More About This Movie")

        if homepage:
            st.link_button(
                "🌐 Official Website",
                homepage,
                width="stretch",
            )

        if trailer:
            st.link_button(
                "▶ Watch Trailer",
                trailer,
                width="stretch",
            )

    # =====================================================
    # STREAMING AVAILABILITY — INDIA
    # =====================================================

    movie_id = movie.get("movie_id") or movie.get("id")

    if movie_id:
        movie_watch_providers(
            movie_id=movie_id,
            country_code=st.session_state.get(
            "watch_country_code", "IN"
        ),
            movie_title=movie.get("title", ""),
        )
    else:
        st.info(
            "Streaming availability cannot be loaded "
            "because this movie has no TMDB ID."
        )

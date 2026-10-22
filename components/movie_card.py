import html
from urllib.parse import urlparse

import streamlit as st

from services.favorites_service import (
    add_favorite,
    remove_favorite,
    is_favorite,
)

from services.tmdb_service import get_movie_details

from utils.session_state import initialize_movie_detail_state


PLACEHOLDER_POSTER = (
    "https://placehold.co/500x750?text=No+Poster"
)


def valid_http_url(value):
    """Accept only valid HTTP/HTTPS URLs."""
    if not isinstance(value, str) or not value.strip():
        return False

    try:
        parsed = urlparse(value.strip())
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )
    except ValueError:
        return False


def empty_link_space():
    """Reserve space when an optional link is unavailable."""
    st.markdown(
        "<div style='height:40px;'></div>",
        unsafe_allow_html=True,
    )


def movie_card(movie):

    # =====================================================
    # 1. VALIDATE MOVIE
    # =====================================================

    if not isinstance(movie, dict):
        return

    movie_id = movie.get("movie_id")

    if movie_id is None:
        return

    title = str(movie.get("title") or "Unknown Movie")
    safe_title = html.escape(title)

    poster = movie.get("poster")

    rating = movie.get("rating")
    rating_text = (
        str(rating)
        if rating is not None and rating != ""
        else "N/A"
    )

    release_date = movie.get("release_date") or ""
    year = str(release_date)[:4] if release_date else "----"

    runtime = movie.get("runtime")
    runtime_text = (
        f"{runtime} min"
        if runtime is not None
        and str(runtime).strip() not in ("", "0")
        else "N/A"
    )

    genres = movie.get("genres") or []
    votes = movie.get("votes") or 0

    try:
        votes = int(votes)
    except (TypeError, ValueError):
        votes = 0

    trailer = movie.get("trailer")
    homepage = movie.get("homepage")

    trailer_available = valid_http_url(trailer)
    homepage_available = valid_http_url(homepage)

    # =====================================================
    # 2. MOVIE CARD CONTAINER
    # =====================================================

    with st.container(border=True):

        # -------------------------------------------------
        # POSTER
        # -------------------------------------------------

        if valid_http_url(poster):
            st.image(
                poster,
                width="stretch",
            )
        else:
            st.image(
                PLACEHOLDER_POSTER,
                width="stretch",
            )

        # -------------------------------------------------
        # TITLE - FIXED HEIGHT
        # -------------------------------------------------

        st.markdown(
            f"""
            <div style="
                height:82px;
                display:flex;
                align-items:center;
                justify-content:center;
                text-align:center;
                padding:4px 2px;
                box-sizing:border-box;
                overflow:hidden;
            ">
                <div style="
                    color:white;
                    font-size:18px;
                    font-weight:700;
                    line-height:1.35;
                    display:-webkit-box;
                    -webkit-box-orient:vertical;
                    -webkit-line-clamp:3;
                    overflow:hidden;
                    overflow-wrap:anywhere;
                ">
                    {safe_title}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # FAVORITES
        # -------------------------------------------------

        if is_favorite(movie_id):

            if st.button(
                "💔 Remove Favorite",
                key=f"remove_{movie_id}",
                width="stretch",
            ):
                remove_favorite(movie_id)
                st.rerun()

        else:

            if st.button(
                "❤️ Add to Favorites",
                key=f"fav_{movie_id}",
                width="stretch",
            ):
                add_favorite(movie)
                st.rerun()

        # -------------------------------------------------
        # RATING, YEAR AND RUNTIME
        # -------------------------------------------------

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div>⭐</div>
                    <div style="
                        font-size:13px;
                        font-weight:700;
                        overflow-wrap:anywhere;
                    ">{html.escape(rating_text)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with info_col2:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div>🗓️</div>
                    <div style="
                        font-size:13px;
                        font-weight:700;
                    ">{html.escape(year)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with info_col3:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div>⏱️</div>
                    <div style="
                        font-size:13px;
                        font-weight:700;
                        overflow-wrap:anywhere;
                    ">{html.escape(runtime_text)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # -------------------------------------------------
        # GENRES - RESERVED SPACE
        # -------------------------------------------------

        genre_html = ""

        if isinstance(genres, (list, tuple)):
            for genre in genres[:3]:
                if genre:
                    safe_genre = html.escape(str(genre))

                    genre_html += (
                        "<span style='"
                        "display:inline-block;"
                        "background:#252525;"
                        "color:#ffffff;"
                        "padding:5px 9px;"
                        "margin:3px 2px;"
                        "border-radius:18px;"
                        "font-size:10px;"
                        "font-weight:600;"
                        "white-space:nowrap;"
                        "'>"
                        f"{safe_genre}"
                        "</span>"
                    )

        st.markdown(
            f"""
            <div style="
                min-height:44px;
                display:flex;
                align-content:flex-start;
                justify-content:center;
                align-items:center;
                flex-wrap:wrap;
                text-align:center;
                margin-top:8px;
                margin-bottom:6px;
            ">
                {genre_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # VOTE COUNT
        # -------------------------------------------------

        if votes > 0:
            st.caption(f"👥 {votes:,} votes")
        else:
            st.caption("👥 Votes unavailable")

        # -------------------------------------------------
        # TRAILER - FIXED SLOT
        # -------------------------------------------------

        if trailer_available:
            st.link_button(
                "▶ Watch Trailer",
                trailer,
                width="stretch",
            )
        else:
            empty_link_space()

        # -------------------------------------------------
        # OFFICIAL WEBSITE - FIXED SLOT
        # -------------------------------------------------

        if homepage_available:
            st.link_button(
                "🌐 Official Website",
                homepage,
                width="stretch",
            )
        else:
            empty_link_space()

        # -------------------------------------------------
        # DETAILS BUTTON
        # -------------------------------------------------

        details_clicked = st.button(
            "ℹ️ View Details",
            key=f"details_{movie_id}",
            width="stretch",
        )

        # -------------------------------------------------
        # LOAD MOVIE DETAILS
        # -------------------------------------------------

        if details_clicked:

            initialize_movie_detail_state()

            # Clear previously selected movie
            st.session_state.selected_movie_details = None
            st.session_state.selected_cast = []
            st.session_state.details_movie_id = None
            st.session_state.details_page = None

            with st.spinner("Loading movie details..."):
                details = get_movie_details(movie_id)

            if not details:
                st.warning(
                    "Unable to load movie details. Please try again."
                )
                return

            # Preserve the selected movie's identity
            details["movie_id"] = movie_id
            details["title"] = title

            current_page = st.session_state.get(
                "page",
                "Home",
            )

            # Save selected movie and cast.
            st.session_state.selected_movie_details = details
            st.session_state.selected_cast = details.get("cast") or []
            st.session_state.details_movie_id = movie_id
            st.session_state.details_page = current_page

            # Update recently viewed movies.
            if "recent_movies" not in st.session_state:
                st.session_state.recent_movies = []

            recent_movies = [
                item
                for item in st.session_state.recent_movies
                if item.get("movie_id") != movie_id
            ]

            recent_movies.insert(0, movie)
            st.session_state.recent_movies = recent_movies[:10]

            st.rerun()
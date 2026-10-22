
import streamlit as st
from urllib.parse import quote_plus

from services.tmdb_service import get_watch_providers


PROVIDER_LOGO_BASE = "https://image.tmdb.org/t/p/w92"


def render_provider_group(title, providers, category):
    """Display one category of viewing providers."""

    if not providers:
        return

    seen = set()
    unique_providers = []

    for provider in providers:
        provider_id = provider.get("provider_id")

        if provider_id is None:
            continue

        if provider_id not in seen:
            seen.add(provider_id)
            unique_providers.append(provider)

    if not unique_providers:
        return

    st.markdown(f"### {title}")

    columns = st.columns(min(4, len(unique_providers)))

    for index, provider in enumerate(unique_providers):
        with columns[index % len(columns)]:
            logo_path = provider.get("logo_path")
            provider_name = provider.get(
                "provider_name", "Streaming provider"
            )

            if logo_path:
                st.image(
                    PROVIDER_LOGO_BASE + logo_path,
                    width=64,
                )

            st.markdown(f"**{provider_name}**")

            if category == "flatrate":
                st.caption("Subscription")
            elif category == "free":
                st.caption("Free")
            elif category == "ads":
                st.caption("Free with ads")
            elif category == "rent":
                st.caption("Rent")
            elif category == "buy":
                st.caption("Buy")


def movie_watch_providers(
    movie_id,
    country_code="IN",
    movie_title="",
):
    """Display regional streaming options and search fallback."""

    st.divider()
    st.subheader("📺 Where to Watch")

    country_names = {
        "IN": "India",
        "US": "United States",
        "GB": "United Kingdom",
        "CA": "Canada",
        "AU": "Australia",
    }

    country_code = country_code.upper()
    country_name = country_names.get(
        country_code, country_code
    )

    st.caption(f"Viewing options for {country_name}")

    with st.spinner("Checking viewing availability..."):
        data = get_watch_providers(
            movie_id,
            country_code,
        )

    if data is None:
        st.warning(
            "Streaming availability could not be retrieved. "
            "Please try again later."
        )
        return

    groups = [
        ("📡 Included with Subscription", "flatrate"),
        ("🆓 Free Streaming", "free"),
        ("📺 Free with Advertisements", "ads"),
        ("🎟️ Available to Rent", "rent"),
        ("🛒 Available to Buy", "buy"),
    ]

    has_providers = False

    # Display provider categories returned by TMDB.
    for title, category in groups:
        providers = data.get(category, []) or []

        if providers:
            has_providers = True

            render_provider_group(
                title,
                providers,
                category,
            )

        elif category == "free":
            st.markdown(f"### {title}")
            st.info(
                f"No free-streaming provider was found in our "
                f"current listings for {country_name}. "
                "This does not mean that no legal free viewing "
                "option exists."
            )

        elif category == "ads":
            st.markdown(f"### {title}")
            st.info(
                f"No ad-supported provider was found in our "
                f"current listings for {country_name}. "
                "Other viewing options may exist."
            )

    # Link supplied by TMDB for the movie's viewing options.
    watch_link = data.get("link")

    if watch_link:
        st.link_button(
            "🔗 View All Viewing Options",
            watch_link,
            width="stretch",
        )

    # If free options are missing, offer a movie-specific
    # JustWatch search as an additional place to check.
    free_providers = data.get("free", []) or []
    ad_providers = data.get("ads", []) or []

    if not free_providers and not ad_providers:
        if movie_title and movie_title.strip():
            justwatch_regions = {
                "IN": "in",
                "US": "us",
                "GB": "uk",
                "CA": "ca",
                "AU": "au",
            }

            region = justwatch_regions.get(
                country_code, country_code.lower()
            )

            search_query = quote_plus(movie_title.strip())

            justwatch_url = (
                f"https://www.justwatch.com/{region}/search"
                f"?q={search_query}"
            )

            st.link_button(
                "🔎 Check Free Options on JustWatch",
                justwatch_url,
                width="stretch",
            )

    if not has_providers:
        st.info(
            f"Our current listings do not confirm any viewing "
            f"providers for this movie in {country_name}. "
            "This does not prove that the movie is unavailable "
            "to watch legally."
        )

    st.caption(
        "Availability may change. Confirm current prices and "
        "subscription requirements with the provider."
    )

    st.caption(
        "Streaming availability data powered by JustWatch via TMDB."
    )

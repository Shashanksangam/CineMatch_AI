
import streamlit as st
from streamlit.components.v1 import html as components_html

from utils.session_state import clear_movie_details


# ============================================================
# DESKTOP HOVER + MOBILE TAP SIDEBAR CONTROLLER
# ============================================================

SIDEBAR_HOVER_SCRIPT = r"""
<!DOCTYPE html>
<html>
<body>
<script>
(function () {
    "use strict";

    let doc;
    try {
        doc = window.parent.document;
    } catch (error) {
        return;
    }

    // New controller version, so a previous controller won't block it.
    const GUARD = "__cinematchSidebarControllerV2";

    if (doc[GUARD]) {
        return;
    }
    doc[GUARD] = true;

    const EDGE_WIDTH = 36;
    const OPEN_DELAY = 120;
    const CLOSE_DELAY = 220;

    let openTimer = null;
    let closeTimer = null;

    function getSidebar() {
        return doc.querySelector(
            'section[data-testid="stSidebar"]'
        );
    }

    function isSidebarOpen() {
        const sidebar = getSidebar();

        return Boolean(
            sidebar &&
            sidebar.getAttribute("aria-expanded") === "true"
        );
    }

    function findControl(shouldOpen) {
        const selectors = shouldOpen
            ? [
                '[data-testid="stExpandSidebarButton"]',
                '[data-testid="collapsedControl"]',
                'button[aria-label*="Open sidebar" i]',
                'button[title*="Open sidebar" i]'
              ]
            : [
                '[data-testid="stSidebarCollapseButton"]',
                'button[aria-label*="Close sidebar" i]',
                'button[title*="Close sidebar" i]'
              ];

        for (const selector of selectors) {
            const element = doc.querySelector(selector);

            if (!element) {
                continue;
            }

            if (element.tagName === "BUTTON") {
                return element;
            }

            const nestedButton = element.querySelector("button");

            if (nestedButton) {
                return nestedButton;
            }

            // Some Streamlit versions attach the click handler
            // to the control wrapper instead of the inner button.
            return element;
        }

        return null;
    }

    function setSidebarOpen(shouldOpen) {
        if (isSidebarOpen() === shouldOpen) {
            return;
        }

        const control = findControl(shouldOpen);

        if (control) {
            control.click();
        }
    }

    function cancelOpenTimer() {
        if (openTimer !== null) {
            clearTimeout(openTimer);
            openTimer = null;
        }
    }

    function cancelCloseTimer() {
        if (closeTimer !== null) {
            clearTimeout(closeTimer);
            closeTimer = null;
        }
    }

    function scheduleOpen() {
        if (isSidebarOpen() || openTimer !== null) {
            return;
        }

        cancelCloseTimer();

        openTimer = setTimeout(function () {
            openTimer = null;
            setSidebarOpen(true);
        }, OPEN_DELAY);
    }

    function scheduleClose(delay = CLOSE_DELAY) {
        if (!isSidebarOpen() || closeTimer !== null) {
            return;
        }

        cancelOpenTimer();

        closeTimer = setTimeout(function () {
            closeTimer = null;
            setSidebarOpen(false);
        }, delay);
    }

    function isSidebarControl(target) {
        return Boolean(
            target &&
            target.closest &&
            target.closest(
                '[data-testid="stExpandSidebarButton"],' +
                '[data-testid="collapsedControl"],' +
                '[data-testid="stSidebarCollapseButton"],' +
                'button[aria-label*="sidebar" i]'
            )
        );
    }

    // DESKTOP: hover at the left edge to open.
    doc.addEventListener("pointermove", function (event) {
        if (event.pointerType === "touch") {
            return;
        }

        const sidebar = getSidebar();

        if (!sidebar) {
            return;
        }

        if (!isSidebarOpen()) {
            if (event.clientX <= EDGE_WIDTH) {
                scheduleOpen();
            }
            return;
        }

        const rect = sidebar.getBoundingClientRect();

        if (event.clientX <= rect.right + 8) {
            cancelCloseTimer();
        } else {
            scheduleClose();
        }
    }, true);

    // MOBILE: tap the left edge to open; tap outside to close.
    doc.addEventListener("pointerdown", function (event) {
        const sidebar = getSidebar();

        if (!sidebar) {
            return;
        }

        if (!isSidebarOpen()) {
            if (
                event.pointerType === "touch" &&
                event.clientX <= EDGE_WIDTH &&
                !isSidebarControl(event.target)
            ) {
                cancelOpenTimer();
                setSidebarOpen(true);
            }
            return;
        }

        if (
            sidebar.contains(event.target) ||
            isSidebarControl(event.target)
        ) {
            return;
        }

        scheduleClose(120);
    }, true);

})();
</script>
</body>
</html>
"""

def navigate_to(page_name):
    """Switch pages and clear details belonging to the previous page."""
    clear_movie_details()
    st.session_state.page = page_name
    st.rerun()


def navigation_button(label, page_name):
    """Render a sidebar navigation button."""
    current_page = st.session_state.get("page", "Home")
    is_active = current_page == page_name

    button_key = "sidebar_" + page_name.lower().replace(" ", "_")

    if st.button(
        label,
        key=button_key,
        type="primary" if is_active else "secondary",
        width="stretch",
    ):
        navigate_to(page_name)


def sidebar():
    # Install the browser interaction controller once.
    # It controls the shared sidebar used throughout the app.
    components_html(
        SIDEBAR_HOVER_SCRIPT,
        height=1,
        width=1,
        scrolling=False,
    )

    # ========================================================
    # SIDEBAR STYLING
    # ========================================================

    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            background: #101116;
            border-right: 1px solid #282a32;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }

        section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
            min-height: 44px !important;
            height: auto !important;
            padding: 10px 12px !important;
            border-radius: 10px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            transition: background 0.2s ease;
        }

        section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"] {
            background: #181a21 !important;
            color: #dedee5 !important;
            border: 1px solid #292c35 !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: #292c35 !important;
            border-color: #e50914 !important;
            color: white !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
            background: #e50914 !important;
            color: white !important;
            border: 1px solid #e50914 !important;
        }

        .cinematch-sidebar-logo {
            font-size: 25px;
            font-weight: 800;
            color: white;
            line-height: 1.3;
        }

        .cinematch-sidebar-caption {
            color: #a5a7b0;
            font-size: 12px;
            margin-top: 5px;
            margin-bottom: 20px;
        }

        .cinematch-sidebar-section {
            color: #9295a2;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.4px;
            margin-top: 15px;
            margin-bottom: 8px;
        }

        .cinematch-sidebar-footer {
            color: #9295a2;
            font-size: 12px;
            text-align: center;
            padding: 12px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # SIDEBAR CONTENT
    # ========================================================

    with st.sidebar:
        st.markdown(
            """
            <div class="cinematch-sidebar-logo">
                🎬 CineMatch AI
            </div>
            <div class="cinematch-sidebar-caption">
                Discover your next favourite movie.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # DISCOVER
        st.markdown(
            '<div class="cinematch-sidebar-section">DISCOVER</div>',
            unsafe_allow_html=True,
        )

        navigation_button("🏠  Home", "Home")
        navigation_button("🔍  Search Movies", "Search")
        navigation_button("🔥  Trending", "Trending")
        navigation_button("⭐  Top Rated", "Top Rated")
        navigation_button("🎥  Upcoming", "Upcoming")

        st.divider()

        # STREAMING REGION / PREFERENCES
        st.markdown(
            '<div class="cinematch-sidebar-section">PREFERENCES</div>',
            unsafe_allow_html=True,
        )

        country_codes = {
            "India": "IN",
            "United States": "US",
            "United Kingdom": "GB",
            "Canada": "CA",
            "Australia": "AU",
        }

        selected_country = st.selectbox(
            "🌍 Streaming Country",
            options=list(country_codes.keys()),
            index=0,
            key="watch_country_name",
            help="Choose the country to check movie streaming availability.",
        )

        st.session_state["watch_country_code"] = country_codes[
            selected_country
        ]

        st.divider()

        # PERSONAL LIBRARY
        st.markdown(
            '<div class="cinematch-sidebar-section">MY LIBRARY</div>',
            unsafe_allow_html=True,
        )

        navigation_button("❤️  Favorites", "Favorites")
        navigation_button("🕘  Recently Viewed", "Recently Viewed")

        st.divider()

        # PROJECT INFORMATION
        st.markdown(
            '<div class="cinematch-sidebar-section">ABOUT</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="
                color:#c2c4cd;
                font-size:13px;
                line-height:1.9;
            ">
                🎯 Content-based recommendations<br>
                🖼️ TMDB movie information<br>
                ⚡ Cached movie data<br>
                🤖 Machine learning powered
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown(
            """
            <div class="cinematch-sidebar-footer">
                CineMatch AI · Version 8.6<br>
                Built with ❤️ using Streamlit
            </div>
            """,
            unsafe_allow_html=True,
        )

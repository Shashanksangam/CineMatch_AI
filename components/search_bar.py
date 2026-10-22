from pathlib import Path

import streamlit.components.v1 as components


# Locate the custom HTML component relative to this file.
COMPONENT_DIR = (
    Path(__file__).resolve().parent
    / "search_component"
)

cinematch_search_component = components.declare_component(
    "cinematch_search_component",
    path=str(COMPONENT_DIR),
)


def search_bar():
    """Render the custom search bar and return submitted text."""

    value = cinematch_search_component(
        key="cinematch_search_bar",
        default="",
    )

    if not isinstance(value, str):
        return ""

    return value.strip()
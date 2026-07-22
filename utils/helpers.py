import streamlit as st


def section_title(title):

    st.markdown(f"## {title}")


def horizontal_line():

    st.divider()


def show_error(message):

    st.error(message)


def show_success(message):

    st.success(message)


def show_warning(message):

    st.warning(message)
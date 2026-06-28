import streamlit as st
from config import APP_NAME, APP_TAGLINE, PAGE_TITLE, PAGE_ICON

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
)

st.title(APP_NAME)
st.subheader(APP_TAGLINE)

st.success("Phase 0 setup completed successfully! 🚀")
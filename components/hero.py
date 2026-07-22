import streamlit as st


def hero():
    st.markdown(
        """
        <div class="hero">
            <h1>🎬 CineMatch AI</h1>
            <h3>Discover Movies You'll Love</h3>
            <p>AI Powered Movie Recommendation Engine</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
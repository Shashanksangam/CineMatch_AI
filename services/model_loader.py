import pickle
import streamlit as st


@st.cache_resource
def load_models():

    movies = pickle.load(
        open("models/movies.pkl", "rb")
    )

    similarity = pickle.load(
        open("models/similarity.pkl", "rb")
    )

    return movies, similarity
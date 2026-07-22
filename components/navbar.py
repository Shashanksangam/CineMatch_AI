import streamlit as st


def navbar():

    c1,c2,c3,c4,c5,c6,c7 = st.columns(
        [2,1,1,1,1,1,1]
    )

    with c1:

        st.markdown("## 🎬 CineMatch AI")

    with c2:

        if st.button("🏠 Home",use_container_width=True):

            st.session_state.page="Home"

            st.rerun()

    with c3:

        if st.button("🔍 Search",use_container_width=True):

            st.session_state.page="Search"

            st.rerun()

    with c4:

        if st.button("🔥 Trending",use_container_width=True):

            st.session_state.page="Trending"

            st.rerun()

    with c5:

        if st.button("⭐ Top Rated",use_container_width=True):

            st.session_state.page="Top Rated"

            st.rerun()

    with c6:

        if st.button("🎥 Upcoming",use_container_width=True):

            st.session_state.page="Upcoming"

            st.rerun()

    with c7:

        if st.button("❤️ Favorites",use_container_width=True):

            st.session_state.page="Favorites"

            st.rerun()

    st.divider()
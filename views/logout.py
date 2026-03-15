# views/logout.py
import streamlit as st

st.session_state.token = None
st.rerun()

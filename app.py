import streamlit as st
from engine import analyze_input

st.set_page_config(page_title="Pause AI")

st.title("⏸ Pause AI")
st.write("Clarity before AI")

user_input = st.text_area("Enter your prompt:")

if st.button("Analyze"):
    if user_input:
        result = analyze_input(user_input)
        st.json(result)
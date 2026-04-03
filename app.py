# app.py

import streamlit as st
from engine import analyze_input

# ============================
# PAGE CONFIG
# ============================

st.set_page_config(page_title="Pause AI", layout="centered")

st.title("⏸️ Pause AI")
st.caption("Clarity before action")

# ============================
# INPUT
# ============================

user_input = st.text_area("Enter your prompt:", height=150)

# ============================
# ACTION
# ============================

if st.button("Analyze"):

    result = analyze_input(user_input)

    intent = result.get("intent")

    # ============================
    # OUTPUT ROUTING
    # ============================

    if intent == "empty":
        st.warning(result["message"])

    elif intent == "non_decision":
        st.info(result["message"])

    elif intent == "low_stakes":
        st.success(result["message"])

    elif intent == "medium_stakes":
        st.warning(result["message"])

    elif intent == "high_stakes":
        st.error(result["message"])
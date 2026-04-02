import streamlit as st
from engine import analyze_input

st.set_page_config(page_title="Pause AI", layout="centered")

# ----------------------------
# Header
# ----------------------------
st.title("⏸️ Pause AI")
st.caption("Clarity before action")

# ----------------------------
# Input
# ----------------------------
user_input = st.text_area("Enter your prompt:", height=150)

# ----------------------------
# Analyze Button
# ----------------------------
if st.button("Analyze"):

    if not user_input.strip():
        st.warning("Please enter something first.")
    else:
        result = analyze_input(user_input)

        # ----------------------------
        # Score Display
        # ----------------------------
        score = result["score"]

        if score >= 80:
            st.success(f"Pause Score: {score} (Low Risk)")
        elif score >= 60:
            st.warning(f"Pause Score: {score} (Moderate Risk)")
        else:
            st.error(f"Pause Score: {score} (High Risk)")

        # ----------------------------
        # Type
        # ----------------------------
        st.subheader("Decision Type")
        st.write(result["type"])

        # ----------------------------
        # Signals
        # ----------------------------
        st.subheader("Signals Detected")

        if result["signals"]:
            for s in result["signals"]:
                st.write(f"- {s.replace('_', ' ').title()}")
        else:
            st.write("No major risk signals detected")

        # ----------------------------
        # Analysis (clean formatting)
        # ----------------------------
        st.subheader("Analysis")

        analysis_text = result["analysis"]

        # Fix formatting from LLM
        analysis_text = analysis_text.replace("\\n", "\n")

        st.markdown(f"```\n{analysis_text}\n```")
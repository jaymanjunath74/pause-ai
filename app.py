import streamlit as st
from engine import analyze_input

st.set_page_config(page_title="Pause AI", layout="centered")

st.title("⏸️ Pause AI")
st.caption("Clarity before action")

user_input = st.text_area("Enter your prompt:", height=150)

if st.button("Analyze"):

    if not user_input.strip():
        st.warning("Please enter something first.")
    else:
        result = analyze_input(user_input)

        score = result["score"]

        # Score
        if score >= 80:
            st.success(f"Pause Score: {score} (Low Risk)")
        elif score >= 50:
            st.warning(f"Pause Score: {score} (Moderate Risk)")
        else:
            st.error(f"Pause Score: {score} (High Risk)")

        # Type
        st.subheader("Decision Type")
        st.write(result["type"])

        # Decision Intelligence
        st.subheader("Decision Intelligence")

        col1, col2, col3 = st.columns(3)
        col1.metric("Weight", result.get("decision_weight", "N/A"))
        col2.metric("Reversibility", result.get("reversibility", "N/A"))
        col3.metric("Action", result.get("action", "N/A"))

        # Top Signals
        st.subheader("Key Drivers")

        for s in result.get("top_signals", []):
            st.write(f"- {s.replace('_', ' ').title()}")

        # Analysis
        st.subheader("Analysis")

        analysis = result["analysis"]

        st.markdown("**Reason:**")
        for r in analysis["reason"]:
            st.write(f"- {r}")

        st.markdown("**Recommendation:**")
        for r in analysis["recommendation"]:
            st.write(f"- {r}")
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

        score = result.get("score", 0)

        # ============================
        # SCORE DISPLAY
        # ============================

        if score >= 80:
            st.success(f"Pause Score: {score} (Low Risk)")
        elif score >= 50:
            st.warning(f"Pause Score: {score} (Moderate Risk)")
        else:
            st.error(f"Pause Score: {score} (High Risk)")

        # ============================
        # TYPE
        # ============================

        st.subheader("Decision Type")
        st.write(result.get("type", "N/A"))

        # ============================
        # DECISION INTELLIGENCE
        # ============================

        st.subheader("Decision Intelligence")

        col1, col2, col3 = st.columns(3)

        col1.metric("Weight", result.get("decision_weight", "N/A"))
        col2.metric("Reversibility", result.get("reversibility", "N/A"))
        col3.metric("Action", result.get("action", "N/A"))

        # ============================
        # KEY DRIVERS
        # ============================

        st.subheader("Key Drivers")

        for s in result.get("top_signals", []):
            st.write(f"- {s.replace('_', ' ').title()}")

        # ============================
        # QUESTIONS (NEW 🔥)
        # ============================

        st.subheader("Questions to Consider")

        questions = result.get("questions", [])

        if questions:
            for q in questions:
                st.write(f"- {q}")
        else:
            st.write("No additional questions needed.")

        # ============================
        # ANALYSIS
        # ============================

        st.subheader("Analysis")

        analysis = result.get("analysis", {})

        st.markdown("**Reason:**")
        for r in analysis.get("reason", []):
            st.write(f"- {r}")

        st.markdown("**Recommendation:**")
        for r in analysis.get("recommendation", []):
            st.write(f"- {r}")
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
        # DIMENSIONS (🔥 CORE FEATURE)
        # ============================

        st.subheader("Decision Dimensions")

        dimensions = result["dimensions"]

        for k, v in dimensions.items():
            st.write(f"**{k.replace('_', ' ').title()}**: {v}")

        # ============================
        # DECISION INTELLIGENCE
        # ============================

        st.subheader("Decision Intelligence")

        col1, col2, col3 = st.columns(3)

        col1.metric("Weight", result["decision_weight"])
        col2.metric("Reversibility", result["reversibility"])
        col3.metric("Action", result["action"])

        # ============================
        # QUESTIONS
        # ============================

        st.subheader("Questions to Consider")

        for q in result["questions"]:
            st.write(f"- {q}")

        # ============================
        # ANALYSIS
        # ============================

        st.subheader("Analysis")

        st.markdown("**Reason:**")
        for r in result["analysis"]["reason"]:
            st.write(f"- {r}")

        st.markdown("**Recommendation:**")
        for r in result["analysis"]["recommendation"]:
            st.write(f"- {r}")
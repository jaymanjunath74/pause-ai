import streamlit as st
from engine import analyze_input

st.set_page_config(page_title="Pause AI", layout="centered")

st.title("⏸️ Pause AI")
st.caption("Clarity before action")

user_input = st.text_area("Enter your prompt:", height=150)

if st.button("Analyze"):

    if not user_input.strip():
        st.warning("Please enter something first.")
        st.stop()

    result = analyze_input(user_input)

    # ============================
    # INTENT ROUTING
    # ============================

    if result.get("intent"):

        if result["intent"] == "non_decision":
            st.info(result["message"])

        elif result["intent"] == "low_stakes":
            st.info(result["message"])

        st.stop()

    score = result["score"]

    # ============================
    # SCORE
    # ============================

    if score >= 80:
        st.success(f"Pause Score: {score} (Low Risk)")
    elif score >= 50:
        st.warning(f"Pause Score: {score} (Moderate Risk)")
    else:
        st.error(f"Pause Score: {score} (High Risk)")

    # ============================
    # STRUCTURE
    # ============================

    st.subheader("Decision Breakdown")

    for k, v in result["structure"].items():
        if k != "confidence":
            st.write(f"**{k.replace('_', ' ').title()}**: {v}")

    # ============================
    # INTELLIGENCE
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
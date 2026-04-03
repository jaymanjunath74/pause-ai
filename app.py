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
    # INTENT HANDLING
    # ============================

    if result.get("intent"):
        intent = result.get("intent")

        if intent == "task":
            st.info("This looks like a task, but there may be an underlying decision.")

        elif intent == "information":
            st.info("This looks like an information request, not a decision.")

        elif intent == "conversation":
            st.info("This appears conversational, not a decision.")

        else:
            st.info(result.get("message"))

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
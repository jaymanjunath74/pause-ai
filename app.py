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

        score = result["score"]

        # ----------------------------
        # Score Display
        # ----------------------------
        if score >= 80:
            st.success(f"Pause Score: {score} (Low Risk)")
        elif score >= 50:
            st.warning(f"Pause Score: {score} (Moderate Risk)")
        else:
            st.error(f"Pause Score: {score} (High Risk)")

        # ----------------------------
        # Decision Type
        # ----------------------------
        st.subheader("Decision Type")
        st.write(result["type"])

        # ----------------------------
        # Decision Intelligence (NEW)
        # ----------------------------
        st.subheader("Decision Intelligence")

        col1, col2, col3 = st.columns(3)
        col1.metric("Weight", result["decision_weight"])
        col2.metric("Reversibility", result["reversibility"])
        col3.metric("Action", result["action"])

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
        # Analysis (FIXED)
        # ----------------------------
        st.subheader("Analysis")

        analysis = result["analysis"]

        st.markdown("**Reason:**")
        for r in analysis["reason"]:
            st.write(f"- {r}")

        st.markdown("**Recommendation:**")
        for r in analysis["recommendation"]:
            st.write(f"- {r}")
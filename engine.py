import json
import streamlit as st
from openai import OpenAI

# ============================
# CLIENT
# ============================

def get_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        return OpenAI(api_key=api_key)
    except Exception:
        return None


# ============================
# SAFE JSON PARSER
# ============================

def safe_parse_json(content: str):
    try:
        return json.loads(content)
    except Exception:
        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            return json.loads(content[start:end])
        except Exception:
            return None


# ============================
# DEFAULT STRUCTURE
# ============================

def default_structure():
    return {
        "request_kind": "unknown",
        "decision_present": False,
        "decision_type": "none",
        "decision_statement": None,
        "stakes_level": "low",
        "time_pressure": "unknown",
        "information_completeness": "low",
        "reversibility": "high",
        "uncertainty_level": "low",
        "confidence": 0.0
    }


# ============================
# LLM STRUCTURE EXTRACTION
# ============================

def extract_structure(text):
    client = get_client()

    if client is None:
        return default_structure()

    prompt = f"""
You are a decision intelligence system.

Determine whether the user input involves a decision.

A decision exists if the user:
- expresses intent
- plans an action
- considers doing something
- asks how to do something

Prefer detecting decisions over missing them.

User Input:
"{text}"

Return ONLY valid JSON:

{{
  "request_kind": "decision | task | information | conversation | mixed",
  "decision_present": true/false,
  "decision_type": "explicit | implicit | none",
  "decision_statement": "clear decision or null",
  "stakes_level": "low | medium | high",
  "time_pressure": "low | medium | high | unknown",
  "information_completeness": "low | medium | high",
  "reversibility": "low | medium | high",
  "uncertainty_level": "low | medium | high",
  "confidence": 0.0-1.0
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content
        structure = safe_parse_json(raw)

        if not structure:
            return default_structure()

    except Exception:
        return default_structure()

    return validate_structure(structure, text)


# ============================
# VALIDATION (FIXED)
# ============================

def validate_structure(structure, text=None):

    # 🔥 HARD OVERRIDE: INTENT DETECTION
    if text:
        t = text.lower()

        intent_signals = [
            "i want", "i will", "i plan", "i am going to",
            "thinking of", "considering", "should i",
            "how do i", "can i"
        ]

        if any(signal in t for signal in intent_signals):
            structure["decision_present"] = True

            if not structure.get("decision_type") or structure["decision_type"] == "none":
                structure["decision_type"] = "implicit"

    # 🔥 CONFIDENCE FIX
    if structure.get("confidence", 0) < 0.5:
        structure["decision_present"] = True
        structure["decision_type"] = "implicit"

    return structure


# ============================
# SCORING
# ============================

def calculate_score(structure):
    score = 100

    penalties = {
        "information_completeness": {"low": 30, "medium": 15, "high": 0},
        "uncertainty_level": {"high": 20, "medium": 10, "low": 0},
        "time_pressure": {"high": 10, "medium": 5, "low": 0},
        "reversibility": {"low": 20, "medium": 10, "high": 0}
    }

    for key, mapping in penalties.items():
        value = structure.get(key)
        if value in mapping:
            score -= mapping[value]

    return max(score, 5)


# ============================
# HELPERS
# ============================

def get_decision_weight(structure):
    return structure.get("stakes_level", "low").title()


def get_reversibility(structure):
    rev = structure.get("reversibility")

    if rev == "low":
        return "Hard to Reverse"
    elif rev == "medium":
        return "Moderate"
    return "Reversible"


def get_action(score):
    if score < 30:
        return "Pause"
    elif score < 60:
        return "Think More"
    elif score < 80:
        return "Proceed Carefully"
    return "Proceed"


# ============================
# QUESTIONS
# ============================

def generate_questions(structure):
    questions = []

    if structure.get("information_completeness") == "low":
        questions.append("What key information are you missing?")

    if structure.get("uncertainty_level") == "high":
        questions.append("What assumptions might be incorrect?")

    if structure.get("reversibility") == "low":
        questions.append("What happens if this goes wrong?")

    if structure.get("time_pressure") == "high":
        questions.append("Is this urgency real or self-imposed?")

    if structure.get("stakes_level") == "high":
        questions.append("How important is this decision long-term?")

    questions.append("What are the second-order consequences?")

    return list(dict.fromkeys(questions))[:5]


# ============================
# ANALYSIS
# ============================

def generate_analysis(structure):
    reasons = []
    recommendations = []

    if structure.get("information_completeness") == "low":
        reasons.append("Insufficient information")

    if structure.get("uncertainty_level") == "high":
        reasons.append("High uncertainty")

    if structure.get("reversibility") == "low":
        reasons.append("Hard to reverse")

    recommendations.append("Gather missing information")
    recommendations.append("Evaluate risks")
    recommendations.append("Avoid rushing")

    return {
        "reason": reasons[:3],
        "recommendation": recommendations[:3]
    }


# ============================
# MAIN ENTRY
# ============================

def analyze_input(text):
    structure = extract_structure(text)

    # 🚫 NOT A DECISION
    if not structure.get("decision_present"):
        return {
            "intent": "non_decision",
            "message": "This doesn’t appear to involve a meaningful decision."
        }

    # 🟢 LOW STAKES
    if structure.get("stakes_level") == "low":
        return {
            "intent": "low_stakes",
            "message": "This looks like a low-stakes decision. You can proceed."
        }

    # 🔥 FULL ANALYSIS
    score = calculate_score(structure)

    return {
        "score": score,
        "structure": structure,
        "decision_weight": get_decision_weight(structure),
        "reversibility": get_reversibility(structure),
        "action": get_action(score),
        "questions": generate_questions(structure),
        "analysis": generate_analysis(structure)
    }
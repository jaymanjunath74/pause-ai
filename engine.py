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
    """
    Handles cases where model returns extra text around JSON.
    """
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
# LLM STRUCTURE EXTRACTION
# ============================

def extract_structure(text):
    client = get_client()

    # Fallback if no API
    if client is None:
        return default_structure()

    prompt = f"""
You are a decision intelligence system.

Your job is to determine whether a user input involves a decision — even if it is not explicitly stated.

A decision exists if the user:
1. Is choosing between options
2. Is planning or intending to take an action
3. Is asking how to perform a meaningful action
4. Expresses desire to do something significant

---

Examples:

EXPLICIT:
- "Should I quit my job?" → decision

IMPLICIT:
- "How do I quit my job?" → decision
- "I want to buy a car" → decision
- "I am thinking of moving abroad" → decision
- "I plan to start a business" → decision

NOT decisions:
- "Write an email"
- "What is inflation?"
- "Tell me a joke"

---

User Input:
"{text}"

---

Return ONLY valid JSON:

{{
  "request_kind": "decision | task | information | conversation | mixed",

  "decision_present": true/false,

  "decision_type": "explicit | implicit | none",

  "decision_statement": "clear decision being considered OR null",

  "stakes_level": "low | medium | high",

  "time_pressure": "low | medium | high | unknown",

  "information_completeness": "low | medium | high",

  "reversibility": "low | medium | high",

  "uncertainty_level": "low | medium | high",

  "confidence": 0.0-1.0
}}

CRITICAL RULES:
- If the user expresses intent to act → decision_present MUST be true
- Prefer false positives over false negatives
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

    # ============================
    # VALIDATION LAYER (CRITICAL)
    # ============================

    structure = validate_structure(structure, text)

    return structure


# ============================
# DEFAULT STRUCTURE
# ============================

def default_structure():
    return {
        "request_kind": "unknown",
        "decision_present": False,
        "decision_type": "none",
        "decision_statement": None,
        "stakes_level": "unknown",
        "time_pressure": "unknown",
        "information_completeness": "low",
        "reversibility": "unknown",
        "uncertainty_level": "high",
        "confidence": 0.0
    }


# ============================
# VALIDATION (NO HARDCODING, JUST SAFETY)
# ============================

def validate_structure(structure, text):
    """
    Fixes LLM mistakes WITHOUT keyword hardcoding.
    """

    # Ensure required keys exist
    required_keys = [
        "request_kind",
        "decision_present",
        "decision_type",
        "confidence"
    ]

    for key in required_keys:
        if key not in structure:
            return default_structure()

    # Confidence fallback (soft correction)
    if structure.get("confidence", 0) < 0.5:
        if structure.get("request_kind") in ["task", "mixed", "decision"]:
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
# DECISION INTELLIGENCE
# ============================

def get_decision_weight(structure):
    if structure.get("stakes_level") == "high":
        return "High"
    elif structure.get("stakes_level") == "medium":
        return "Medium"
    return "Low"


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
        questions.append("What happens if this decision goes wrong?")

    if structure.get("time_pressure") == "high":
        questions.append("Is the urgency real or self-imposed?")

    if structure.get("stakes_level") == "high":
        questions.append("How significant is this decision relative to your situation?")

    questions.append("What are the second-order consequences of this decision?")

    return list(dict.fromkeys(questions))[:5]


# ============================
# ANALYSIS
# ============================

def generate_analysis(structure):
    reasons = []
    recommendations = []

    if structure.get("information_completeness") == "low":
        reasons.append("Insufficient information to make a confident decision")

    if structure.get("uncertainty_level") == "high":
        reasons.append("High uncertainty detected")

    if structure.get("reversibility") == "low":
        reasons.append("Decision may be difficult to reverse")

    recommendations.append("Gather more relevant information before deciding")
    recommendations.append("Evaluate potential outcomes and risks")
    recommendations.append("Avoid rushing high-impact decisions")

    return {
        "reason": reasons[:3],
        "recommendation": recommendations[:3]
    }


# ============================
# MAIN ENTRY
# ============================

def analyze_input(text):
    structure = extract_structure(text)

    if not structure.get("decision_present"):
        return {
            "intent": structure.get("request_kind", "unknown"),
            "message": f"This appears to be a '{structure.get('request_kind')}' request, not a clear decision problem."
        }

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
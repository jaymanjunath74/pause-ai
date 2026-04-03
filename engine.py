import json
from openai import OpenAI

client = OpenAI()

# ============================
# LLM STRUCTURE EXTRACTION
# ============================

def extract_structure(text):
    prompt = f"""
You are a decision analysis engine.

Convert the user input into a structured JSON.

User Input:
"{text}"

Return ONLY valid JSON with this schema:

{{
  "request_kind": "decision | task | information | conversation | unknown",
  "decision_present": true/false,
  "decision_statement": "string or null",
  "stakes_level": "low | medium | high | unknown",
  "time_pressure": "low | medium | high | unknown",
  "information_completeness": "low | medium | high",
  "reversibility": "low | medium | high | unknown",
  "uncertainty_level": "low | medium | high",
  "confidence": 0.0-1.0
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "request_kind": "unknown",
            "decision_present": False,
            "confidence": 0
        }


# ============================
# SCORING (DETERMINISTIC)
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
# QUESTION ENGINE (DERIVED)
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

    return questions[:5]


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

    # ROUTING (NO HARD CODING)
    if not structure.get("decision_present", False):
        return {
            "intent": structure.get("request_kind", "unknown"),
            "message": f"This appears to be a '{structure.get('request_kind')}' request, not a decision problem."
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
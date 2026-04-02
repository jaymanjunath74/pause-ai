import re
from collections import defaultdict

# ============================
# SIGNAL DEFINITIONS
# ============================

SIGNALS = {
    # 🔴 STAKES
    "financial_magnitude_high": {
        "weight": 25,
        "description": "Large financial commitment detected"
    },
    "irreversible_decision": {
        "weight": 25,
        "description": "Decision is hard to reverse"
    },
    "career_impact": {
        "weight": 20,
        "description": "Career impact involved"
    },
    "relationship_impact": {
        "weight": 20,
        "description": "Relationship impact involved"
    },
    "health_legal_risk": {
        "weight": 30,
        "description": "Health or legal risk detected"
    },

    # 🟡 CONTEXT
    "low_context": {
        "weight": 20,
        "description": "Insufficient context"
    },
    "missing_constraints": {
        "weight": 15,
        "description": "Missing constraints (budget, limits)"
    },
    "missing_alternatives": {
        "weight": 10,
        "description": "No alternatives considered"
    },
    "unclear_objective": {
        "weight": 15,
        "description": "Goal or success criteria unclear"
    },

    # 🟣 COGNITIVE
    "urgency_bias": {
        "weight": 20,
        "description": "Urgency detected"
    },
    "emotional_state": {
        "weight": 15,
        "description": "Emotional influence detected"
    },
    "reassurance_seeking": {
        "weight": 10,
        "description": "User seeking external validation"
    },

    # 🔵 ACTION
    "insufficient_information": {
        "weight": 20,
        "description": "Not enough information to act"
    },
    "premature_action": {
        "weight": 15,
        "description": "Action suggested too early"
    },
    "decision_can_wait": {
        "weight": 10,
        "description": "No real urgency"
    },

    # 🟢 AI FIT
    "needs_human_judgment": {
        "weight": 15,
        "description": "Better handled by human judgment"
    },
    "high_risk_advice": {
        "weight": 20,
        "description": "High-risk domain"
    }
}


# ============================
# DETECTION ENGINE
# ============================

def detect_signals(text):
    signals = set()
    t = text.lower()

    # ------------------------
    # STAKES
    # ------------------------
    if re.search(r"\$\s?\d+", text):
        signals.add("financial_magnitude_high")

    if any(w in t for w in ["buy", "spend", "purchase", "invest"]):
        signals.add("irreversible_decision")

    if any(w in t for w in ["job", "quit", "career"]):
        signals.add("career_impact")

    if any(w in t for w in ["relationship", "breakup", "text her", "text him"]):
        signals.add("relationship_impact")

    if any(w in t for w in ["legal", "lawsuit", "doctor", "medical"]):
        signals.add("health_legal_risk")

    # ------------------------
    # CONTEXT
    # ------------------------
    if len(text.split()) < 8:
        signals.add("low_context")

    if "should i" in t:
        signals.add("missing_constraints")
        signals.add("missing_alternatives")

    if "?" in text:
        signals.add("unclear_objective")

    # ------------------------
    # COGNITIVE
    # ------------------------
    if any(w in t for w in ["now", "asap", "urgent"]):
        signals.add("urgency_bias")

    if any(w in t for w in ["hate", "love", "angry", "excited"]):
        signals.add("emotional_state")

    if "should i" in t:
        signals.add("reassurance_seeking")

    # ------------------------
    # ACTION
    # ------------------------
    if "should i" in t:
        signals.add("insufficient_information")

    if any(w in t for w in ["buy", "quit", "send"]):
        signals.add("premature_action")

    if not any(w in t for w in ["now", "urgent"]):
        signals.add("decision_can_wait")

    # ------------------------
    # AI FIT
    # ------------------------
    if any(w in t for w in ["should i", "life", "marry"]):
        signals.add("needs_human_judgment")

    if any(w in t for w in ["invest", "medical", "legal"]):
        signals.add("high_risk_advice")

    return list(signals)


# ============================
# SCORING ENGINE
# ============================

def calculate_score(signals):
    score = 100

    # subtract weights
    for s in signals:
        if s in SIGNALS:
            score -= SIGNALS[s]["weight"]

    # cognitive stacking penalty
    cognitive = [s for s in signals if s in ["urgency_bias", "emotional_state", "reassurance_seeking"]]
    if len(cognitive) >= 2:
        score -= 10

    return max(score, 0)


# ============================
# CLASSIFICATION
# ============================

def classify_type(text):
    t = text.lower()

    if any(w in t for w in ["job", "career"]):
        return "Career"
    if any(w in t for w in ["buy", "money", "invest", "spend"]):
        return "Financial"
    if any(w in t for w in ["relationship", "marry", "breakup"]):
        return "Personal"

    return "General"


# ============================
# ANALYSIS GENERATOR
# ============================

def generate_analysis(signals):
    reasons = []
    recommendations = []

    for s in signals:
        if s in SIGNALS:
            reasons.append(SIGNALS[s]["description"])

    # Smart recommendations
    if "financial_magnitude_high" in signals:
        recommendations.append("Evaluate affordability relative to income and savings.")

    if "low_context" in signals:
        recommendations.append("Add more context before making a decision.")

    if "irreversible_decision" in signals:
        recommendations.append("Consider long-term impact and resale/liquidity.")

    if "needs_human_judgment" in signals:
        recommendations.append("Discuss with a trusted person before deciding.")

    if not recommendations:
        recommendations.append("Decision appears low risk. Proceed with awareness.")

    return {
        "reason": reasons[:3],  # top 3 only
        "recommendation": recommendations[:3]
    }


# ============================
# MAIN ENTRY
# ============================

def analyze_input(text):
    signals = detect_signals(text)
    score = calculate_score(signals)
    decision_type = classify_type(text)
    analysis = generate_analysis(signals)

    return {
        "score": score,
        "type": decision_type,
        "signals": signals,
        "analysis": analysis
    }
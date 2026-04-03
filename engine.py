import re

# ============================
# SIGNAL CONFIG (WEIGHTS)
# ============================

SIGNALS = {
    "financial_magnitude_high": 25,
    "irreversible_decision": 25,
    "career_impact": 20,
    "relationship_impact": 20,
    "health_legal_risk": 30,

    "low_context": 20,
    "missing_constraints": 15,
    "missing_alternatives": 10,
    "unclear_objective": 15,

    "urgency_bias": 20,
    "emotional_state": 15,
    "reassurance_seeking": 10,

    "insufficient_information": 20,
    "premature_action": 15,
    "decision_can_wait": 10,

    "needs_human_judgment": 15,
    "high_risk_advice": 20
}


# ============================
# SIGNAL DETECTION
# ============================

def detect_signals(text):
    signals = set()
    t = text.lower()

    # Stakes
    if re.search(r"\$\s?\d+", text):
        signals.add("financial_magnitude_high")

    if any(w in t for w in ["buy", "spend", "purchase", "invest"]):
        signals.add("irreversible_decision")

    if any(w in t for w in ["job", "career", "quit"]):
        signals.add("career_impact")

    if any(w in t for w in ["relationship", "breakup"]):
        signals.add("relationship_impact")

    if any(w in t for w in ["medical", "legal"]):
        signals.add("health_legal_risk")

    # Context
    if len(text.split()) < 8:
        signals.add("low_context")

    if "should i" in t:
        signals.add("missing_constraints")
        signals.add("missing_alternatives")
        signals.add("insufficient_information")
        signals.add("reassurance_seeking")

    if "?" in text:
        signals.add("unclear_objective")

    # Cognitive
    if any(w in t for w in ["now", "asap", "urgent"]):
        signals.add("urgency_bias")

    if any(w in t for w in ["angry", "frustrated", "excited"]):
        signals.add("emotional_state")

    # Action
    if any(w in t for w in ["buy", "quit", "send"]):
        signals.add("premature_action")

    if not any(w in t for w in ["now", "urgent"]):
        signals.add("decision_can_wait")

    # AI Fit
    if "should i" in t:
        signals.add("needs_human_judgment")

    if any(w in t for w in ["invest", "medical", "legal"]):
        signals.add("high_risk_advice")

    return list(signals)


# ============================
# SCORING (NORMALIZED)
# ============================

def calculate_score(signals):
    total_penalty = sum(SIGNALS.get(s, 0) for s in signals)
    max_possible = sum(SIGNALS.values())

    score = 100 * (1 - total_penalty / max_possible)
    return max(int(score), 5)


# ============================
# TOP SIGNALS (PRIORITY)
# ============================

def get_top_signals(signals):
    ranked = sorted(
        signals,
        key=lambda s: SIGNALS.get(s, 0),
        reverse=True
    )
    return ranked[:3]


# ============================
# DECISION WEIGHT
# ============================

def get_decision_weight(signals):
    if "health_legal_risk" in signals:
        return "Very High"

    if "financial_magnitude_high" in signals or "career_impact" in signals:
        return "High"

    if "relationship_impact" in signals:
        return "Medium"

    return "Low"


# ============================
# REVERSIBILITY
# ============================

def get_reversibility(signals):
    if "irreversible_decision" in signals:
        return "Hard to Reverse"

    return "Reversible"


# ============================
# ACTION
# ============================

def get_action(score, signals):
    if "insufficient_information" in signals:
        return "Ask More Info"

    if score < 30:
        return "Pause"

    if score < 60:
        return "Think More"

    return "Proceed"


# ============================
# ANALYSIS
# ============================

def generate_analysis(signals):
    reasons = []
    recommendations = []

    if "financial_magnitude_high" in signals:
        reasons.append("Large financial commitment detected")

    if "irreversible_decision" in signals:
        reasons.append("Decision may be hard to reverse")

    if "low_context" in signals:
        reasons.append("Not enough context to decide confidently")

    recommendations.append("Clarify your constraints (budget, priorities)")
    recommendations.append("Compare alternatives before committing")
    recommendations.append("Delay decision if not time-sensitive")

    return {
        "reason": reasons[:3],
        "recommendation": recommendations[:3]
    }


# ============================
# CLASSIFICATION
# ============================

def classify_type(text):
    t = text.lower()

    if any(w in t for w in ["job", "career"]):
        return "Career"

    if any(w in t for w in ["money", "buy", "invest", "spend"]):
        return "Financial"

    if any(w in t for w in ["relationship", "marry", "breakup"]):
        return "Personal"

    return "General"


# ============================
# MAIN
# ============================

def analyze_input(text):
    signals = detect_signals(text)
    score = calculate_score(signals)

    return {
        "score": score,
        "type": classify_type(text),
        "signals": signals,
        "top_signals": get_top_signals(signals),
        "decision_weight": get_decision_weight(signals),
        "reversibility": get_reversibility(signals),
        "action": get_action(score, signals),
        "analysis": generate_analysis(signals)
    }
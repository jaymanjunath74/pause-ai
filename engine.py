# ============================
# PAUSE AI - CLEAN ENGINE (V2)
# ============================

def extract_features(text):
    t = text.lower()

    return {
        "length": len(text.split()),
        "has_numbers": any(char.isdigit() for char in text),
        "is_question": "?" in text,
        "has_uncertainty": any(word in t for word in ["should", "not sure", "confused"]),
        "has_urgency": any(word in t for word in ["now", "asap", "urgent"]),
        "has_action_words": any(word in t for word in ["buy", "quit", "move", "invest", "sell", "start", "stop"])
    }


# ============================
# DIMENSION EVALUATION
# ============================

def evaluate_dimensions(features):
    dimensions = {}

    # Information Quality
    if features["length"] < 8:
        dimensions["information_quality"] = "LOW"
    elif features["length"] < 20:
        dimensions["information_quality"] = "MEDIUM"
    else:
        dimensions["information_quality"] = "HIGH"

    # Clarity
    if features["is_question"]:
        dimensions["clarity"] = "LOW"
    else:
        dimensions["clarity"] = "MEDIUM"

    # Stakes (proxy-based, no domain assumption)
    if features["has_numbers"]:
        dimensions["stakes"] = "HIGH"
    else:
        dimensions["stakes"] = "UNKNOWN"

    # Certainty
    if features["has_uncertainty"]:
        dimensions["certainty"] = "LOW"
    else:
        dimensions["certainty"] = "MEDIUM"

    # Time Pressure
    if features["has_urgency"]:
        dimensions["time_pressure"] = "HIGH"
    else:
        dimensions["time_pressure"] = "LOW"

    # Action Readiness
    if features["has_action_words"]:
        dimensions["action_readiness"] = "HIGH"
    else:
        dimensions["action_readiness"] = "LOW"

    return dimensions


# ============================
# SCORING (DIMENSION-BASED)
# ============================

def calculate_score(dimensions):
    score = 100

    penalties = {
        "information_quality": {"LOW": 25, "MEDIUM": 10, "HIGH": 0},
        "clarity": {"LOW": 15, "MEDIUM": 5},
        "certainty": {"LOW": 15, "MEDIUM": 5},
        "time_pressure": {"HIGH": 10, "LOW": 0},
        "action_readiness": {"HIGH": 10, "LOW": 0}
    }

    for dim, value in dimensions.items():
        if dim in penalties and value in penalties[dim]:
            score -= penalties[dim][value]

    return max(score, 5)


# ============================
# DECISION INTELLIGENCE
# ============================

def get_decision_weight(dimensions):
    if dimensions["stakes"] == "HIGH":
        return "High"
    return "Medium"


def get_reversibility(dimensions):
    if dimensions["action_readiness"] == "HIGH":
        return "Hard to Reverse"
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
# QUESTION ENGINE (DIMENSION-DRIVEN)
# ============================

def generate_questions(dimensions):
    questions = []

    if dimensions["information_quality"] == "LOW":
        questions.append("What key information are you missing?")
        questions.append("What details would make this decision clearer?")

    if dimensions["clarity"] == "LOW":
        questions.append("What exactly are you trying to decide?")

    if dimensions["certainty"] == "LOW":
        questions.append("What assumptions might be incorrect?")
        questions.append("What would change your confidence in this decision?")

    if dimensions["stakes"] == "HIGH":
        questions.append("How significant is this decision relative to your situation?")

    if dimensions["time_pressure"] == "HIGH":
        questions.append("Is the urgency real or self-imposed?")

    if dimensions["action_readiness"] == "HIGH":
        questions.append("What happens if this decision goes wrong?")
        questions.append("Can you test this decision before fully committing?")

    questions.append("What are the second-order consequences of this decision?")

    # Deduplicate + limit
    return list(dict.fromkeys(questions))[:5]


# ============================
# ANALYSIS
# ============================

def generate_analysis(dimensions):
    reasons = []
    recommendations = []

    if dimensions["information_quality"] == "LOW":
        reasons.append("Insufficient information to make a confident decision")

    if dimensions["clarity"] == "LOW":
        reasons.append("Decision framing is unclear")

    if dimensions["certainty"] == "LOW":
        reasons.append("Uncertainty detected in decision-making")

    recommendations.append("Gather more relevant information before deciding")
    recommendations.append("Clarify your objective and constraints")
    recommendations.append("Consider possible outcomes and risks")

    return {
        "reason": reasons[:3],
        "recommendation": recommendations[:3]
    }


# ============================
# MAIN ENTRY
# ============================

def analyze_input(text):
    features = extract_features(text)
    dimensions = evaluate_dimensions(features)
    score = calculate_score(dimensions)

    return {
        "score": score,
        "dimensions": dimensions,
        "decision_weight": get_decision_weight(dimensions),
        "reversibility": get_reversibility(dimensions),
        "action": get_action(score),
        "questions": generate_questions(dimensions),
        "analysis": generate_analysis(dimensions)
    }
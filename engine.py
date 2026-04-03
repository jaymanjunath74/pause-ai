# engine.py

# ============================
# INTENT DETECTION (DETERMINISTIC)
# ============================

def detect_decision(text: str) -> bool:
    t = text.lower().strip()

    intent_patterns = [
        "i want", "i will", "i plan", "i am going to",
        "thinking of", "considering", "should i",
        "how do i", "can i"
    ]

    return any(p in t for p in intent_patterns)


# ============================
# STAKES DETECTION (SIMPLE HEURISTIC)
# ============================

def detect_stakes(text: str) -> str:
    t = text.lower()

    high_keywords = [
        "job", "career", "quit", "resign",
        "marriage", "divorce",
        "move", "relocate",
        "buy house", "mortgage",
        "invest", "investment", "loan", "debt",
        "surgery", "health", "diagnosis",
        "legal", "lawsuit"
    ]

    if any(k in t for k in high_keywords):
        return "high"

    medium_keywords = [
        "buy", "purchase", "car", "course",
        "travel", "trip", "change", "switch"
    ]

    if any(k in t for k in medium_keywords):
        return "medium"

    return "low"


# ============================
# MAIN ENTRY
# ============================

def analyze_input(text: str) -> dict:

    if not text or not text.strip():
        return {
            "intent": "empty",
            "message": "Please enter something."
        }

    is_decision = detect_decision(text)

    if not is_decision:
        return {
            "intent": "non_decision",
            "message": "This doesn’t appear to involve a decision."
        }

    stakes = detect_stakes(text)

    if stakes == "low":
        return {
            "intent": "low_stakes",
            "message": "This is a low-stakes decision. No need to overthink."
        }

    if stakes == "medium":
        return {
            "intent": "medium_stakes",
            "message": "This decision has some impact. Take a moment to think it through."
        }

    return {
        "intent": "high_stakes",
        "message": "This looks like a meaningful decision. Slow down and evaluate carefully."
    }
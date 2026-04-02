import os
from openai import AzureOpenAI

# ----------------------------
# Azure OpenAI Client
# ----------------------------
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")


# ----------------------------
# Signal Detection (Deterministic)
# ----------------------------
def detect_signals(prompt: str):
    prompt_lower = prompt.lower()

    signals = []

    # Urgency
    urgency_words = ["now", "asap", "immediately", "urgent", "right away"]
    if any(word in prompt_lower for word in urgency_words):
        signals.append("urgency_detected")

    # Emotional language
    emotional_words = ["angry", "frustrated", "hate", "love", "upset", "excited"]
    if any(word in prompt_lower for word in emotional_words):
        signals.append("emotional_language")

    # Absolute thinking
    absolute_words = ["always", "never", "everyone", "no one"]
    if any(word in prompt_lower for word in absolute_words):
        signals.append("absolute_thinking")

    # Low context
    if len(prompt.split()) < 8:
        signals.append("low_context")

    return signals


# ----------------------------
# Classification
# ----------------------------
def classify_prompt(prompt: str):
    p = prompt.lower()

    if any(word in p for word in ["money", "invest", "buy", "sell", "price"]):
        return "Financial"

    if any(word in p for word in ["job", "career", "offer", "boss"]):
        return "Career"

    if any(word in p for word in ["relationship", "friend", "girlfriend", "boyfriend"]):
        return "Social"

    if any(word in p for word in ["feel", "emotion", "angry", "sad"]):
        return "Emotional"

    return "General"


# ----------------------------
# Scoring System
# ----------------------------
def compute_pause_score(signals):
    score = 100

    penalties = {
        "urgency_detected": 20,
        "emotional_language": 15,
        "absolute_thinking": 10,
        "low_context": 15
    }

    for s in signals:
        score -= penalties.get(s, 0)

    return max(score, 0)


# ----------------------------
# LLM Controlled Interpretation
# ----------------------------
def generate_analysis(prompt, decision_type, signals, score):
    system_prompt = f"""
You are a decision analysis assistant.

DO NOT be verbose.
DO NOT rewrite the prompt.
DO NOT give generic advice.

You must respond in this EXACT format:

Reason:
- bullet points explaining risks based on signals

Recommendation:
- 1 clear actionable suggestion

Context:
Decision Type: {decision_type}
Signals: {signals}
Score: {score}
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# ----------------------------
# Main Function
# ----------------------------
def analyze_input(prompt: str):
    signals = detect_signals(prompt)
    decision_type = classify_prompt(prompt)
    score = compute_pause_score(signals)

    llm_output = generate_analysis(prompt, decision_type, signals, score)

    return {
        "type": decision_type,
        "score": score,
        "signals": signals,
        "analysis": llm_output
    }
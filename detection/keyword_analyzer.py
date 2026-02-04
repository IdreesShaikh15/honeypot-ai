from detection.keyword_rules import SUSPICIOUS_KEYWORDS, SCAM_THRESHOLD

# Behavioral eagerness / pressure patterns
EAGERNESS_PATTERNS = [
    "send your",
    "share your",
    "provide your",
    "give your",
    "why haven't you",
    "do it now",
    "immediately",
    "right now",
    "fast"
]

def analyze_keywords(text: str, session: dict) -> bool:
    text_lower = text.lower()

    # 1️⃣ Keyword-based detection
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text_lower:
            session["keyword_hits"] += 1
            session["intelligence"]["suspiciousKeywords"].append(keyword)

    # 2️⃣ Eagerness / pressure-based detection
    for pattern in EAGERNESS_PATTERNS:
        if pattern in text_lower:
            session["keyword_hits"] += 1
            session["intelligence"]["suspiciousKeywords"].append("eagerness_pressure")
            break  # avoid multiple counts for same message

    # 3️⃣ Repeated detail-request behavior
    if session["total_messages"] > 1:
        if any(x in text_lower for x in ["upi", "account", "number", "details"]):
            session["keyword_hits"] += 1
            session["intelligence"]["suspiciousKeywords"].append("repeated_detail_request")

    # Final scam decision
    return session["keyword_hits"] >= SCAM_THRESHOLD

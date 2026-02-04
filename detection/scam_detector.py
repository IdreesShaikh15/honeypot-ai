def detect_scam(text: str) -> bool:
    scam_keywords = [
        "blocked",
        "verify",
        "urgent",
        "suspended",
        "account",
        "upi",
        "payment",
        "click link"
    ]

    text = text.lower()

    for keyword in scam_keywords:
        if keyword in text:
            return True

    return False

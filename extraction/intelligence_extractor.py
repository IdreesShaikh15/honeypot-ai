import re

def extract_intelligence(text: str):

    intelligence = {
        "upiIds": re.findall(r"\b[\w.-]+@[\w.-]+\b", text),
        "phoneNumbers": re.findall(r"\b[6-9]\d{9}\b", text),
        "phishingLinks": re.findall(r"https?://[^\s]+", text),
        "suspiciousKeywords": []
    }

    keywords = ["urgent", "verify", "blocked", "suspended", "account"]

    for k in keywords:
        if k in text.lower():
            intelligence["suspiciousKeywords"].append(k)

    return intelligence

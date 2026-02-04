import random
import re
from extraction.intelligence_extractor import extract_intelligence


# -----------------------
# LANGUAGE DETECTION
# -----------------------
def is_non_english(text: str) -> bool:
    non_ascii = re.findall(r"[^\x00-\x7F]", text)
    return len(non_ascii) > 3


# -----------------------
# GREETING DETECTION
# -----------------------
def is_greeting(text: str) -> bool:
    greetings = [
        "hello", "hi", "hey",
        "good morning", "good afternoon", "good evening",
        "namaste", "greetings"
    ]
    text = text.lower()
    return any(g in text for g in greetings)


# -----------------------
# OFF TOPIC DETECTION
# -----------------------
def is_off_topic(text: str) -> bool:
    off_topic_keywords = [
        "weather", "movie", "food", "cricket", "match", "family",
        "weekend", "holiday", "party", "travel", "game", "music",
        "friend", "shopping", "salary", "relationship"
    ]
    text = text.lower()
    return any(word in text for word in off_topic_keywords)


# -----------------------
# MAIN REPLY ENGINE
# -----------------------
def get_human_reply(session: dict) -> str:

    msg_count = session["total_messages"]
    scam = session["scam_detected"]
    last_message = session["messages"][-1] if session["messages"] else ""

    text_lower = last_message.lower()

    # -----------------------
    # INTELLIGENCE EXTRACTION
    # -----------------------
    details = extract_intelligence(last_message)

    for key in details:
        if details[key]:
            session["intelligence"][key].extend(details[key])

    # -----------------------
    # LANGUAGE ENFORCEMENT
    # -----------------------
    if is_non_english(last_message):
        return "Sorry, I am comfortable only in English. Please explain again."

    # -----------------------
    # OFF TOPIC REDIRECTION
    # -----------------------
    if is_off_topic(last_message):
        return "Sir/Ma’am please focus on your banking issue first."

    # -----------------------
    # CONTEXT BASED REPLIES
    # -----------------------

    if "upi" in text_lower:
        return "Okay, can you confirm the UPI ID again so I don't send money to the wrong account?"

    if "otp" in text_lower:
        return "Why do you need the OTP? Is it required for verification?"

    if "payment" in text_lower or "fee" in text_lower:
        return "How much payment is required and where should I send it?"

    if "link" in text_lower or "click" in text_lower:
        return "Can you send the official verification link again?"

    if "account" in text_lower or "bank" in text_lower:
        return "What exactly is wrong with my account? Is it blocked or suspended?"

    if "verify" in text_lower:
        return "What details do I need to verify? Please explain step by step."

    # -----------------------
    # GREETING RESPONSES
    # -----------------------
    if msg_count == 1 and is_greeting(last_message):
        return "Hello. Please tell me what this is regarding."

    # -----------------------
    # HUMAN REALISM FALLBACK
    # -----------------------
    normal_replies = [
        "I am not very familiar with these things. Please explain step by step.",
        "I am trying to understand. Please guide me.",
        "Please explain clearly so I don't make mistakes.",
        "Can you explain the full process slowly?",
    ]

    cautious_replies = [
        "Is this safe? I usually do not share details.",
        "Why is this verification required suddenly?",
        "Can you confirm if this is official?",
    ]

    honeypot_replies = [
        "Okay, what should I do next?",
        "Please guide me slowly.",
        "Where exactly do I need to enter these details?",
    ]

    correction_replies = [
        "Sorry, I misunderstood earlier. Please continue.",
        "Ignore my previous message. Please explain again.",
    ]

    ending_replies = [
        "Let me check this and get back to you.",
        "Give me few minutes to verify this.",
    ]

    # -----------------------
    # FLOW CONTROL
    # -----------------------
    if not scam:
        return random.choice(normal_replies + cautious_replies)

    if scam and msg_count <= 6:
        return random.choice(honeypot_replies + cautious_replies + correction_replies)

    return random.choice(ending_replies)

sessions = {}

def get_session(session_id: str):

    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "scam_detected": False,
            "total_messages": 0,
            "keyword_hits": 0,
            "terminated": False,
            "intelligence": {
                "upiIds": [],
                "phoneNumbers": [],
                "phishingLinks": [],
                "suspiciousKeywords": []
            }
        }

    return sessions[session_id]

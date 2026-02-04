import requests

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"


def send_final_result(process_id: str, session: dict):

    payload = {
        "processId": process_id,  # ⭐ IMPORTANT
        "scamDetected": session.get("scam_detected", False),
        "totalMessagesExchanged": session.get("total_messages", 0),
        "extractedIntelligence": session.get("intelligence", {}),
        "agentNotes": "Progressive keyword + behavioral honeypot extraction"
    }

    try:
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )

        print("GUVI Response:", response.status_code)
        print("GUVI Response Text:", response.text)

    except Exception as e:
        print("GUVI callback failed:", e)

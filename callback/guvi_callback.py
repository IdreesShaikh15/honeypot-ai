import requests



GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"





def send_final_result(session_id: str, session: dict):



    payload = {

        "sessionId": session_id,

        "scamDetected": session["scam_detected"],

        "totalMessagesExchanged": session["total_messages"],



        # ✅ FIXED STRUCTURE

        "extractedIntelligence": {

            "upiId": session["intelligence"]["upiIds"],

            "phoneNumbers": session["intelligence"]["phoneNumbers"],

            "phishingLinks": session["intelligence"]["phishingLinks"],

            "suspiciousKeywords": session["intelligence"]["suspiciousKeywords"]

        },



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
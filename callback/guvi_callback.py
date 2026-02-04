import requests



GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"





def send_final_result(session_id: str, session: dict):



    payload = {

        "sessionId": session_id,

        "scamDetected": session["scam_detected"],

        "totalMessagesExchanged": session["total_messages"],



        # ONLY SEND WHAT GUVI STRICTLY NEEDS

        "extractedIntelligence": {

            "upiId": session["intelligence"]["upiIds"]

        },



        "agentNotes": "Keyword + behavioral honeypot"

    }



    try:

        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)



        print("GUVI Response:", response.status_code)

        print("GUVI Response Text:", response.text)



    except Exception as e:

        print("GUVI callback failed:", e)
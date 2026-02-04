from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader

from detection.keyword_analyzer import analyze_keywords
from sessions.session_manager import get_session
from termination.termination_logic import should_terminate
from callback.guvi_callback import send_final_result
from conversation.reply_generator import get_human_reply

app = FastAPI()

API_KEY = "lushlife"
API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/honeypot/message")
async def honeypot_message(request: Request, _: str = Depends(verify_api_key)):

    try:
        payload = await request.json()

        if "processId" in payload:
            return {
                "status": "success",
                "reply": "Hello, how can I help you today?",
                "processId": payload["processId"]
            }

        session_id = payload.get("sessionId", "default-session")

        message_text = ""

        if isinstance(payload.get("message"), dict):
            message_text = payload.get("message", {}).get("text", "")

        elif isinstance(payload.get("message"), str):
            message_text = payload.get("message")

        if not message_text:
            return {
                "status": "success",
                "reply": "Could you please repeat that message?"
            }

        session = get_session(session_id)

        if session.get("terminated"):
            session["terminated"] = False
            session["messages"].clear()
            session["total_messages"] = 0
            session["scam_detected"] = False
            session["intelligence"] = {
                "upiIds": [],
                "phoneNumbers": [],
                "phishingLinks": [],
                "suspiciousKeywords": []
            }

        session["messages"].append(message_text)
        session["total_messages"] += 1

        if not session["scam_detected"]:
            session["scam_detected"] = analyze_keywords(message_text, session)

        reply = get_human_reply(session)

        if session["scam_detected"] and should_terminate(session):

            session["terminated"] = True
            send_final_result(session_id, session)

            return {
                "status": "success",
                "reply": "I will check this and get back to you. Thank you."
            }

        return {
            "status": "success",
            "reply": reply
        }

    except Exception:
        return {
            "status": "success",
            "reply": "Unable to process message."
        }

from fastapi import FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Optional, Union

from detection.keyword_analyzer import analyze_keywords
from sessions.session_manager import get_session
from termination.termination_logic import should_terminate
from callback.guvi_callback import send_final_result
from conversation.reply_generator import get_human_reply

app = FastAPI()

# ---------------- API KEY ----------------
API_KEY = "lushlife"
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# ---------------- HEALTH CHECK (VERY IMPORTANT FOR GUVI) ----------------
@app.get("/honeypot/message")
async def honeypot_health_check():
    print("✅ Health check called")
    return {"status": "alive"}


# ---------------- REQUEST MODELS ----------------
class MessageModel(BaseModel):
    text: Optional[str] = None


class HoneypotRequest(BaseModel):
    processId: Optional[str] = None
    sessionId: Optional[str] = None
    message: Optional[Union[MessageModel, str]] = None


# ---------------- ENDPOINT ----------------
@app.post("/honeypot/message")
async def honeypot_message(
    payload: HoneypotRequest,
    api_key: str = Security(api_key_header)
):

    print("🔥 POST RECEIVED")
    print("Payload:", payload)

    # AUTH
    verify_api_key(api_key)

    # ⭐⭐⭐ GUVI VALIDATION (FIRST RETURN)
    if payload.processId:
        print("✅ Process ID Validation Hit")
        return {
            "status": "success",
            "processId": payload.processId
        }

    try:
        print("➡ Inside try block")

        session_id = payload.sessionId or "default-session"

        # -------- Extract message safely --------
        message_text = ""

        if isinstance(payload.message, MessageModel):
            message_text = payload.message.text or ""

        elif isinstance(payload.message, str):
            message_text = payload.message

        print("📝 Extracted message:", message_text)

        if not message_text:
            return {
                "status": "success",
                "reply": "Could you please repeat that message?"
            }

        session = get_session(session_id)

        # -------- Reset terminated session --------
        if session.get("terminated"):
            session["terminated"] = False
            session["messages"].clear()
            session["total_messages"] = 0
            session["scam_detected"] = False
            session["keyword_hits"] = 0
            session["intelligence"] = {
                "upiIds": [],
                "phoneNumbers": [],
                "phishingLinks": [],
                "suspiciousKeywords": []
            }

        session["messages"].append(message_text)
        session["total_messages"] += 1

        # -------- Keyword analysis --------
        if not session["scam_detected"]:
            session["scam_detected"] = analyze_keywords(message_text, session)

        reply = get_human_reply(session)

        # -------- Termination logic --------
        if session["scam_detected"] and should_terminate(session):

            print("🚨 Scam detected, terminating session")

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

    except Exception as e:
        print("❌ ERROR:", str(e))

        return {
            "status": "success",
            "reply": "Unable to process message."
        }

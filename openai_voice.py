import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    raise ValueError("Missing the OpenAI API key. Please set it in the .env file.")

app = FastAPI()

TEMPERATURE = 0.8

PERSONA = {
    "Dana": {
        "system_message": (
            "You are Dana Whitfield, 34, calling a medical office to book a "
            "first appointment as a new patient. Your date of birth is March 12, 1992. "
            "You are calm, polite and easy to deal with. "
            "Speak one short thought per turn, the way people actually talk on the phone. "
            "Never volunteer anything you were not asked for. "
            "Wait for them to finish before you answer. "
            "You are the caller, not an assistant, so never offer to help them. "
            "Once the appointment is booked, thank them and say goodbye."
        ),
        "voice": "sage",
    }
}

SYSTEM_MESSAGE = PERSONA["Dana"]["system_message"]

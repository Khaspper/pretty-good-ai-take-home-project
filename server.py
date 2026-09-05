import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, Response

load_dotenv()

STREAM_URL = os.getenv("PUBLIC_URL", "").replace("https://", "wss://")

app = FastAPI()


@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    return "pong"


@app.post("/voice")
def voice() -> Response:
    response = f"""
    <Response>
        <Connect>
            <Stream url="{STREAM_URL}/listen" />
        </Connect>
    </Response>
    """
    return Response(content=response, media_type="application/xml")

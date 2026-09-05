import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
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


# https://fastapi.tiangolo.com/advanced/websockets/#create-a-websocket
# I've actually never really touched websockets with python
@app.websocket("/listen")
async def listen_to_call(websocket: WebSocket):
    await websocket.accept()
    print("line opened")

    slices = 0
    while True:
        data = await websocket.receive_text()
        slices += 1
        print(slices)
        print(f"data: {data}")

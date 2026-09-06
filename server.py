import asyncio
import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse, Response
from openai_voice import OPENAI_API_KEY, SYSTEM_MESSAGE, TEMPERATURE, PERSONA
import websockets

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

    async with websockets.connect(
        f"wss://api.openai.com/v1/realtime?model=gpt-realtime&temperature={TEMPERATURE}",
        additional_headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
    ) as openai_ws:
        await initialize_session(openai_ws)

        print("openai line opened")

        async def send_call_to_openai():
            slices = 0
            try:
                while True:
                    message = json.loads(await websocket.receive_text())
                    if message["event"] == "media":
                        slices += 1
                        await openai_ws.send(
                            json.dumps(
                                {
                                    "type": "input_audio_buffer.append",
                                    "audio": message["media"]["payload"],
                                }
                            )
                        )
            except WebSocketDisconnect:
                print(f"caller hung up after {slices} slices")
                await openai_ws.close()

        async def read_openai_reply():
            replies = 0
            async for message in openai_ws:
                event = json.loads(message)
                if event["type"] == "response.output_audio.delta":
                    replies += 1
                    print(f"sound back from openai: {replies}")
                elif event["type"] == "error":
                    print("openai said no:", event)

        await asyncio.gather(send_call_to_openai(), read_openai_reply())


async def initialize_session(openai_ws):
    session_update = {
        "type": "session.update",
        "session": {
            "type": "realtime",
            "model": "gpt-realtime",
            "output_modalities": ["audio"],
            "audio": {
                "input": {
                    "format": {"type": "audio/pcmu"},
                    "turn_detection": {"type": "server_vad"},
                },
                "output": {
                    "format": {"type": "audio/pcmu"},
                    "voice": PERSONA["Dana"]["voice"],
                },
            },
            "instructions": SYSTEM_MESSAGE,
        },
    }
    print("Sending session update:", json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))

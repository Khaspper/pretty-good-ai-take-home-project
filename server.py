from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, Response

app = FastAPI()


@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    return "pong"


@app.post("/voice")
def voice() -> Response:
    response = """
    <Response>
        <Say>Yurrrrrrr what you doin cuh</Say>
        <Pause length="12"/>
        <Say>Alright, hanging up.</Say>
    </Response>
    """
    return Response(content=response, media_type="application/xml")

import os
import time
from pathlib import Path
import requests
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.rest.api.v2010.account.recording import RecordingInstance

load_dotenv()

RECORDINGS_DIR = Path("recordings")
FINISHED = "completed"


class RecordingNeverArrived(Exception):
    """Raised when Twilio never finished a recording for a call"""


def wait_for_recording(call_sid: str, timeout: int = 180) -> RecordingInstance:
    # We have to wait for twilio to finish creating the record
    client = Client()
    deadline = time.time() + timeout

    while time.time() < deadline:
        for recording in client.recordings.list(call_sid=call_sid, limit=1):
            if recording.status == FINISHED:
                return recording
        # If nothing found we wait for 3 seconds
        time.sleep(3)

    # Throw if 180 seconds have passed
    raise RecordingNeverArrived(
        f"no finished recording for {call_sid} after {timeout}s"
    )


def fetch_recording(call_sid: str, timeout: int = 90) -> Path:
    # Download the recording for one call and return it
    recording = wait_for_recording(call_sid, timeout)
    url = "https://api.twilio.com" + recording.uri.replace(".json", ".wav")
    answer = requests.get(
        url,
        auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")),
    )
    answer.raise_for_status()

    RECORDINGS_DIR.mkdir(exist_ok=True)
    path = RECORDINGS_DIR / f"{call_sid}.wav"
    path.write_bytes(answer.content)

    print(f"{recording.channels} channels, {recording.duration}s, {path}")
    return path

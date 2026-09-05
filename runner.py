import os
import time

from dotenv import load_dotenv
from twilio.rest import Client

from recording import fetch_recording
from caller import call_number

load_dotenv()

# Twilio stops updating a call once it reaches one of these
ENDED = {"completed", "busy", "no-answer", "canceled", "failed"}


class CallNeverEnded(Exception):
    """Raised when a call is still running long after it should have stopped"""


def wait_for_end(call_sid: str, timeout: int = 300) -> str:
    client = Client()
    # The TTL for watching the call... if it exceeds 300 seconds then the call keeps going byt we don't download the recording...
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = client.calls(call_sid).fetch().status
        if status in ENDED:
            return status
        print(f"call is {status}")
        time.sleep(3)
    raise CallNeverEnded(f"call {call_sid} still running after {timeout}s")


def main() -> None:
    # Temporary: this becomes PGA_LINE once the refuse-to-dial guard goes back on.
    number = os.getenv("MY_PHONE_NUMBER")
    call_sid = call_number(number)
    print(f"placed {call_sid}")

    status = wait_for_end(call_sid)
    print(f"call {status}")
    if status != "completed":
        return

    fetch_recording(call_sid)


if __name__ == "__main__":
    main()

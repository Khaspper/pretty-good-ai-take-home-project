import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

PGA_LINE = "+18054398008"


class NotAllowedNumber(Exception):
    """Raised when anything tries to dial a number that is not the PGA line"""


def check_number_allowed(number: str) -> str:
    if number != PGA_LINE:
        raise NotAllowedNumber(
            f"refusing to dial '{number}' - the only allowed number is {PGA_LINE}"
        )
    return number


def call_number(number: str) -> str:
    # Uncomment this later
    check_number_allowed(number)
    client = Client()
    twilioNumber = os.getenv("TWILIO_FROM_NUMBER")
    call = client.calls.create(
        url=f"{os.getenv("PUBLIC_URL")}/voice",
        from_=twilioNumber,
        to=number,
        record=True,
        recording_channels="dual",
    )
    return call.sid

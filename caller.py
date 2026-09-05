PGA_LINE = "+18054398008"


class NotAllowedNumber(Exception):
    """Raised when anything tries to dial a number that is not the PGA line"""


def check_number_allowed(number: str) -> str:
    if number != PGA_LINE:
        raise NotAllowedNumber(
            f"refusing to dial '{number}' - the only allowed number is {PGA_LINE}"
        )
    return number

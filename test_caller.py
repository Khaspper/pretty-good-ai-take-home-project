from caller import NotAllowedNumber, check_number_allowed


def test_allowed_number_passes():
    number = check_number_allowed("+18054398008")
    assert number == "+18054398008"


def test_other_number_raises():
    try:
        check_number_allowed("123123123123")
    except NotAllowedNumber:
        return
    raise AssertionError("dialed a number it should have refused")


def test_blank_number_raises():
    try:
        check_number_allowed("")
    except NotAllowedNumber:
        return
    raise AssertionError("dialed a blank number it should have refused")


def main():
    test_allowed_number_passes()
    test_other_number_raises()
    test_blank_number_raises()
    print("ok")


if __name__ == "__main__":
    main()

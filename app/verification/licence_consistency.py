import re


def normalize_licence_number(value):
    if not value:
        return None

    return re.sub(
        r"[^A-Z0-9]",
        "",
        value.upper()
    )


def compare_licence_numbers(front_number, back_number):
    """
    Compare independently extracted licence numbers
    from the front OCR and back PDF417 barcode.
    """

    front = normalize_licence_number(front_number)
    back = normalize_licence_number(back_number)

    if not front or not back:
        return {
            "match": False,
            "status": "INCOMPLETE",
            "reason": "Could not extract both licence numbers.",
        }

    if front == back:
        return {
            "match": True,
            "status": "CONSISTENT",
            "reason": "Front OCR matches back PDF417.",
        }

    return {
        "match": False,
        "status": "MISMATCH",
        "reason": "Front OCR does not match back PDF417.",
    }

def normalize_date(value):
    """
    Normalize dates to YYYYMMDD for comparison.

    Examples:
    2029/10/27 -> 20291027
    20291027   -> 20291027
    """
    if not value:
        return None

    digits = re.sub(r"[^0-9]", "", str(value))

    if len(digits) != 8:
        return None

    return digits


def compare_dates(front_date, back_date, field_name="date"):
    """
    Compare a date independently extracted from the
    front of the licence with the PDF417 value.
    """

    front = normalize_date(front_date)
    back = normalize_date(back_date)

    if not front:
        return {
            "match": False,
            "status": "UNREADABLE",
            "reason": f"Front {field_name} could not be read reliably.",
        }

    if not back:
        return {
            "match": False,
            "status": "INCOMPLETE",
            "reason": f"Back {field_name} is unavailable.",
        }

    if front == back:
        return {
            "match": True,
            "status": "CONSISTENT",
            "reason": f"Front {field_name} matches back PDF417.",
        }

    return {
        "match": False,
        "status": "MISMATCH",
        "reason": f"Front {field_name} does not match back PDF417.",
    }
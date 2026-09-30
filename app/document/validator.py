import re
from datetime import datetime, date


def normalize_licence_number(text):
    return re.sub(
        r"[^A-Z0-9]",
        "",
        text.upper()
    )


def valid_ontario_number(text):
    cleaned = normalize_licence_number(
        text
    )

    return bool(
        re.fullmatch(
            r"[A-Z]\d{14}",
            cleaned
        )
    )


def parse_barcode_date(value):
    """
    Parse an AAMVA/PDF417 date in YYYYMMDD format.
    """

    if not value:
        return None

    cleaned = str(value).strip()

    if not re.fullmatch(r"\d{8}", cleaned):
        return None

    try:
        return datetime.strptime(
            cleaned,
            "%Y%m%d"
        ).date()

    except ValueError:
        return None


def check_expiry_date(expiry):
    """
    Determine whether a parsed expiry date
    is expired.
    """

    parsed = parse_barcode_date(
        expiry
    )

    if parsed is None:
        return {
            "valid": False,
            "status": "UNKNOWN",
            "date": None,
        }

    if parsed < date.today():
        return {
            "valid": False,
            "status": "EXPIRED",
            "date": parsed,
        }

    return {
        "valid": True,
        "status": "NOT_EXPIRED",
        "date": parsed,
    }


def check_issue_date(issue):
    """
    Check that the issue date is a valid date
    and is not in the future.
    """

    parsed = parse_barcode_date(
        issue
    )

    if parsed is None:
        return {
            "valid": False,
            "status": "UNKNOWN",
            "date": None,
        }

    if parsed > date.today():
        return {
            "valid": False,
            "status": "FUTURE_DATE",
            "date": parsed,
        }

    return {
        "valid": True,
        "status": "VALID",
        "date": parsed,
    }
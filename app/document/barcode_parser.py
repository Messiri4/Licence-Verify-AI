import re
from datetime import datetime, date


def extract_field(raw_text, code):
    """
    Extract one field from decoded PDF417 data.

    Handles both:
    - real CR/LF characters
    - literal <CR>/<LF> strings returned by some decoders
    """

    if not raw_text:
        return None

    pattern = (
        rf"{re.escape(code)}"
        rf"(.*?)"
        rf"(?=<LF>|<CR>|\r|\n|$)"
    )

    match = re.search(
        pattern,
        raw_text
    )

    if not match:
        return None

    return match.group(1).strip()


def extract_licence_number(raw_text):
    """
    DAQ = customer ID / licence number.
    """
    value = extract_field(raw_text, "DAQ")

    if not value:
        return None

    return re.sub(
        r"[^A-Z0-9]",
        "",
        value.upper()
    )


def extract_barcode_fields(raw_text):
    """
    Extract only the fields needed for licence validation.
    """

    return {
        "licence_number": extract_licence_number(raw_text),

        # Dates
        "expiry_date": extract_field(raw_text, "DBA"),
        "issue_date": extract_field(raw_text, "DBD"),
        "date_of_birth": extract_field(raw_text, "DBB"),

        # Identity
        "last_name": extract_field(raw_text, "DCS"),
        "first_name": extract_field(raw_text, "DAC"),
    }
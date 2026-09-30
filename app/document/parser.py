import re


def parse_licence_text(ocr_results):
    lines = [item["text"] for item in ocr_results]

    combined_text = " ".join(lines)

    parsed = {
        "province": None,
        "licence_number": None,
        "expiry_date": None,
        "raw_text": lines
    }

    # Province detection
    if "ONTARIO" in combined_text.upper():
        parsed["province"] = "Ontario"

    # Temporary licence-number pattern
    # We will refine this after seeing actual OCR output.
    licence_pattern = r"\b[A-Z0-9\-]{10,20}\b"

    matches = re.findall(
        licence_pattern,
        combined_text.upper()
    )

    if matches:
        parsed["licence_number"] = matches[0]

    # Basic date detection
    date_pattern = r"\b\d{4}[-/]\d{2}[-/]\d{2}\b"

    dates = re.findall(
        date_pattern,
        combined_text
    )

    if dates:
        parsed["expiry_date"] = dates[-1]

    return parsed
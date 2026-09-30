from datetime import datetime, date
import re


def parse_document_date(value):
    """
    Parse date formats used by our document sources.

    Supported:
    - ID Analyzer: YYYY-MM-DD
    - PDF417:      YYYYMMDD
    - PDF417:      MMDDYYYY
    """

    if not value:
        return None

    value = str(value).strip()

    formats = [
        "%Y-%m-%d",
        "%Y%m%d",
        "%m%d%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(
                value,
                fmt
            ).date()
        except ValueError:
            continue

    return None

def parse_aamva_date(value):
    """
    Backward-compatible wrapper for existing code.
    """

    return parse_document_date(value)


def validate_required_fields(fields):
    """
    Check whether essential document fields exist.
    """

    required = [
        "licence_number",
        "expiry_date",
        "issue_date",
        "date_of_birth",
    ]

    missing = [
        field
        for field in required
        if not fields.get(field)
    ]

    return {
        "valid": len(missing) == 0,
        "status": (
            "VALID"
            if not missing
            else "MISSING_FIELDS"
        ),
        "missing_fields": missing,
    }


def validate_ontario_number(value):
    """
    Validate the expected Ontario licence-number
    structure used by this application.
    """

    if not value:
        return {
            "valid": False,
            "status": "MISSING",
            "reason": "Licence number is missing.",
        }

    cleaned = re.sub(
        r"[^A-Z0-9]",
        "",
        str(value).upper()
    )

    valid = bool(
        re.fullmatch(
            r"[A-Z]\d{14}",
            cleaned
        )
    )

    return {
        "valid": valid,
        "status": (
            "VALID"
            if valid
            else "INVALID_FORMAT"
        ),
        "reason": (
            "Licence number format is valid."
            if valid
            else "Licence number format is invalid."
        ),
    }


def validate_expiry(expiry_value):
    """
    Check whether the document has expired.
    """

    expiry = parse_document_date(
    expiry_value
)

    if expiry is None:
        return {
            "valid": False,
            "status": "UNKNOWN",
            "reason": (
                "Expiry date could not be parsed."
            ),
            "expiry_date": None,
        }

    today = date.today()

    if expiry < today:
        return {
            "valid": False,
            "status": "EXPIRED",
            "reason": (
                "Licence expiry date has passed."
            ),
            "expiry_date": expiry,
        }

    return {
        "valid": True,
        "status": "NOT_EXPIRED",
        "reason": (
            "Licence expiry date has not passed."
        ),
        "expiry_date": expiry,
    }


def validate_issue_date(
    issue_value,
    expiry_value
):
    """
    Check issue-date chronology.
    """

    issue = parse_document_date(
        issue_value
    )

    expiry = parse_document_date(
        expiry_value
    )

    if issue is None:
        return {
            "valid": False,
            "status": "UNKNOWN",
            "reason": (
                "Issue date could not be parsed."
            ),
        }

    today = date.today()

    if issue > today:
        return {
            "valid": False,
            "status": "FUTURE_ISSUE_DATE",
            "reason": (
                "Issue date is in the future."
            ),
        }

    if (
        expiry is not None
        and issue > expiry
    ):
        return {
            "valid": False,
            "status": "INVALID_DATE_ORDER",
            "reason": (
                "Issue date occurs after "
                "expiry date."
            ),
        }

    return {
        "valid": True,
        "status": "VALID",
        "reason": (
            "Issue date is chronologically "
            "consistent."
        ),
    }


def validate_dob(dob_value):
    """
    Validate basic DOB chronology.
    """

    dob = parse_document_date(
        dob_value
    )

    if dob is None:
        return {
            "valid": False,
            "status": "UNKNOWN",
            "reason": (
                "Date of birth could not be parsed."
            ),
        }

    today = date.today()

    if dob > today:
        return {
            "valid": False,
            "status": "FUTURE_DOB",
            "reason": (
                "Date of birth is in the future."
            ),
        }

    return {
        "valid": True,
        "status": "VALID",
        "reason": (
            "Date of birth is chronologically valid."
        ),
    }


def validate_jurisdiction(fields):
    """
    Check whether the extracted document identifies
    Ontario as its jurisdiction.
    """

    province = str(
        fields.get("province") or ""
    ).strip().upper()

    accepted = {
        "ON",
        "ONTARIO",
    }

    valid = province in accepted

    return {
        "valid": valid,
        "status": (
            "ONTARIO"
            if valid
            else "NOT_ONTARIO"
        ),
        "reason": (
            "Document jurisdiction is Ontario."
            if valid
            else
            "Document was not identified as Ontario."
        ),
    }


def validate_document(fields):
    """
    Run the complete local document-field
    validation stage.
    """

    required = validate_required_fields(
        fields
    )

    number = validate_ontario_number(
        fields.get("licence_number")
    )

    expiry = validate_expiry(
        fields.get("expiry_date")
    )

    issue = validate_issue_date(
        fields.get("issue_date"),
        fields.get("expiry_date")
    )

    dob = validate_dob(
        fields.get("date_of_birth")
    )

    jurisdiction = validate_jurisdiction(
        fields
    )

    checks = {
        "required_fields": required,
        "licence_number": number,
        "expiry": expiry,
        "issue_date": issue,
        "date_of_birth": dob,
        "jurisdiction": jurisdiction,
    }

    all_valid = all(
        result["valid"]
        for result in checks.values()
    )

    return {
        "valid": all_valid,
        "status": (
            "VALID"
            if all_valid
            else "INVALID"
        ),
        "checks": checks,
    }


# Keep this for existing code that still uses
# barcode-specific validation.
def validate_barcode(fields):
    required_result = validate_required_fields(
        fields
    )

    expiry_result = validate_expiry(
        fields.get("expiry_date")
    )

    issue_result = validate_issue_date(
        fields.get("issue_date"),
        fields.get("expiry_date")
    )

    return {
        "required_fields": required_result,
        "expiry": expiry_result,
        "issue_date": issue_result,
    }
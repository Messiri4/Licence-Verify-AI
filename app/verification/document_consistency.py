from app.verification.licence_consistency import (
    compare_licence_numbers,
    compare_dates,
)


def check_document_consistency(
    front_number,
    back_number,
    front_expiry=None,
    back_expiry=None,
    front_issue=None,
    back_issue=None,
    front_dob=None,
    back_dob=None,
):
    """
    Compare fields independently extracted from
    the front and back of the licence.

    An unreadable optional front field is different
    from a confirmed mismatch.
    """

    licence_number = compare_licence_numbers(
        front_number,
        back_number
    )

    expiry = compare_dates(
        front_expiry,
        back_expiry,
        "expiry date"
    )

    issue = compare_dates(
        front_issue,
        back_issue,
        "issue date"
    )

    dob = compare_dates(
        front_dob,
        back_dob,
        "date of birth"
    )

    results = {
        "licence_number": licence_number,
        "expiry_date": expiry,
        "issue_date": issue,
        "date_of_birth": dob,
    }

    # A confirmed mismatch is much more important
    # than an OCR field that could not be read.
    mismatches = [
        field
        for field, result in results.items()
        if result["status"] == "MISMATCH"
    ]

    unreadable = [
        field
        for field, result in results.items()
        if result["status"] in {
            "UNREADABLE",
            "INCOMPLETE",
        }
    ]

    if mismatches:
        status = "INCONSISTENT"
    elif unreadable:
        status = "PARTIAL"
    else:
        status = "CONSISTENT"

    return {
        "status": status,
        "consistent": len(mismatches) == 0,
        "mismatches": mismatches,
        "unreadable_fields": unreadable,
        "fields": results,
    }
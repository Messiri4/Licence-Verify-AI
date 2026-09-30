def assess_local_document(
    barcode_validation,
    consistency_result
):
    """
    Produce a local document assessment.

    This does NOT represent an official MTO,
    ServiceOntario, or third-party verification.
    """

    required_fields = (
        barcode_validation
        .get("required_fields", {})
        .get("valid", False)
    )

    expiry_valid = (
        barcode_validation
        .get("expiry", {})
        .get("valid", False)
    )

    issue_valid = (
        barcode_validation
        .get("issue_date", {})
        .get("valid", False)
    )

    consistency_status = (
        consistency_result.get(
            "status",
            "UNKNOWN"
        )
    )

    # Hard failures
    if not required_fields:
        return {
            "status": "FAILED",
            "reason": (
                "Required barcode fields "
                "are missing."
            ),
        }

    if not expiry_valid:
        return {
            "status": "FAILED",
            "reason": (
                "Licence expiry validation "
                "failed."
            ),
        }

    if not issue_valid:
        return {
            "status": "FAILED",
            "reason": (
                "Licence issue-date validation "
                "failed."
            ),
        }

    if consistency_status == "INCONSISTENT":
        return {
            "status": "FAILED",
            "reason": (
                "Front and back licence data "
                "contain confirmed mismatches."
            ),
        }

    # Some front OCR fields were unreadable,
    # but no actual mismatch was found.
    if consistency_status == "PARTIAL":
        return {
            "status": "PARTIAL",
            "reason": (
                "Local document checks passed, "
                "but some front fields could not "
                "be independently verified."
            ),
        }

    if consistency_status == "CONSISTENT":
        return {
            "status": "PASSED",
            "reason": (
                "Local document checks passed "
                "and available front/back fields "
                "are consistent."
            ),
        }

    return {
        "status": "UNKNOWN",
        "reason": (
            "Document assessment could not "
            "be completed."
        ),
    }
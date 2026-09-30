def assess_local_verification(
    consistency,
    document_validation,
    identity_verification=None,
):
    """
    Combine local verification stages into one result.

    This does NOT determine official Ontario licence
    status. Official status belongs to the future
    MTO integration.

    Possible results:
        PASS
        PARTIAL
        FAIL
        UNKNOWN
    """

    checks = {
        "cross_source_consistency": None,
        "document_validation": None,
        "identity_verification": None,
    }

    reasons = []

    # ------------------------------------------
    # 1. CROSS-SOURCE CONSISTENCY
    # ------------------------------------------

    if not consistency:
        checks["cross_source_consistency"] = "UNKNOWN"

    else:
        consistency_status = consistency.get(
            "status"
        )

        if consistency_status == "CONSISTENT":
            checks[
                "cross_source_consistency"
            ] = "PASS"

        elif consistency_status == "PARTIAL":
            checks[
                "cross_source_consistency"
            ] = "PARTIAL"

            reasons.append(
                "Some front/back fields could not "
                "be independently compared."
            )

        elif consistency_status == "INCONSISTENT":
            checks[
                "cross_source_consistency"
            ] = "FAIL"

            reasons.append(
                "Front and back licence data are "
                "inconsistent."
            )

        else:
            checks[
                "cross_source_consistency"
            ] = "UNKNOWN"

    # ------------------------------------------
    # 2. DOCUMENT VALIDATION
    # ------------------------------------------

    if not document_validation:
        checks["document_validation"] = "UNKNOWN"

    else:
        validation_status = document_validation.get(
            "status"
        )

        if validation_status == "VALID":
            checks["document_validation"] = "PASS"

        elif validation_status == "INVALID":
            checks["document_validation"] = "FAIL"

            reasons.append(
                "One or more document validation "
                "checks failed."
            )

        else:
            checks["document_validation"] = "UNKNOWN"

    # ------------------------------------------
    # 3. IDENTITY VERIFICATION
    # ------------------------------------------

    if not identity_verification:
        checks["identity_verification"] = "UNKNOWN"

    else:
        identity_status = identity_verification.get(
            "status"
        )

        if identity_status in {
            "VERIFIED",
            "MATCH",
        }:
            checks["identity_verification"] = "PASS"

        elif identity_status in {
            "NOT_VERIFIED",
            "NO_MATCH",
            "FAILED",
        }:
            checks["identity_verification"] = "FAIL"

            reasons.append(
                "Identity verification failed."
            )

        elif identity_status == "PARTIAL":
            checks["identity_verification"] = "PARTIAL"

        else:
            checks["identity_verification"] = "UNKNOWN"

    # ------------------------------------------
    # FINAL LOCAL DECISION
    # ------------------------------------------

    statuses = list(
        checks.values()
    )

    # A confirmed failure takes priority.
    if "FAIL" in statuses:
        final_status = "FAIL"

    # Everything passed.
    elif all(
        status == "PASS"
        for status in statuses
    ):
        final_status = "PASS"

    # At least one successful check, but some
    # information is incomplete.
    elif (
        "PASS" in statuses
        and any(
            status in {
                "PARTIAL",
                "UNKNOWN",
            }
            for status in statuses
        )
    ):
        final_status = "PARTIAL"

    # Nothing was sufficiently verified.
    else:
        final_status = "UNKNOWN"

    # ------------------------------------------
    # DEFAULT REASON
    # ------------------------------------------

    if not reasons:

        if final_status == "PASS":
            reasons.append(
                "All available local verification "
                "checks passed."
            )

        elif final_status == "PARTIAL":
            reasons.append(
                "Local verification was only "
                "partially completed."
            )

        elif final_status == "UNKNOWN":
            reasons.append(
                "Insufficient information was "
                "available for local verification."
            )

    return {
        "status": final_status,
        "checks": checks,
        "reasons": reasons,

        # Important architectural boundary.
        "official_licence_status": "NOT_CHECKED",
    }
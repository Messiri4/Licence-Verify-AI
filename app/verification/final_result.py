def build_final_result(
    local_assessment,
    official_status,
):
    """
    Stage 10 — Build the final verification result.

    Local verification and official licence status
    remain separate because they establish different
    facts.
    """

    local_status = (
        local_assessment.get("status", "UNKNOWN")
        if local_assessment
        else "UNKNOWN"
    )

    official_value = (
        official_status.get("status", "NOT_CHECKED")
        if official_status
        else "NOT_CHECKED"
    )

    official_checked = (
        official_status.get("checked", False)
        if official_status
        else False
    )

    # ------------------------------------------
    # FINAL DECISION
    # ------------------------------------------

    if local_status == "FAIL":
        overall = "LOCAL_VERIFICATION_FAILED"

    elif local_status == "UNKNOWN":
        overall = "INSUFFICIENT_LOCAL_INFORMATION"

    elif local_status == "PARTIAL":
        overall = "LOCAL_VERIFICATION_PARTIAL"

    elif (
        local_status == "PASS"
        and not official_checked
    ):
        overall = (
            "LOCAL_PASS_OFFICIAL_NOT_CHECKED"
        )

    elif (
        local_status == "PASS"
        and official_value == "VALID"
    ):
        overall = "VERIFIED"

    elif (
        local_status == "PASS"
        and official_value != "VALID"
    ):
        overall = (
            "LOCAL_PASS_OFFICIAL_NOT_VALID"
        )

    else:
        overall = "UNKNOWN"

    return {
        "overall": overall,

        "local_verification": {
            "status": local_status,
            "checks": (
                local_assessment.get(
                    "checks",
                    {},
                )
                if local_assessment
                else {}
            ),
        },

        "official_licence_status": {
            "status": official_value,
            "checked": official_checked,
            "official": (
                official_status.get(
                    "official",
                    False,
                )
                if official_status
                else False
            ),
            "source": (
                official_status.get(
                    "source"
                )
                if official_status
                else None
            ),
        },
    }
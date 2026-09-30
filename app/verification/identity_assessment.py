def assess_identity(
    liveness_result,
    face_result,
    mode="development",
):
    """
    Combine active liveness and face matching into
    the Stage 7 identity-verification result.

    In development mode, the reference identity may
    be a developer test identity rather than the
    actual licence holder.
    """

    mode = mode.upper()

    # ------------------------------------------
    # LIVENESS
    # ------------------------------------------

    if not liveness_result:
        liveness_status = "UNKNOWN"
    else:
        liveness_status = liveness_result.get(
            "status",
            "UNKNOWN",
        ).upper()

    # ------------------------------------------
    # FACE MATCH
    # ------------------------------------------

    if not face_result:
        face_status = "UNKNOWN"
        similarity = None
    else:
        face_status = face_result.get(
            "status",
            "UNKNOWN",
        ).upper()

        similarity = face_result.get(
            "similarity"
        )

    # ------------------------------------------
    # FINAL IDENTITY DECISION
    # ------------------------------------------

    if (
        liveness_status == "PASSED"
        and face_status == "MATCH"
    ):
        status = "VERIFIED"

    elif (
        liveness_status == "FAILED"
        or face_status == "NO_MATCH"
    ):
        status = "NOT_VERIFIED"

    elif (
        liveness_status == "UNKNOWN"
        and face_status == "UNKNOWN"
    ):
        status = "UNKNOWN"

    else:
        status = "PARTIAL"

    return {
        "status": status,
        "liveness": liveness_status,
        "face_match": face_status,
        "similarity": similarity,
        "mode": mode,
    }
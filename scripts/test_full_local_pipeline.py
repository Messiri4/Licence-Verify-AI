from app.verification.licence_status import (
    get_official_licence_status,
)

from app.verification.final_result import (
    build_final_result,
)

from app.verification.identity_pipeline import (
    run_identity_verification,
)

from app.verification.local_pipeline import (
    run_local_verification,
)


FRONT_IMAGE = "data/input/licence_front.jpg"
BACK_IMAGE = "data/input/licence_back.jpg"

# Use the SAME development reference image that
# produced the 0.8042 MATCH in your Stage 7 test.
REFERENCE_IMAGE = (
    "data/test/my_reference_face.jpg"
)


def main():

    print("FULL LOCAL VERIFICATION PIPELINE")
    print("=" * 60)

    # ==========================================
    # STAGE 7 — IDENTITY
    # ==========================================

    print("\nSTAGE 7 — IDENTITY VERIFICATION")
    print("-" * 60)
    print("Mode: DEVELOPMENT")

    identity_result = run_identity_verification(
        reference_image=REFERENCE_IMAGE,
        mode="development",
    )

    print("\nIdentity status:",
          identity_result["status"])

    print("Liveness:",
          identity_result["liveness"])

    print("Face match:",
          identity_result["face_match"])

    print("Similarity:",
          identity_result["similarity"])

    # Don't continue after a confirmed identity
    # failure.
    if identity_result["status"] == "NOT_VERIFIED":
        print(
            "\nLOCAL VERIFICATION STOPPED: "
            "identity verification failed."
        )
        return

    # ==========================================
    # STAGES 3–8
    # ==========================================

    print("\nRUNNING DOCUMENT PIPELINE")
    print("-" * 60)

    result = run_local_verification(
        front_path=FRONT_IMAGE,
        back_path=BACK_IMAGE,
        identity_verification=identity_result,
    )

    # ==========================================
    # RESULTS
    # ==========================================

    print("\nCROSS-SOURCE CONSISTENCY")
    print("-" * 60)

    consistency = result.get("consistency")

    if consistency:
        print("Status:", consistency["status"])
    else:
        print("Status: NOT COMPLETED")

    print("\nDOCUMENT VALIDATION")
    print("-" * 60)

    validation = result.get(
        "document_validation"
    )

    if validation:
        print("Status:", validation["status"])
    else:
        print("Status: NOT COMPLETED")

    print("\nIDENTITY VERIFICATION")
    print("-" * 60)

    identity = result.get(
        "identity_verification"
    )

    if identity:
        print("Status:", identity["status"])
        print("Liveness:", identity["liveness"])
        print("Face match:", identity["face_match"])
        print("Similarity:", identity["similarity"])
        print("Mode:", identity["mode"])

    # ==========================================
    # STAGE 8
    # ==========================================

    print("\nLOCAL VERIFICATION ASSESSMENT")
    print("-" * 60)

    assessment = result.get("assessment")

    if assessment:

        for check, status in assessment[
            "checks"
        ].items():

            print(
                f"{check}: {status}"
            )

        print(
            "\nFINAL LOCAL STATUS:",
            assessment["status"],
        )

    else:
        print(
            "Status:",
            result["status"],
        )

    # ==========================================
    # STAGE 9 BOUNDARY
    # ==========================================

    # ==========================================
    # STAGE 9 — OFFICIAL MTO STATUS
    # ==========================================

    print("\nSTAGE 9 — OFFICIAL MTO STATUS")
    print("-" * 60)

    front_fields = result.get(
        "front_fields",
        {}
    )

    licence_number = front_fields.get(
        "licence_number"
    )

    official_status = get_official_licence_status(
        licence_number
    )

    print(
        "Source:",
        official_status["source"],
    )

    print(
        "Status:",
        official_status["status"],
    )

    print(
        "Checked:",
        official_status["checked"],
    )

    print(
        "Official:",
        official_status["official"],
    )

    print(
        "Reason:",
        official_status["reason"],
    )


    # ==========================================
    # STAGE 10 — FINAL RESULT
    # ==========================================

    print("\nSTAGE 10 — FINAL RESULT")
    print("-" * 60)

    final_result = build_final_result(
        local_assessment=assessment,
        official_status=official_status,
    )

    print(
        "Local verification:",
        final_result[
            "local_verification"
        ]["status"],
    )

    print(
        "Official licence status:",
        final_result[
            "official_licence_status"
        ]["status"],
    )

    print(
        "Overall:",
        final_result["overall"],
    )


if __name__ == "__main__":
    main()
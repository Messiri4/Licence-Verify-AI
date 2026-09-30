from app.verification.local_assessment import (
    assess_local_verification,
)


def print_result(name, result):
    print(f"\n{name}")
    print("-" * 50)

    for check, status in result["checks"].items():
        print(f"{check}: {status}")

    print("\nOverall:", result["status"])

    print("Reasons:")
    for reason in result["reasons"]:
        print(f"- {reason}")

    print(
        "Official licence status:",
        result["official_licence_status"],
    )


def main():

    print("LOCAL VERIFICATION ASSESSMENT TEST")
    print("=" * 50)

    # ==========================================
    # TEST 1
    # Everything passed
    # ==========================================

    result = assess_local_verification(
        consistency={
            "status": "CONSISTENT",
        },
        document_validation={
            "status": "VALID",
        },
        identity_verification={
            "status": "VERIFIED",
        },
    )

    print_result(
        "TEST 1 — ALL CHECKS PASS",
        result,
    )

    # ==========================================
    # TEST 2
    # Identity verification unavailable
    # ==========================================

    result = assess_local_verification(
        consistency={
            "status": "CONSISTENT",
        },
        document_validation={
            "status": "VALID",
        },
        identity_verification=None,
    )

    print_result(
        "TEST 2 — IDENTITY UNKNOWN",
        result,
    )

    # ==========================================
    # TEST 3
    # Document validation failed
    # ==========================================

    result = assess_local_verification(
        consistency={
            "status": "CONSISTENT",
        },
        document_validation={
            "status": "INVALID",
        },
        identity_verification={
            "status": "VERIFIED",
        },
    )

    print_result(
        "TEST 3 — DOCUMENT FAILURE",
        result,
    )

    # ==========================================
    # TEST 4
    # Nothing available
    # ==========================================

    result = assess_local_verification(
        consistency=None,
        document_validation=None,
        identity_verification=None,
    )

    print_result(
        "TEST 4 — NO RESULTS",
        result,
    )


if __name__ == "__main__":
    main()
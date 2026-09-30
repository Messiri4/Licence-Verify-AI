from app.verification.local_pipeline import (
    run_local_verification,
)


FRONT_IMAGE = "data/input/licence_front.jpg"
BACK_IMAGE = "data/input/licence_back.jpg"


def main():

    print("END-TO-END LOCAL VERIFICATION")
    print("=" * 50)

    result = run_local_verification(
        front_path=FRONT_IMAGE,
        back_path=BACK_IMAGE,

        # Stage 7 will be integrated next.
        identity_verification=None,
    )

    print("\nFIELD EXTRACTION")
    print("-" * 50)

    extraction = result.get(
        "extraction"
    )

    if extraction:
        print(
            "Success:",
            extraction["success"]
        )

        print(
            "Source:",
            extraction["source"]
        )

    print("\nCROSS-SOURCE CONSISTENCY")
    print("-" * 50)

    consistency = result.get(
        "consistency"
    )

    if consistency:
        print(
            "Status:",
            consistency["status"]
        )
    else:
        print("Status: NOT COMPLETED")

    print("\nDOCUMENT VALIDATION")
    print("-" * 50)

    validation = result.get(
        "document_validation"
    )

    if validation:
        print(
            "Status:",
            validation["status"]
        )
    else:
        print("Status: NOT COMPLETED")

    print("\nIDENTITY VERIFICATION")
    print("-" * 50)

    identity = result.get(
        "identity_verification"
    )

    if identity:
        print(
            "Status:",
            identity.get("status")
        )
    else:
        print("Status: NOT COMPLETED")

    print("\nLOCAL ASSESSMENT")
    print("-" * 50)

    assessment = result.get(
        "assessment"
    )

    if assessment:
        print(
            "Status:",
            assessment["status"]
        )

        print("\nChecks:")

        for check, status in assessment[
            "checks"
        ].items():
            print(
                f"  {check}: {status}"
            )
    else:
        print(
            "Status:",
            result["status"]
        )

    print("\nOFFICIAL LICENCE STATUS")
    print("-" * 50)

    print(
        result.get(
            "official_licence_status",
            "NOT_CHECKED",
        )
    )


if __name__ == "__main__":
    main()
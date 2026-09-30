from app.verification.identity_assessment import (
    assess_identity,
)


def run_test(
    name,
    liveness,
    face,
):
    result = assess_identity(
        liveness,
        face,
        mode="development",
    )

    print(f"\n{name}")
    print("-" * 50)
    print("Status:", result["status"])
    print("Liveness:", result["liveness"])
    print("Face match:", result["face_match"])
    print("Similarity:", result["similarity"])
    print("Mode:", result["mode"])


def main():

    print("IDENTITY ASSESSMENT TEST")
    print("=" * 50)

    run_test(
        "TEST 1 — LIVENESS + FACE MATCH",
        {"status": "PASSED"},
        {
            "status": "MATCH",
            "similarity": 0.97,
        },
    )

    run_test(
        "TEST 2 — LIVENESS FAILURE",
        {"status": "FAILED"},
        {
            "status": "MATCH",
            "similarity": 0.97,
        },
    )

    run_test(
        "TEST 3 — FACE MISMATCH",
        {"status": "PASSED"},
        {
            "status": "NO_MATCH",
            "similarity": 0.31,
        },
    )

    run_test(
        "TEST 4 — LIVENESS ONLY",
        {"status": "PASSED"},
        None,
    )


if __name__ == "__main__":
    main()
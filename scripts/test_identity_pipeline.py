from app.verification.identity_pipeline import (
    run_identity_verification,
)


# IMPORTANT:
# This is the same development reference image
# you previously used successfully with
# test_identity_verification.py.
REFERENCE_IMAGE = (
    "data/test/my_reference_face.jpg"
)


def main():

    print("STAGE 7 — IDENTITY VERIFICATION")
    print("=" * 50)
    print("Mode: DEVELOPMENT")
    print(
        "Look straight at the camera "
        "during calibration."
    )

    result = run_identity_verification(
        reference_image=REFERENCE_IMAGE,
        mode="development",
    )

    print("\nIDENTITY RESULT")
    print("-" * 50)

    print(
        "Status:",
        result["status"],
    )

    print(
        "Liveness:",
        result["liveness"],
    )

    print(
        "Face match:",
        result["face_match"],
    )

    print(
        "Similarity:",
        result["similarity"],
    )

    print(
        "Mode:",
        result["mode"],
    )


if __name__ == "__main__":
    main()
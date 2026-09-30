from app.face.webcam import (
    capture_live_face,
)

from app.verification.identity_verifier import (
    verify_faces,
)


REFERENCE_IMAGE = (
    "data/test/my_reference_face.jpg"
)


def main():
    print("IDENTITY VERIFICATION")
    print("=" * 50)

    print("Mode: DEVELOPMENT")
    print(
        "Reference: development test identity"
    )

    print("\nCapture a live face.")
    print("-" * 50)

    live_image = capture_live_face()

    if live_image is None:
        print("Capture cancelled.")
        return

    result = verify_faces(
        reference_image=REFERENCE_IMAGE,
        live_image=live_image,
        mode="development",
    )

    print("\nFACE MATCH")
    print("-" * 50)

    print(
        "Status:",
        result["status"]
    )

    print(
        "Match:",
        result["match"]
    )

    if result["similarity"] is not None:
        print(
            "Similarity:",
            f"{result['similarity']:.4f}"
        )

    print(
        "Threshold:",
        result["threshold"]
    )

    print(
        "Mode:",
        result["mode"]
    )


if __name__ == "__main__":
    main()
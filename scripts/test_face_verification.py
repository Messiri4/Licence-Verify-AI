from app.document.portrait_extractor import (
    extract_portrait_roi
)
from app.face.face_detector import (
    extract_face_from_image
)
from app.face.face_matcher import (
    create_embedding,
    compare_embeddings
)
from app.face.webcam import (
    capture_live_face
)


LICENCE_IMAGE = (
    "data/output/cropped_licence.jpg"
)

PORTRAIT_IMAGE = (
    "data/output/portrait_roi.jpg"
)


def main():
    print(
        "Extracting licence portrait..."
    )

    # Step 1:
    # Extract the portrait using the Ontario
    # driver's licence template.
    extract_portrait_roi(
        LICENCE_IMAGE,
        PORTRAIT_IMAGE
    )

    # Step 2:
    # Detect and align the face inside
    # the extracted portrait.
    licence_face = extract_face_from_image(
        PORTRAIT_IMAGE
    )

    if licence_face is None:
        print(
            "No face detected "
            "in licence portrait."
        )
        return

    print(
        "Licence face detected."
    )

    licence_embedding = create_embedding(
        licence_face
    )

    # Step 3:
    # Capture a live image.
    live_image = capture_live_face()

    if live_image is None:
        print(
            "Capture cancelled."
        )
        return

    # Step 4:
    # Detect the face in the live image.
    live_face = extract_face_from_image(
        live_image
    )

    if live_face is None:
        print(
            "No live face detected."
        )
        return

    # Step 5:
    # Generate the live face embedding.
    live_embedding = create_embedding(
        live_face
    )

    # Step 6:
    # Compare both embeddings.
    similarity = compare_embeddings(
        licence_embedding,
        live_embedding
    )

    print("\nFACE VERIFICATION")
    print("-" * 40)

    print(
        f"Similarity: "
        f"{similarity:.4f}"
    )

    threshold = 0.60

    if similarity >= threshold:
        print(
            "Result: MATCH"
        )
    else:
        print(
            "Result: NO MATCH"
        )


if __name__ == "__main__":
    main()
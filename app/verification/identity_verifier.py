from app.face.face_detector import (
    extract_face_from_image,
)

from app.face.face_matcher import (
    create_embedding,
    compare_embeddings,
)


DEFAULT_THRESHOLD = 0.60


def verify_faces(
    reference_image,
    live_image,
    threshold=DEFAULT_THRESHOLD,
    mode="production",
):
    """
    Compare a reference identity image against
    a captured live image.

    Development:
        reference = developer test image

    Production:
        reference = licence portrait/card image
    """

    reference_face = extract_face_from_image(
        reference_image
    )

    if reference_face is None:
        return {
            "status": "REFERENCE_FACE_NOT_FOUND",
            "match": False,
            "similarity": None,
            "threshold": threshold,
            "mode": mode.upper(),
        }

    live_face = extract_face_from_image(
        live_image
    )

    if live_face is None:
        return {
            "status": "LIVE_FACE_NOT_FOUND",
            "match": False,
            "similarity": None,
            "threshold": threshold,
            "mode": mode.upper(),
        }

    reference_embedding = create_embedding(
        reference_face
    )

    live_embedding = create_embedding(
        live_face
    )

    similarity = compare_embeddings(
        reference_embedding,
        live_embedding
    )

    matched = similarity >= threshold

    return {
        "status": (
            "MATCH"
            if matched
            else "NO_MATCH"
        ),
        "match": matched,
        "similarity": float(similarity),
        "threshold": threshold,
        "mode": mode.upper(),
    }
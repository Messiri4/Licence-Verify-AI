from app.document.portrait_extractor import (
    extract_portrait_roi
)


LICENCE_PATH = (
    "data/output/cropped_licence.jpg"
)

OUTPUT_PATH = (
    "data/output/portrait_roi.jpg"
)


def main():
    extract_portrait_roi(
        LICENCE_PATH,
        OUTPUT_PATH
    )

    print(
        f"Saved: {OUTPUT_PATH}"
    )

    print(
        "Check whether the complete licence "
        "portrait is visible."
    )


if __name__ == "__main__":
    main()
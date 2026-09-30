from app.document.dob_extractor import extract_dob_roi


IMAGE_PATH = "data/output/cropped_licence.jpg"
OUTPUT_PATH = "data/output/dob_roi.jpg"


def main():

    extract_dob_roi(
        IMAGE_PATH,
        OUTPUT_PATH
    )

    print("Saved:", OUTPUT_PATH)
    print("Check whether the complete DOB is visible.")


if __name__ == "__main__":
    main()
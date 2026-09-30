from app.verification.licence_status import (
    get_official_licence_status,
)


def main():

    print("STAGE 9 — OFFICIAL LICENCE STATUS")
    print("=" * 60)

    # We deliberately use a dummy number here.
    result = get_official_licence_status(
        "A1234-56789-01234"
    )

    print("Source:", result["source"])
    print("Status:", result["status"])
    print("Checked:", result["checked"])
    print("Official:", result["official"])
    print("Reason:", result["reason"])


if __name__ == "__main__":
    main()
from app.verification.final_result import (
    build_final_result,
)


def show(name, local, official):

    result = build_final_result(
        local,
        official,
    )

    print(f"\n{name}")
    print("-" * 60)

    print(
        "Local:",
        result["local_verification"]["status"],
    )

    print(
        "Official:",
        result[
            "official_licence_status"
        ]["status"],
    )

    print(
        "Overall:",
        result["overall"],
    )


def main():

    print("STAGE 10 — FINAL RESULT")
    print("=" * 60)

    # Current development situation
    show(
        "TEST 1 — LOCAL PASS / MTO NOT CHECKED",
        {
            "status": "PASS",
            "checks": {},
        },
        {
            "status": "NOT_CHECKED",
            "checked": False,
            "official": False,
            "source": "MTO",
        },
    )

    # Future authorized MTO result
    show(
        "TEST 2 — LOCAL PASS / MTO VALID",
        {
            "status": "PASS",
            "checks": {},
        },
        {
            "status": "VALID",
            "checked": True,
            "official": True,
            "source": "MTO",
        },
    )

    show(
        "TEST 3 — LOCAL PASS / MTO SUSPENDED",
        {
            "status": "PASS",
            "checks": {},
        },
        {
            "status": "SUSPENDED",
            "checked": True,
            "official": True,
            "source": "MTO",
        },
    )

    show(
        "TEST 4 — LOCAL FAILURE",
        {
            "status": "FAIL",
            "checks": {},
        },
        {
            "status": "NOT_CHECKED",
            "checked": False,
            "official": False,
            "source": "MTO",
        },
    )


if __name__ == "__main__":
    main()
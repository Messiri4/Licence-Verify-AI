import cv2


def capture_live_face(
    output_path="data/output/live_face.jpg"
):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError(
            "Could not open webcam."
        )

    window_name = "Live Face Capture"

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL
    )

    captured = None

    print("Click the webcam window.")
    print("SPACE or ENTER = capture")
    print("Q or ESC = cancel")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        display = frame.copy()

        cv2.putText(
            display,
            "SPACE/ENTER = capture",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            window_name,
            display
        )

        key = cv2.waitKeyEx(30)

        if key in (32, 13, 10):
            captured = frame.copy()
            break

        if key in (
            ord("q"),
            ord("Q"),
            27
        ):
            break

    cap.release()
    cv2.destroyAllWindows()

    if captured is None:
        return None

    cv2.imwrite(
        output_path,
        captured
    )

    return output_path
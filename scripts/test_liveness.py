import cv2

from app.liveness.head_pose import HeadPoseDetector
from app.liveness.challenge import LivenessChallenge


CALIBRATION_FRAMES = 30


def main():

    print("ACTIVE LIVENESS TEST")
    print("=" * 50)
    print("Look straight at the camera for calibration.")
    print("Press Q or ESC to stop.")

    detector = HeadPoseDetector()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open webcam.")
        return

    # ------------------------------------------
    # CALIBRATION
    # ------------------------------------------

    calibration_h = []
    calibration_pitch = []

    calibrated = False
    challenge = None

    try:

        while True:

            ret, frame = cap.read()

            if not ret:
                print("Could not read webcam frame.")
                break

            result = detector.process(frame)

            # ----------------------------------
            # NO FACE
            # ----------------------------------

            if not result["detected"]:

                overlay_text = "NO FACE"

            # ----------------------------------
            # CALIBRATION
            # ----------------------------------

            elif not calibrated:

                calibration_h.append(
                    result["horizontal_ratio"]
                )

                calibration_pitch.append(
                    result["pitch"]
                )

                overlay_text = (
                    "CALIBRATING - LOOK STRAIGHT"
                )

                if (
                    len(calibration_h)
                    >= CALIBRATION_FRAMES
                ):

                    baseline_h = (
                        sum(calibration_h)
                        / len(calibration_h)
                    )

                    baseline_pitch = (
                        sum(calibration_pitch)
                        / len(calibration_pitch)
                    )

                    detector.calibrate(
                        baseline_h,
                        baseline_pitch
                    )

                    detector.horizontal_history.clear()
                    detector.pitch_history.clear()

                    calibrated = True

                    # Create challenge only AFTER
                    # calibration is complete.
                    challenge = LivenessChallenge(
                        challenge_count=3,
                        required_frames=5,
                        timeout_seconds=10,
                    )

                    print("\nCALIBRATION COMPLETE")
                    print("-" * 50)

                    print(
                        f"Baseline H: "
                        f"{baseline_h:.3f}"
                    )

                    print(
                        f"Baseline Pitch: "
                        f"{baseline_pitch:.1f}"
                    )

                    print("\nCHALLENGE SEQUENCE")
                    print("-" * 50)

                    # Development only.
                    # We'll remove this later.
                    print(
                        " -> ".join(
                            challenge.sequence
                        )
                    )

            # ----------------------------------
            # LIVENESS CHALLENGE
            # ----------------------------------

            else:

                challenge_result = (
                    challenge.update(
                        result["direction"]
                    )
                )

                status = challenge_result[
                    "status"
                ]

                if status == "IN_PROGRESS":

                    instruction = (
                        challenge_result[
                            "instruction"
                        ]
                    )

                    overlay_text = (
                        f"LOOK {instruction}"
                    )

                elif status == "PASSED":

                    overlay_text = (
                        "LIVENESS PASSED"
                    )

                else:

                    overlay_text = (
                        "LIVENESS FAILED"
                    )

            # ----------------------------------
            # OVERLAY
            # ----------------------------------

            cv2.putText(
                frame,
                overlay_text,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )

            # Show detected direction too.
            if (
                result["detected"]
                and calibrated
            ):

                direction_text = (
                    f"Detected: "
                    f"{result['direction']}"
                )

                cv2.putText(
                    frame,
                    direction_text,
                    (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 0),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow(
                "Active Liveness Test",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key in (
                ord("q"),
                27,
            ):
                break

    finally:

        cap.release()
        cv2.destroyAllWindows()
        detector.close()


if __name__ == "__main__":
    main()
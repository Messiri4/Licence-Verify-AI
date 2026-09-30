import cv2

from app.liveness.head_pose import (
    HeadPoseDetector,
)


def main():
    detector = HeadPoseDetector()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open webcam.")
        return

    print("HEAD POSE TEST")
    print("=" * 50)

    print(
        "Move your head LEFT, RIGHT, "
        "UP and DOWN."
    )

    print("Press Q or ESC to stop.")

    calibration_h = []
    calibration_pitch = []
    CALIBRATION_FRAMES = 30
    calibrated = False

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Could not read webcam.")
            break

        result = detector.process(
            frame
        )

        # ------------------------------------------
        # NEUTRAL POSITION CALIBRATION
        # ------------------------------------------

        if result["detected"] and not calibrated:

            calibration_h.append(
                result["horizontal_ratio"]
            )

            calibration_pitch.append(
                result["pitch"]
            )

            if len(calibration_h) >= CALIBRATION_FRAMES:

                baseline_h = (
                    sum(calibration_h)
                    / len(calibration_h)
                )

                baseline_pitch = (
                    sum(calibration_pitch)
                    / len(calibration_pitch)
                )

                # Set the neutral head position
                detector.calibrate(
                    baseline_h,
                    baseline_pitch
                )

                # Clear smoothing history so calibration
                # frames don't affect movement detection.
                detector.horizontal_history.clear()
                detector.pitch_history.clear()

                calibrated = True

                print("\nCALIBRATION COMPLETE")
                print("-" * 50)
                print(
                    f"Baseline H: {baseline_h:.3f}"
                )
                print(
                    f"Baseline Pitch: {baseline_pitch:.1f}"
                )

                print("\nCALIBRATION COMPLETE")
                print("-" * 50)
                print(f"Baseline H: {baseline_h:.3f}")
                print(
                    f"Baseline Pitch: "
                    f"{baseline_pitch:.1f}"
                )

         # ------------------------------------------
        # DEBUG OUTPUT AFTER CALIBRATION
        # ------------------------------------------

        if result["detected"] and calibrated:

            h_delta = (
                result["horizontal_ratio"]
                - detector.baseline_horizontal
            )

            pitch_delta = (
                result["pitch"]
                - detector.baseline_pitch
            )

            print(
                f"HΔ={h_delta:+.3f} | "
                f"PitchΔ={pitch_delta:+.1f} | "
                f"Direction={result['direction']}"
            )

        # ------------------------------------------
        # DIRECTION OVERLAY
        # ------------------------------------------

        if result["detected"]:

            if not calibrated:
                overlay_text = "CALIBRATING - LOOK STRAIGHT"

            else:
                direction = result["direction"]
                overlay_text = f"Direction: {direction}"

        else:
            overlay_text = "NO FACE"


        cv2.putText(
            frame,
            overlay_text,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),   # Black text
            2,
            cv2.LINE_AA
        )

        cv2.imshow(
            "Head Pose Test",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key in (
            ord("q"),
            27,
        ):
            break

    cap.release()
    detector.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
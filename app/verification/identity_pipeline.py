import cv2
from pathlib import Path

from app.liveness.head_pose import HeadPoseDetector
from app.liveness.challenge import LivenessChallenge
from app.verification.identity_verifier import verify_faces
from app.verification.identity_assessment import assess_identity


CALIBRATION_FRAMES = 30


def run_identity_verification(
    reference_image,
    mode="development",
    camera_index=0,
):
    """
    Run Stage 7:

    1. Calibrate neutral head position
    2. Run randomized active-liveness challenge
    3. Capture live face after successful liveness
    4. Compare live face against reference
    5. Produce combined identity result

    DEVELOPMENT:
        reference_image may be the developer's
        test identity.

    PRODUCTION:
        reference_image must represent the
        submitted licence holder.
    """

    detector = HeadPoseDetector()

    cap = cv2.VideoCapture(
        camera_index
    )

    if not cap.isOpened():
        detector.close()

        return {
            "status": "UNKNOWN",
            "liveness": "UNKNOWN",
            "face_match": "UNKNOWN",
            "similarity": None,
            "mode": mode.upper(),
            "reason": "Could not open webcam.",
        }

    calibration_h = []
    calibration_pitch = []

    calibrated = False
    challenge = None

    liveness_result = None
    captured_frame = None

    # After liveness passes, require the user to
    # return to a stable frontal position before
    # capturing the image for FaceNet.
    waiting_for_center = False
    center_counter = 0
    CENTER_REQUIRED_FRAMES = 8

    try:

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            result = detector.process(
                frame
            )

            # ==================================
            # NO FACE
            # ==================================

            if not result["detected"]:

                overlay_text = "NO FACE"

            # ==================================
            # CALIBRATION
            # ==================================

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
                        baseline_pitch,
                    )

                    detector.horizontal_history.clear()
                    detector.pitch_history.clear()

                    calibrated = True

                    challenge = LivenessChallenge(
                        challenge_count=3,
                        required_frames=5,
                        timeout_seconds=10,
                    )

                    print(
                        "\nLIVENESS CALIBRATION COMPLETE"
                    )

            else:

                # ==================================
                # RETURN TO CENTER FOR FACE CAPTURE
                # ==================================

                if waiting_for_center:

                    overlay_text = (
                        "RETURN TO CENTER"
                    )

                    if result["direction"] == "CENTER":
                        center_counter += 1
                    else:
                        center_counter = 0

                    if (
                        center_counter
                        >= CENTER_REQUIRED_FRAMES
                    ):

                        captured_frame = (
                            frame.copy()
                        )

                        overlay_text = (
                            "FACE CAPTURED"
                        )

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

                        cv2.imshow(
                            "Identity Verification",
                            frame,
                        )

                        cv2.waitKey(500)

                        break

                # ==================================
                # ACTIVE LIVENESS
                # ==================================

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

                        liveness_result = {
                            "status": "PASSED"
                        }

                        waiting_for_center = True

                        overlay_text = (
                            "RETURN TO CENTER"
                        )

                    elif status == "FAILED":

                        liveness_result = {
                            "status": "FAILED"
                        }

                        break

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

                    liveness_result = {
                        "status": "PASSED"
                    }

                    waiting_for_center = True

                    overlay_text = (
                        "RETURN TO CENTER"
                    )

                elif status == "FAILED":

                    liveness_result = {
                        "status": "FAILED"
                    }

                    break

            # ==================================
            # OVERLAY
            # ==================================

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

            if (
                result["detected"]
                and calibrated
            ):

                cv2.putText(
                    frame,
                    (
                        "Detected: "
                        f"{result['direction']}"
                    ),
                    (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 0),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow(
                "Identity Verification",
                frame,
            )

            key = cv2.waitKey(1) & 0xFF

            if key in {
                ord("q"),
                27,
            }:
                break

    finally:

        cap.release()
        cv2.destroyAllWindows()
        detector.close()

    # ==========================================
    # LIVENESS DID NOT COMPLETE
    # ==========================================

    if not liveness_result:

        return assess_identity(
            {
                "status": "UNKNOWN"
            },
            None,
            mode=mode,
        )

    if (
        liveness_result["status"]
        != "PASSED"
    ):

        return assess_identity(
            liveness_result,
            None,
            mode=mode,
        )

    if captured_frame is None:

        return assess_identity(
            liveness_result,
            None,
            mode=mode,
        )

    # ==========================================
    # TEMPORARY LIVE IMAGE
    # ==========================================

    output_dir = Path(
        "data/output"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    live_path = (
        output_dir
        / "live_identity_capture.jpg"
    )

    cv2.imwrite(
        str(live_path),
        captured_frame,
    )

    # ==========================================
    # FACE MATCH
    # ==========================================

    face_result = verify_faces(
        reference_image,
        str(live_path),
        mode=mode,
    )

    # ==========================================
    # FINAL STAGE 7 RESULT
    # ==========================================

    return assess_identity(
        liveness_result,
        face_result,
        mode=mode,
    )
from collections import deque
import time

import cv2
import mediapipe as mp
import numpy as np


MODEL_PATH = "models/face_landmarker.task"


class HeadPoseDetector:
    """
    Detect basic head direction using MediaPipe
    Face Landmarker and OpenCV solvePnP.
    """

    def __init__(self):
        base_options = mp.tasks.BaseOptions(
            model_asset_path=MODEL_PATH
        )

        options = (
            mp.tasks.vision.FaceLandmarkerOptions(
                base_options=base_options,
                running_mode=(
                    mp.tasks.vision.RunningMode.VIDEO
                ),
                num_faces=1,
                min_face_detection_confidence=0.5,
                min_face_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )
        )

        self.landmarker = (
            mp.tasks.vision.FaceLandmarker
            .create_from_options(options)
        )

        self.start_time = time.monotonic()
        self.last_timestamp_ms = -1

        self.baseline_horizontal = None
        self.baseline_pitch = None

        self.horizontal_history = deque(maxlen=5)
        self.pitch_history = deque(maxlen=5)

    def calibrate(self, horizontal_ratio, pitch):
        """
        Store the user's neutral forward-facing position.
        """

        self.baseline_horizontal = horizontal_ratio
        self.baseline_pitch = pitch    

    def _timestamp_ms(self):
        """
        Return a strictly increasing timestamp.

        MediaPipe VIDEO mode requires every frame
        timestamp to be greater than the previous one.
        """

        timestamp = int(
            (
                time.monotonic()
                - self.start_time
            )
            * 1000
        )

        if timestamp <= self.last_timestamp_ms:
            timestamp = (
                self.last_timestamp_ms + 1
            )

        self.last_timestamp_ms = timestamp

        return timestamp

    def process(self, frame):
        """
        Process one OpenCV webcam frame.

        Returns head-pose information.
        """

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = (
            self.landmarker.detect_for_video(
                mp_image,
                self._timestamp_ms()
            )
        )

        if not result.face_landmarks:
            return {
                "detected": False,
                "yaw": None,
                "pitch": None,
                "direction": None,
            }

        landmarks = result.face_landmarks[0]

        # Horizontal face reference points
        left_face = landmarks[234]
        right_face = landmarks[454]
        nose = landmarks[1]

        face_width = (
            right_face.x - left_face.x
        )

        if abs(face_width) < 1e-6:
            horizontal_ratio = 0.0
        else:
            face_center_x = (
                left_face.x + right_face.x
            ) / 2

            horizontal_ratio = (
                nose.x - face_center_x
            ) / abs(face_width)

        height, width = frame.shape[:2]

        # MediaPipe landmark indices:
        #
        # 1   = nose
        # 152 = chin
        # 33  = left eye outer area
        # 263 = right eye outer area
        # 61  = left mouth corner
        # 291 = right mouth corner

        indices = [
            1,
            152,
            33,
            263,
            61,
            291,
        ]

        image_points = np.array(
            [
                (
                    landmarks[index].x * width,
                    landmarks[index].y * height,
                )
                for index in indices
            ],
            dtype=np.float64,
        )

        # Approximate generic 3D facial model.
        model_points = np.array(
            [
                (0.0, 0.0, 0.0),
                (0.0, -63.6, -12.5),
                (-43.3, 32.7, -26.0),
                (43.3, 32.7, -26.0),
                (-28.9, -28.9, -24.1),
                (28.9, -28.9, -24.1),
            ],
            dtype=np.float64,
        )

        focal_length = float(width)

        camera_matrix = np.array(
            [
                [
                    focal_length,
                    0,
                    width / 2,
                ],
                [
                    0,
                    focal_length,
                    height / 2,
                ],
                [
                    0,
                    0,
                    1,
                ],
            ],
            dtype=np.float64,
        )

        distortion = np.zeros(
            (4, 1),
            dtype=np.float64
        )

        success, rotation_vector, _ = (
            cv2.solvePnP(
                model_points,
                image_points,
                camera_matrix,
                distortion,
                flags=cv2.SOLVEPNP_ITERATIVE,
            )
        )

        if not success:
            return {
                "detected": True,
                "yaw": None,
                "pitch": None,
                "direction": "UNKNOWN",
            }

        rotation_matrix, _ = (
            cv2.Rodrigues(
                rotation_vector
            )
        )

        angles, _, _, _, _, _ = cv2.RQDecomp3x3(
            rotation_matrix
        )

        pitch = float(angles[0])
        yaw = float(angles[1])
        roll = float(angles[2])

        # Normalize pitch because solvePnP can represent
        # the forward-facing orientation close to +/-180 degrees.
        if pitch > 90:
            pitch -= 180
        elif pitch < -90:
            pitch += 180

        # Normalize yaw if necessary.
        if yaw > 90:
            yaw -= 180
        elif yaw < -90:
            yaw += 180

        # ------------------------------------------
        # TEMPORAL SMOOTHING
        # ------------------------------------------

        self.horizontal_history.append(
            horizontal_ratio
        )

        self.pitch_history.append(
            pitch
        )

        smoothed_horizontal = (
            sum(self.horizontal_history)
            / len(self.horizontal_history)
        )

        smoothed_pitch = (
            sum(self.pitch_history)
            / len(self.pitch_history)
        )    

        direction = self.classify(
            smoothed_horizontal,
            smoothed_pitch
        )

        return {
            "detected": True,

            # Smoothed values used for classification
            "horizontal_ratio": smoothed_horizontal,
            "pitch": smoothed_pitch,

            # Raw values useful while debugging
            "raw_horizontal_ratio": horizontal_ratio,
            "raw_pitch": pitch,

            "yaw": yaw,
            "roll": roll,
            "direction": direction,
        }

    def classify(self, horizontal_ratio, pitch):
        """
        Classify movement relative to the calibrated
        neutral head position.
        """

        if (
            self.baseline_horizontal is None
            or self.baseline_pitch is None
        ):
            return "UNCALIBRATED"

        horizontal_delta = (
            horizontal_ratio
            - self.baseline_horizontal
        )

        pitch_delta = (
            pitch
            - self.baseline_pitch
        )

        HORIZONTAL_THRESHOLD = 0.15
        PITCH_THRESHOLD = 15.0

        # Determine how strongly each axis has moved
        # relative to its threshold.
        horizontal_strength = (
            abs(horizontal_delta)
            / HORIZONTAL_THRESHOLD
        )

        vertical_strength = (
            abs(pitch_delta)
            / PITCH_THRESHOLD
        )

        # Nothing moved enough.
        if (
            horizontal_strength < 1.0
            and vertical_strength < 1.0
        ):
            return "CENTER"

        # Whichever axis moved more significantly wins.
        if horizontal_strength > vertical_strength:

            if horizontal_delta < 0:
                return "RIGHT"

            return "LEFT"

        if pitch_delta < 0:
            return "UP"

        return "DOWN"

    def close(self):
        self.landmarker.close()
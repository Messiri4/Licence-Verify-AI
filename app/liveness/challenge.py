import random
import time


class LivenessChallenge:
    """
    Runs a randomized head-movement challenge.

    A requested movement must be detected for several
    consecutive frames before it counts as completed.
    """

    MOVEMENTS = [
        "LEFT",
        "RIGHT",
        "UP",
        "DOWN",
    ]

    def __init__(
        self,
        challenge_count=3,
        required_frames=5,
        timeout_seconds=10,
    ):
        self.challenge_count = challenge_count
        self.required_frames = required_frames
        self.timeout_seconds = timeout_seconds

        self.sequence = random.sample(
            self.MOVEMENTS,
            k=min(
                challenge_count,
                len(self.MOVEMENTS)
            )
        )

        self.current_index = 0
        self.hold_counter = 0
        self.challenge_started = time.monotonic()

        self.completed = []
        self.failed = False

    @property
    def current_challenge(self):
        if self.current_index >= len(self.sequence):
            return None

        return self.sequence[self.current_index]

    @property
    def is_complete(self):
        return (
            self.current_index
            >= len(self.sequence)
        )

    def update(self, detected_direction):
        """
        Process one frame of head-pose information.
        """

        if self.is_complete:
            return {
                "status": "PASSED",
                "instruction": None,
            }

        if self.failed:
            return {
                "status": "FAILED",
                "instruction": None,
            }

        # --------------------------------------
        # TIMEOUT
        # --------------------------------------

        elapsed = (
            time.monotonic()
            - self.challenge_started
        )

        if elapsed > self.timeout_seconds:
            self.failed = True

            return {
                "status": "FAILED",
                "instruction": self.current_challenge,
                "reason": "TIMEOUT",
            }

        expected = self.current_challenge

        # --------------------------------------
        # MOVEMENT CONFIRMATION
        # --------------------------------------

        if detected_direction == expected:
            self.hold_counter += 1
        else:
            self.hold_counter = 0

        # Require several consecutive frames.
        if self.hold_counter >= self.required_frames:

            self.completed.append(expected)

            self.current_index += 1
            self.hold_counter = 0
            self.challenge_started = time.monotonic()

            if self.is_complete:
                return {
                    "status": "PASSED",
                    "instruction": None,
                }

        return {
            "status": "IN_PROGRESS",
            "instruction": self.current_challenge,
            "completed": list(self.completed),
            "progress": (
                f"{self.current_index + 1}/"
                f"{len(self.sequence)}"
            ),
        }
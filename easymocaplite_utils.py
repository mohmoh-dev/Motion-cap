"""
Common utilities for EasyMocapLite.
"""

import time

# MediaPipe 33 landmark names mapped to human skeleton joints.
JOINT_MAP = {
    "Hip": 23,  # LEFT_HIP
    "Spine": 24,  # LEFT_SHOULDER
    "Head": 0,   # NOSE
    "LeftShoulder": 11,
    "LeftElbow": 13,
    "LeftWrist": 15,
    "RightShoulder": 12,
    "RightElbow": 14,
    "RightWrist": 16,
    "LeftHip": 23,
    "LeftKnee": 25,
    "LeftAnkle": 27,
    "RightHip": 24,
    "RightKnee": 26,
    "RightAnkle": 28,
}

JOINT_NAMES = list(JOINT_MAP.keys())

def get_timestamp():
    """Get current timestamp in milliseconds."""
    return int(time.time() * 1000)

def get_fps(prev_time, curr_time):
    """Calculate FPS given previous and current time (in seconds)."""
    return 1.0 / max(curr_time - prev_time, 1e-6)
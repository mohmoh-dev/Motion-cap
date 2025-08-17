"""
Capture webcam frames and extract skeleton using MediaPipe.
"""

import cv2
import mediapipe as mp
import numpy as np
from .utils import JOINT_MAP, get_timestamp

class PoseCapture:
    def __init__(self, src=0, draw_landmarks=True):
        self.cap = cv2.VideoCapture(src)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.draw_landmarks = draw_landmarks
        self.mp_drawing = mp.solutions.drawing_utils

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)
        joints = {}
        if results.pose_landmarks:
            for joint, idx in JOINT_MAP.items():
                lm = results.pose_landmarks.landmark[idx]
                joints[joint] = (lm.x, lm.y, lm.z)
            if self.draw_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return frame, joints

    def release(self):
        self.cap.release()
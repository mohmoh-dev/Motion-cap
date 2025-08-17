"""
Record webcam motion to CSV using EasyMocapLite.
"""

import time
from easymocaplite.capture import PoseCapture
from easymocaplite.record import MotionRecorder
from easymocaplite.utils import get_timestamp

def main():
    cap = PoseCapture()
    recorder = MotionRecorder('output_motion.csv')
    prev_time = time.time()

    print("Press 'q' to quit recording.")
    while True:
        frame, joints = cap.read()
        if frame is None:
            break
        timestamp = get_timestamp()
        if joints:
            recorder.add_frame(timestamp, joints)
        cv2.imshow("EasyMocapLite", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        curr_time = time.time()
        # Aim for ~30fps
        sleep_time = max(0, 1.0/30 - (curr_time - prev_time))
        time.sleep(sleep_time)
        prev_time = curr_time

    recorder.close()
    cap.release()
    print("Recording saved to output_motion.csv")

if __name__ == "__main__":
    import cv2
    main()
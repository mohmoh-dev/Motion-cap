"""
Stream webcam motion live via UDP for Blender.
"""

import time
from easymocaplite.capture import PoseCapture
from easymocaplite.stream import UDPStreamer

def main():
    cap = PoseCapture()
    streamer = UDPStreamer(host='127.0.0.1', port=5005)
    print("Streaming to Blender... Press 'q' to stop.")
    prev_time = time.time()
    while True:
        frame, joints = cap.read()
        if frame is None:
            break
        if joints:
            streamer.send_joints(joints)
        import cv2
        cv2.imshow("EasyMocapLite Live Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        curr_time = time.time()
        sleep_time = max(0, 1.0/30 - (curr_time-prev_time))
        time.sleep(sleep_time)
        prev_time = curr_time
    streamer.close()
    cap.release()
    print("Stopped streaming.")

if __name__ == "__main__":
    main()
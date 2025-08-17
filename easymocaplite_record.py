"""
Record joint positions with timestamps to CSV.
"""

import csv
from .utils import JOINT_NAMES

class MotionRecorder:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'w', newline='')
        self.writer = csv.writer(self.file)
        # CSV header: timestamp + each joint's x, y, z
        header = ['timestamp']
        for joint in JOINT_NAMES:
            header += [f'{joint}_x', f'{joint}_y', f'{joint}_z']
        self.writer.writerow(header)

    def add_frame(self, timestamp, joints):
        row = [timestamp]
        for joint in JOINT_NAMES:
            if joint in joints:
                row += list(joints[joint])
            else:
                row += [None, None, None]
        self.writer.writerow(row)

    def close(self):
        self.file.close()
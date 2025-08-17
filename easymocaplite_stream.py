"""
Stream joint positions live via UDP as JSON packets.
"""

import socket
import json
from .utils import JOINT_NAMES

class UDPStreamer:
    def __init__(self, host='127.0.0.1', port=5005):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_joints(self, joints):
        for joint in JOINT_NAMES:
            if joint in joints:
                x, y, z = joints[joint]
                packet = {
                    'joint': joint,
                    'x': x,
                    'y': y,
                    'z': z
                }
                self.sock.sendto(json.dumps(packet).encode('utf-8'), self.addr)

    def close(self):
        self.sock.close()
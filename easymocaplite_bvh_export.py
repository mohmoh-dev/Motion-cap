"""
Export recorded motion (CSV) to BVH format.
"""

import numpy as np
from .utils import JOINT_NAMES

BVH_JOINTS = [
    "Hip", "Spine", "Head",
    "LeftShoulder", "LeftElbow", "LeftWrist",
    "RightShoulder", "RightElbow", "RightWrist",
    "LeftHip", "LeftKnee", "LeftAnkle",
    "RightHip", "RightKnee", "RightAnkle",
]

BVH_HIERARCHY = {
    "Hip": ["Spine", "LeftHip", "RightHip"],
    "Spine": ["Head", "LeftShoulder", "RightShoulder"],
    "Head": [],
    "LeftShoulder": ["LeftElbow"],
    "LeftElbow": ["LeftWrist"],
    "LeftWrist": [],
    "RightShoulder": ["RightElbow"],
    "RightElbow": ["RightWrist"],
    "RightWrist": [],
    "LeftHip": ["LeftKnee"],
    "LeftKnee": ["LeftAnkle"],
    "LeftAnkle": [],
    "RightHip": ["RightKnee"],
    "RightKnee": ["RightAnkle"],
    "RightAnkle": [],
}

BVH_OFFSETS = {joint: (0, 0, 0) for joint in BVH_JOINTS}  # Placeholder

def load_csv(filename):
    import csv
    frames = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            frame = {}
            for joint in JOINT_NAMES:
                x = float(row.get(f"{joint}_x", 0) or 0)
                y = float(row.get(f"{joint}_y", 0) or 0)
                z = float(row.get(f"{joint}_z", 0) or 0)
                frame[joint] = [x, y, z]
            frames.append(frame)
    return frames

def write_bvh(filename, frames, fps=30):
    with open(filename, 'w') as f:
        # Write hierarchy
        def write_joint(joint, indent=0):
            children = BVH_HIERARCHY[joint]
            offset = BVH_OFFSETS[joint]
            f.write("  " * indent + f"JOINT {joint}\n")
            f.write("  " * indent + "{\n")
            f.write("  " * (indent+1) + f"OFFSET {offset[0]} {offset[1]} {offset[2]}\n")
            f.write("  " * (indent+1) + "CHANNELS 3 Xrotation Yrotation Zrotation\n")
            for child in children:
                write_joint(child, indent+1)
            if not children:
                f.write("  " * (indent+1) + "End Site\n")
                f.write("  " * (indent+1) + "{\n")
                f.write("  " * (indent+2) + "OFFSET 0 0 0\n")
                f.write("  " * (indent+1) + "}\n")
            f.write("  " * indent + "}\n")

        f.write("HIERARCHY\n")
        f.write("ROOT Hip\n{\n")
        f.write("  OFFSET 0 0 0\n")
        f.write("  CHANNELS 6 Xposition Yposition Zposition Xrotation Yrotation Zrotation\n")
        for child in BVH_HIERARCHY["Hip"]:
            write_joint(child, 1)
        f.write("}\n")

        # Write motion
        f.write("MOTION\n")
        f.write(f"Frames: {len(frames)}\n")
        f.write(f"Frame Time: {1.0/fps:.6f}\n")
        for frame in frames:
            # Only position for Hip, rotations for others (set to zero as placeholder)
            hip = frame["Hip"]
            row = [hip[0]*100, hip[1]*100, hip[2]*100, 0, 0, 0]
            for joint in BVH_JOINTS[1:]:
                row += [0, 0, 0]
            f.write(" ".join(f"{v:.4f}" for v in row) + "\n")
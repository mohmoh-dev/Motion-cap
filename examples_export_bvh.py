"""
Export CSV recording to BVH file for Blender.
"""

from easymocaplite.bvh_export import load_csv, write_bvh

def main():
    frames = load_csv('output_motion.csv')
    write_bvh('output_motion.bvh', frames, fps=30)
    print("BVH file saved as output_motion.bvh")

if __name__ == "__main__":
    main()
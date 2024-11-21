import argparse
import numpy as np
import os

def recenter_bvh(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Separate sections
    hierarchy = []
    motion = []
    motion_start_idx = None

    for i, line in enumerate(lines):
        if line.strip() == "MOTION":
            motion_start_idx = i
            break
        hierarchy.append(line)

    if motion_start_idx is None:
        raise ValueError("Invalid BVH file: No MOTION section found.")
    
    motion = lines[motion_start_idx:]
    # Parse initial root position
    root_translation = None
    for line in motion:
        if line.strip().startswith("Frames:"):
            continue
        if line.strip().startswith("Frame Time:"):
            continue
        if line.strip().startswith("MOTION"):
            continue

        frame_data = list(map(float, line.split()))
        root_translation = np.array(frame_data[:3])
        break
    
    if root_translation is None:
        raise ValueError("No root translation data found.")
    
    # Adjust all frames to center root joint
    adjusted_motion = []
    for line in motion:
        if line.strip().startswith("Frames:") or line.strip().startswith("Frame Time:") or line.strip().startswith("MOTION"):
            adjusted_motion.append(line)
        else:
            frame_data = list(map(float, line.split()))
            frame_data[0] -= root_translation[0]  # Adjust X
            frame_data[2] -= root_translation[2]  # Adjust Z
            adjusted_motion.append(" ".join(map(str, frame_data)) + "\n")
    
    # Write output
    with open(input_file, 'w') as file:
        file.writelines(hierarchy + adjusted_motion)


def process_directory(input_directory):
    # Ensure the output directory exists
    if not os.path.exists(input_directory):
        print("Directory not found!")
        return
    
    # Iterate over each .bvh file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".bvh"):
            input_file = os.path.join(input_directory, filename)
            print(f"Processing {input_file}")
            recenter_bvh(input_file)

def main():
    parser = argparse.ArgumentParser(description="Re-center a BVH file's character to start at the origin.")
    parser.add_argument("input_dir", type=str, help="Path to the input BVH file.")

    args = parser.parse_args()

    process_directory(args.input_dir)

if __name__ == "__main__":
    main()

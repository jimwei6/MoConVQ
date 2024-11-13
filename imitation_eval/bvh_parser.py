import pandas as pd
import argparse

def parse_bvh(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    hierarchy = []
    motion_data = []
    frame_time = 0.0
    channels = []

    is_hierarchy = True
    is_motion = False
    current_joint = None

    for line in lines:
        line = line.strip()

        # Parse hierarchy section
        if is_hierarchy:
            if line.startswith("ROOT") or line.startswith("JOINT"):
                joint_name = line.split()[1]
                hierarchy.append(joint_name)
                current_joint = joint_name
            elif line.startswith("CHANNELS"):
                channel_info = line.split()[2:]
                channels.extend([(current_joint, ch) for ch in channel_info])
            elif line.startswith("MOTION"):
                is_hierarchy = False
                is_motion = True

        # Parse motion section
        elif is_motion:
            if line.startswith("Frames:"):
                total_frames = int(line.split()[1])
            elif line.startswith("Frame Time:"):
                frame_time = float(line.split()[2])
            else:
                # Collect motion data
                motion_data.append([float(x) for x in line.split()])
    # Create DataFrame for the motion data
    motion_df = pd.DataFrame(motion_data, columns=[f"{joint}_{channel}" for joint, channel in channels])

    return motion_df, hierarchy, frame_time

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Parse a BVH file and output motion data to a DataFrame.")
    parser.add_argument('file', type=str, help='Path to the BVH file')

    args = parser.parse_args()

    # Parse the BVH file
    motion_df, hierarchy, frame_time = parse_bvh(args.file)

    # Output results
    print("Skeleton Hierarchy:", hierarchy, "Num Skeletons:", len(hierarchy))
    print("Frame Time:", frame_time)
    print(motion_df.head())  # Display first few rows of the motion data
    print(motion_df.info())
    
    print([motion_df.columns.get_loc(c) for c in motion_df.columns if "index" in c or "middle" in c or "pinky" in c or "ring" in c or "thumb" in c or "head" in c or "spine3" in c])

if __name__ == "__main__":
    main()

import re
import argparse

def extract_hierarchy(bvh_file):
    """
    Extract the hierarchy section from a BVH file.

    Args:
        bvh_file (str): Path to the BVH file.

    Returns:
        list: Lines containing the hierarchy section.
    """
    with open(bvh_file, 'r') as f:
        lines = f.readlines()

    hierarchy_lines = []
    for line in lines:
        if 'MOTION' in line:
            break
        hierarchy_lines.append(line)

    return hierarchy_lines

def delete_bvh_columns_and_replace_hierarchy(input_bvh_file, output_bvh_file, columns_to_delete, hierarchy_bvh_file):
    """
    Delete specified frame columns from a BVH file and replace its hierarchy with one from another BVH file.

    Args:
        input_bvh_file (str): Path to the input BVH file.
        output_bvh_file (str): Path to save the modified BVH file.
        columns_to_delete (list): List of indices of the columns to delete (0-indexed).
        hierarchy_bvh_file (str): Path to the BVH file containing the hierarchy to replace with.
    """
    # Step 1: Extract the hierarchy from the specified BVH file
    hierarchy_lines = extract_hierarchy(hierarchy_bvh_file)

    # Step 2: Open the input BVH file to modify
    with open(input_bvh_file, 'r') as f:
        lines = f.readlines()

    # Step 3: Split the input file into the header (skeleton) and motion data sections
    motion_lines = []
    is_motion_section = False

    for line in lines:
        if 'MOTION' in line:
            is_motion_section = True
        if is_motion_section:
            motion_lines.append(line)

    # Extract number of frames and frame time from the motion section
    num_frames = int(re.search(r'\d+', motion_lines[1]).group())
    frame_time = float(re.search(r'[\d\.]+', motion_lines[2]).group())

    # Get the motion data (frames start from index 3 in motion_lines)
    frames_data = [list(map(float, line.strip().split())) for line in motion_lines[3:]]

    # Step 4: Delete the specified columns from the motion data
    modified_frames_data = []
    for frame in frames_data:
        modified_frame = [value for i, value in enumerate(frame) if i not in columns_to_delete]
        modified_frames_data.append(modified_frame)

    for i in range(len(modified_frames_data[0])):
        if(frames_data[0][i] != modified_frames_data[0][i]):
            print(i)

    # Step 5: Write the modified data with the new hierarchy to a new BVH file
    with open(output_bvh_file, 'w') as f:
        # Write the hierarchy section from the specified hierarchy BVH
        f.writelines(hierarchy_lines)

        # Write the motion section
        f.write(f'MOTION\n')
        f.write(f'Frames: {num_frames}\n')
        f.write(f'Frame Time: {frame_time:.6f}\n')

        # Write modified motion data
        for frame in modified_frames_data:
            f.write(' '.join(f'{v:.6f}' for v in frame) + '\n')

    print(f"Specified columns deleted, hierarchy replaced, and new BVH file saved as {output_bvh_file}")

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Delete specified frame columns from a BVH file and replace its hierarchy with another BVH file.')
    parser.add_argument('input_bvh', type=str, help='Path to the input BVH file')
    parser.add_argument('output_bvh', type=str, help='Path to save the modified BVH file')
    parser.add_argument('hierarchy_bvh', type=str, help='Path to the BVH file containing the new hierarchy')

    # Parse arguments
    args = parser.parse_args()

    columns = [36, 37, 38, 42, 43, 44, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158]
    # Call the function with parsed arguments
    delete_bvh_columns_and_replace_hierarchy(args.input_bvh, args.output_bvh, columns, args.hierarchy_bvh)

if __name__ == '__main__':
    main()

#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 file_directory dataset_name output_dir"
    exit 1
fi

# Assign arguments to variables
input_dir=$1
dataset_name=$2
output_dir=$3

if [ -d "$input_dir" ]; then
    mkdir -p "$output_dir"
    for file in "$input_dir"/*; do
            if [ -f "$file" ]; then
                echo $file
                filename=$(basename "$file")
                python "./Script/track_something.py" "-o" "$output_dir/$dataset_name/$filename" "--dataset_name" "$dataset_name" "$file"
                
            fi
        done
else
    echo "Input directory does not exist!"
fi

python "./Script/recenter_bvh.py" "$output_dir/$dataset_name/"


echo "Finished tracking $input_dir"

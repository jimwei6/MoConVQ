#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_dir output_dir"
    exit 1
fi

# Assign arguments to variables
input_dir=$1
output_dir=$2

# Run the first Python file
python './Script/amass_to_moconvq_bvh.py' $input_dir $output_dir './moconvq.bvh'

# Check if the first script ran successfully
if [ $? -ne 0 ]; then
    echo "Error running conversion. Exiting."
    exit 1
fi


python './Script/recenter_bvh.py' $output_dir

# Check if the second script ran successfully
if [ $? -ne 0 ]; then
    echo "Error running recenter. Exiting."
    exit 1
fi

echo "Finished converting $input_dir"

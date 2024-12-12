#!/bin/bash

source /home/abbasih2/miniconda3/etc/profile.d/conda.sh
conda init bash
conda activate sophios_slrum

dataset='SOD1'
current_dir=$(pwd)
platespath="$current_dir/${dataset}/${dataset}_plates.txt"

logs="$current_dir/logs/$dataset"

# Create required directories
mkdir -p "$logs"

# Initialize an empty array to hold plate paths
plates_list=()

# Read the plates file into an array
while IFS= read -r line; do
    plates_list+=("$line")  # Ensure each path is treated as a single entry
done < "$platespath"

# Temporary directory for storing updated WIC files
out_temp="$current_dir/temp"
mkdir -p "$out_temp"

# # Original WIC file
wic_file="$current_dir/wic_workflows/${dataset}_analysis_workflow.wic"
echo $wic_file

# Loop through each plate path and update the WIC file
for plate in "${plates_list[@]}"; do
    plate_name=$(basename "$plate")  # Extract the base name of the plate
    plate_name=$(echo "$plate_name" | tr -d '[:space:]')  # Remove all spaces
    echo "Processing plate: $plate_name"

    # Define paths for output and error logs
    out_log="$logs/${plate_name}.err"
    err_log="$logs/${plate_name}.err"

    updated_wic="$out_temp/$plate_name.wic"

    awk -v new_value="$plate" '
    BEGIN { updated=0; inpDir_found=0 }
    
    # Look for the inpDir line first
    /inpDir:/ && !updated {
        inpDir_found = 1
    }
    
    # Once inpDir is found, update the wic_inline_input on the next occurrence
    inpDir_found && /wic_inline_input:/ && !updated {
        sub(/wic_inline_input: .*/, "wic_inline_input: " new_value)  # Directly use the plate path
        updated = 1  # Set updated to 1 to avoid updating multiple lines
        inpDir_found = 0  # Reset inpDir_found to avoid updating again
    }
    
    # Print all lines, modified or not
    { print }
    ' "$wic_file" > "$updated_wic"

    # Check and print the updated WIC file to confirm changes


    srun -N 1 --mem-per-cpu=50G -p normal_cpu  -o "$out_log" -e "$err_log" sophios --yaml $updated_wic --run_local  --partial_failure_enable  --container_engine singularity --singularity_pull_dir /home/abbasih2/projects/image-workflows/images &




done

echo "All jobs processed successfully."


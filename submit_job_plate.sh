#!/bin/bash

source /home/abbasih2/miniconda3/etc/profile.d/conda.sh
conda init bash
conda activate sophios_slrum

# Insert dataset and current directory from arguments
wic_file=$1
current_dir=$2

logs="$current_dir/logs/$dataset"

# Create required directories
mkdir -p "$logs"

wic_name="${wic_file##*/}"

# Extract the part after the first underscore
wic_name="${wic_name#*_}"

# Extract the part before before '__viz_workflow'
plate_name="${wic_name%%__*}"

# Define paths for output and error logs
out_log="$logs/${plate_name}.err"
err_log="$logs/${plate_name}.err"

# Submit job using srun
echo "Submitting job for: $plate_name"

srun -N 1 --mem-per-cpu=50G -p preempt_cpu \
    -o "$out_log" -e "$err_log" \
    sophios --yaml $wic_file --run_local --partial_failure_enable \
    --container_engine singularity --singularity_pull_dir /home/abbasih2/projects/image-workflows/images &
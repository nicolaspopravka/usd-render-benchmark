#!/bin/bash

# Define arrays for renderers and their corresponding packages
declare -A renderers
renderers=(
    ["Cycles"]="cycles"                         # 5.2.0 + OpenUSD 26.05
)

# Define arrays for scenes, cameras and optional frame specifications
scenes_and_cameras=(
    "assets/full_assets/McUsd/McUsd.usda /McUsd/Camera"
    "assets/full_assets/OpenChessSet/chess_set.usda main_cam"
    "scenes/MoanaIsland/usd/island.usda /island/cam/shotCam"
    "scenes/ALab/ALab/entry.usda /root/camera01/GEO/renderCam_hrc/renderCam_buffer/renderCam_srt/renderCam"
)

# Define problematic combinations of renderer and scene
declare -A problematic_combinations
problematic_combinations=(
    ["Cycles,scenes/MoanaIsland/usd/island.usda"]=1 # /tmp/rez_context_ksn5qef2/context.sh: line 48: 425 Segmentation fault (core dumped) /workspace/usd-render-benchmark/tools/usdrecord_egl.py "$@"
)

# Loop over each renderer
for renderer in "${!renderers[@]}"; do
    package=${renderers[$renderer]}
    
    # Loop over each scene, camera and frame specifications
    for scene_and_camera in "${scenes_and_cameras[@]}"; do
        scene=$(echo $scene_and_camera | awk '{print $1}')
        camera=$(echo $scene_and_camera | awk '{print $2}')
        frames=$(echo $scene_and_camera | awk '{print $3}')
        
        # Check if this combination is problematic
        combination="${renderer},${scene}"
        if [[ -n "${problematic_combinations[$combination]}" ]]; then
            echo "Skipping problematic combination: $combination"
            continue
        fi

        scene_name=$(basename "$scene" | sed 's/\.[^.]*$//')  # Get the scene name without extension
        
        # Determine frames option and modify output path if needed
        if [ -z "$frames" ]; then
            frames_option=""
            output_path="renderers/${renderer}/${scene_name}.jpg"
        else
            frames_option="--frames $frames"
            output_path="renderers/${renderer}/${scene_name}.#.jpg"
        fi

	# Ensure the output directory exists
	output_dir=$(dirname "$output_path")
	mkdir -p "$output_dir"

        # Create a log file for this run
        log_file="logs/${renderer}_${scene_name}.log"
	mkdir -p logs  # Ensure the logs directory exists
        
        # Run the command and log the output
        echo "Running: rez env $package -- usdrecord --camera $camera --renderer \"$renderer\" --purposes render  $frames_option $scene \"$output_path\"" | tee "$log_file"
        (/usr/bin/time -f "Time: %E\nMemory: %M KB" rez env $package -- usdrecord --camera $camera --renderer "$renderer" --purposes render $frames_option $scene "$output_path" || echo "ERROR: usdrecord returned non-zero exit status") |& tee -a "$log_file"
    done
done

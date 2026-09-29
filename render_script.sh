#!/bin/bash

declare -A renderers
renderers=(
    ["Storm"]="aswf"
    ["Moonray"]="aswf"
    ["Cycles"]="aswf"
)

scenes_and_cameras=(
    "assets/full_assets/McUsd/McUsd.usda /McUsd/Camera"
    "assets/full_assets/OpenChessSet/chess_set.usda main_cam"
    "scenes/MoanaIsland/usd/island.usda /island/cam/shotCam"
    "scenes/ALab/ALab/entry.usda /root/camera01/GEO/renderCam_hrc/renderCam_buffer/renderCam_srt/renderCam"
)

declare -A problematic_combinations
problematic_combinations=(
    ["Storm,scenes/MoanaIsland/usd/island.usda"]='Segmentation fault (core dumped)'
    ["Moonray,scenes/MoanaIsland/usd/island.usda"]='Error: Arras session stopped, compExited: mcrt exited due to signal 9'
    ["Cycles,scenes/MoanaIsland/usd/island.usda"]='Killed'
    ["Cycles,scenes/ALab/ALab/entry.usda"]='Segmentation fault (core dumped)'
)

for renderer in "${!renderers[@]}"; do
    package=${renderers[$renderer]}

    for scene_and_camera in "${scenes_and_cameras[@]}"; do
        scene=$(echo $scene_and_camera | awk '{print $1}')
        camera=$(echo $scene_and_camera | awk '{print $2}')
        frames=$(echo $scene_and_camera | awk '{print $3}')

        combination="${renderer},${scene}"
        if [[ -n "${problematic_combinations[$combination]}" ]]; then
            echo "Skipping problematic combination: $combination"
            continue
        fi

        scene_name=$(basename "$scene" | sed 's/\.[^.]*$//')

        if [ -z "$frames" ]; then
            frames_option=""
            output_path="renderers/${renderer}/${scene_name}.jpg"
        else
            frames_option="--frames $frames"
            output_path="renderers/${renderer}/${scene_name}.#.jpg"
        fi

	output_dir=$(dirname "$output_path")
	mkdir -p "$output_dir"

        log_file="logs/${renderer}_${scene_name}.log"
	mkdir -p logs

        echo "Running: rez env $package -- usdrecord --camera $camera --renderer \"$renderer\" --purposes render  $frames_option $scene \"$output_path\"" | tee "$log_file"
        (/usr/bin/time -f "Time: %E\nMemory: %M KB" rez env $package -- usdrecord --camera $camera --renderer "$renderer" --purposes render $frames_option $scene "$output_path" || echo "ERROR: usdrecord returned non-zero exit status") |& tee -a "$log_file"
    done
done
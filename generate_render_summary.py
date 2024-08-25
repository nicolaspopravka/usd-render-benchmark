import os
import re
import argparse

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Generate a markdown summary.')
parser.add_argument('--system-specs', type=str, required=True, help='System specifications to include in the markdown table')
args = parser.parse_args()

# Directory containing the log files
log_dir = 'logs'

# System specifications
system_specs = args.system_specs

# Initialize a dictionary to hold results
results = {}
renderers = set()
scenes = set()

# Read all log files in the specified directory
for filename in os.listdir(log_dir):
    if filename.endswith('.log'):
        # Parse renderer and scene from filename
        renderer, scene = filename[:-4].split('_', 1)
        renderers.add(renderer)
        scenes.add(scene)

        # Initialize a dictionary for the specific renderer-scene combination
        if scene not in results:
            results[scene] = {}
        
        # Read log file
        with open(os.path.join(log_dir, filename), 'r') as file:
            log_content = file.read()

            # Check if the render succeeded
            if "ERROR: usdrecord returned non-zero exit status" in log_content:
                status = "Failure"
            else:
                status = "Success"

            # Extract time and memory using regex
            time_match = re.search(r'Time:\s*(\S+)', log_content)
            memory_match = re.search(r'Memory:\s*(\S+)', log_content)

            time = time_match.group(1) if time_match else "N/A"
            memory = memory_match.group(1) + "KB" if memory_match else "N/A"

            # Store the result
            results[scene][renderer] = (status, time, memory)

# Prepare markdown table header
header = '| Scene \\ Renderer | ' + ' | '.join(sorted(renderers)) + ' |'
separator = '|' + '---|' * (len(renderers) + 1)

# Prepare the table rows
rows = []
for scene in sorted(scenes):
    row = f"| {scene} | "
    row += ' | '.join(
        f"{results[scene].get(renderer, ('N/A', 'N/A', 'N/A'))[0]}<br>{results[scene].get(renderer, ('N/A', 'N/A', 'N/A'))[1]}<br>{results[scene].get(renderer, ('N/A', 'N/A', 'N/A'))[2]}"
        for renderer in sorted(renderers)
    )
    row += ' |'
    rows.append(row)

# Generate complete markdown content
markdown_content = f"# USD Render Benchmark\n\n"
markdown_content += header + '\n' + separator + '\n' + '\n'.join(rows)
markdown_content += f"\n## System Specs\n{system_specs}\n"

# Save the markdown content to a file
output_file = 'render_summary.md'
with open(output_file, 'w') as f:
    f.write(markdown_content)

print(f"Markdown table generated and saved to {output_file}.")

#!/bin/zsh
# /Volumes/BIGWD8/Datalake/chess/lichess_downloads

# Check if both arguments (source folder and destination folder) are provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <source-folder> <destination-folder>"
  exit 1
fi

# Assign parameters to variables
source_folder="$1"
destination_folder="$2"

# Ensure the destination folder exists, if not, create it
if [ ! -d "$destination_folder" ]; then
  mkdir -p "$destination_folder"
fi

# Loop through all .pgn files in the source folder
for file in "$source_folder"/*.pgn; do
  filename=$(basename "$file")
  # Extract the ECO-Code (first three characters of the filename)
  eco_code="${filename:0:3}"

  # Append the contents of the current file to the new file in the destination folder
  cat "$file" >> "${destination_folder}/${eco_code}.pgn"
done

echo "All files have been concatenated based on their ECO-Code."

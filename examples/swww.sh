#!/bin/bash



# -- variables--

# Directory containing the images
# also counts all subdirectories
directory="/path/to/images/"
# where the scripts from github are
scripts="/path/to/git/repo/"
# where songs from currently playing items are stored
current_dir="/path/to/save/currently/playing/images/"
# time before background is changed
sleep_time_default=60

# --Code--

# For Logging

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sleep_time="$sleep_time_default"

exec > "$SCRIPT_DIR/swww.sh.log"
exec 2>&1

pwd

cd "$(dirname "$0")"

all_files=$(find "$directory" -type f -print)

# Store the file paths in an array
IFS=$'\n' read -rd '' -a files <<<"$all_files"

get_file() {

    current_img=$(python "$scripts/spotify_api/current.py" "$current_dir" | awk 'NR==2')

    if [ -n "$current_img" ]; then
        echo "$current_img"
        return 10
    else
        # Generate a random index within the range of available file paths
        index=$((RANDOM % ${#files[@]}))
        # Return the randomly selected file path
        echo "${files[$index]}"
        return "$sleep_time_default"
    fi
}

# Function to get the average color of the img
get_hex() {

    img="$1" # path to img
    out=$(python "$scripts"/imageaverage/main.py "$img" -m 0.5 --hex)

    echo "$out"
}

# Function to set the background
set_background() {
    bg="$1" # argument 1 is the img path
    hex="$2" # argument 2 is the fill color as a hex value

    # Set the background using swww
    swww img "$bg" --no-resize --fill-color "$hex" -t grow --transition-pos 'top-right' --transition-duration 5
}

bash ./swww-prep.sh & disown

swww-daemon & disown

source "$scripts"/.venv/bin/activate

# cd /home/david/Scripts/WallTune-Usage/imageaverage/

while true; do
    # Get the next image
    image=$(get_file)
    sleep_time=$?
    echo "Changing to $image"

    hex=$(get_hex "$image")

    set_background "$image" "$hex"

    echo "Waiting for $sleep_time"
    sleep "$sleep_time"
done


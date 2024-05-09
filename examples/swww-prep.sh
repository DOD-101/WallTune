#!/bin/bash


# where files from the API are stored
directory="/path/to/API/storage"
# location of the files after adjustbrightness  
save_dir="/path/to/adjustbrightness/storage"
# where the scripts from github are
scripts="/path/to/git/repo"
# .env file for saving last API call time
env_file="/path/to/something.env"
# the options.json for the grouping
grouping_options="path/to/options.json"

# --code--
source "$scripts/.venv/bin/activate"

source "$env_file"

# Function to update a specific environment variable in the .env file
function update_env_var {
    local var_name="$1"
    local new_value="$2"

    # Check if the variable exists in the .env file
    if grep -q "^$var_name=" "$env_file"; then
        # Update the variable value in the .env file
        sed -i "s/^$var_name=.*/$var_name=$new_value/" "$env_file"
    else
        # Append the variable to the .env file if it doesn't exist
        echo "$var_name=$new_value" >> "$env_file"
    fi

    # Reload the environment variables
    source "$env_file"
}

function write_time_to_cache {
    time_var=$(date +%s)
    update_env_var "LAST_API_CALL" "$time_var"
}

function make_call {
    current_time=$(date +%s)
    time_seconds=$((24 * 60 *  60)) # one day (h:m:s)

    if (( current_time - LAST_API_CALL >= time_seconds )); then
        echo "Getting Tracks"
        python ""$scripts"/spotify_api/main.py" "$directory" -a 10
        echo "Adjusting brightness"
        python "$scripts/adjustbrightness/main.py" "$directory" "$save_dir" -m 0.6 -c 150 -r --move
        echo "Grouping Images"
        python "$scripts/grouping/main.py" "$save_dir" "$grouping_options" -r --move
        write_time_to_cache
    fi
}

make_call









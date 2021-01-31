#!/bin/bash

# Check if argument is a file
if [[ ! -f "$1" ]]; then
    echo "$1 does not exist!"
    exit 1
fi

cp $1 current.md

# Replaces '_' with ' '. Filenames often use _ while ordning.txt uses the song name
song_name="${1//_/' '}"

# Remove the fileending like .txt (again ordning.txt uses the song name not file name)
name=$(echo "${song_name}" | awk -F "." '{print $1}')

# Do the replacement inplace.
sed -i "s/${name}/${name} */i" ordning.txt

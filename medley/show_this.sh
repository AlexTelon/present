#!/bin/bash

# Check if argument is a file
if [[ ! -f "$1" ]]; then
    echo "$1 does not exist!"
    exit 1
fi

cp $1 current.txt

# replaces '_' with ' '. Filenames often use _ while ordning.txt will not
file_name="${1//_/' '}"

# Remove the fileending like .txt
name=$(echo "${file_name}" | awk -F "." '{print $1}')

#sed "s/${name}/${name} */i" ordning.txt > ordning.txt
sed -i "s/${name}/${name} */i" ordning.txt

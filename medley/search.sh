#!/bin/bash
all_args="${@:1}"

# Allow for some special chars between words when you are searching
pattern=""
for arg in $all_args; do
    pattern="${pattern} ${arg}[,.!?]?"
done

# -i to be case insensitive
egrep --color=auto  -i --exclude="current.txt" --exclude="ordning.txt" "${pattern}" *
#!/bin/bash

# Initialize variables
current_word=""
current_count=0

# Read input from STDIN, sorted by word
while IFS=$'\t' read -r word count; do
    # If we have the same word as the previous one, accumulate the count
    if [ "$current_word" == "$word" ]; then
        ((current_count += count))
    else
        # If it's a new word, print the previous word and count (if applicable)
        if [ -n "$current_word" ]; then
            echo -e "$current_word\t$current_count"
        fi
        # Reset for the new word
        current_word="$word"
        current_count="$count"
    fi
done

# Print the last word if needed
if [ -n "$current_word" ]; then
    echo -e "$current_word\t$current_count"
fi

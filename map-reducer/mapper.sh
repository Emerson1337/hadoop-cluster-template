#!/bin/bash

# Read each line from standard input (STDIN)
while IFS= read -r line
do
  # Convert the line to lowercase (optional, can be removed if not needed)
  line=$(echo "$line" | tr '[:upper:]' '[:lower:]')
  
  # Split the line into words using 'tr' to replace spaces with newlines and process each word
  for word in $line; do
    # Output the word and a count of 1, separated by a tab
    echo -e "$word\t1"
  done
done
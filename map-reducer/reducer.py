#!/usr/bin/env python3

import sys

current_word = None
current_count = 0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    try:
        word, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        # if count is not a number, skip this line
        continue

    # this IF-switch works because Hadoop sorts map output
    # by key (word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # write result to STDOUT
            print(f'{current_word}\t{current_count}')
        current_count = count
        current_word = word

# do not forget to output the last word if needed!
if current_word:
    print(f'{current_word}\t{current_count}')
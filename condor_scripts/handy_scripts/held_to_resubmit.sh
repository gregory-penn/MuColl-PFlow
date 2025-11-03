#!/bin/bash
# Extract held subjob numbers from condor_q output and save to joblist.txt
# can be run anywhere. 

batchName="$1"
output_file="joblist.txt"

if [[ -z "$batchName" ]]; then
    echo "Usage: $0 <batchName>"
    exit 1
fi

# Run condor_q and filter held jobs
condor_q "$batchName" --hold 2>/dev/null | \
awk -F'[ .]' '/^[0-9]+\.[0-9]+/ {printf "%03d\n", $2}' > "$output_file"

echo "Wrote held job numbers to $output_file:"
cat "$output_file"

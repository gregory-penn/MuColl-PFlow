#!/bin/bash
# Check which expected files from joblist.txt are missing in the current directory.

input_prefix="output_sim_tau_gen_split"
joblist="joblist.txt"

if [[ ! -f "$joblist" ]]; then
    echo "Error: $joblist not found."
    exit 1
fi

missing=()

while read -r jobnum; do
    [[ -z "$jobnum" ]] && continue  # skip blank lines
    file="${input_prefix}.${jobnum}.slcio"
    if [[ ! -f "$file" ]]; then
        missing+=("$jobnum")
    fi
done < "$joblist"

if (( ${#missing[@]} == 0 )); then
    echo "All files are present."
else
    printf "%s\n" "${missing[@]}"
fi

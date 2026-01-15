#!/bin/bash
# Resubmit only Condor jobs held due to "Transfer input files failure"

batch_no="$1"
if [[ -z "$batch_no" ]]; then
    echo "Usage: $0 <batch_no>"
    exit 1
fi

echo "Checking held jobs for batch $batch_no ..."
fail_list="resubmit_list.txt"
> "$fail_list"

# Extract job numbers with transfer input failure
condor_q "$batch_no" --hold 2>/dev/null | \
grep -F "Transfer input files failure" | \
awk -F'[ .]' '{print $2}' > "$fail_list"

count=$(wc -l < "$fail_list")
if (( count == 0 )); then
    echo "No jobs with input transfer failure found."
    exit 0
fi

echo "Found $count jobs with input transfer failure:"
cat "$fail_list"

read -p "Release these jobs? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Resubmit each listed job
while read -r job; do
    echo "Releasing job ${batch_no}.${job} ..."
    condor_release "${batch_no}.${job}"
done < "$fail_list"

echo "Done. Released $count job(s)."

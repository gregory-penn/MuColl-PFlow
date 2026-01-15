#!/bin/bash
# Split listed .slcio files into 3 smaller files using lcio_split_file
# Outputs go to split/ directory.

input_prefix="output_sim_neutronGun_E_50_250_split"
output_dir="split"
joblist="joblist.txt"

# Make sure joblist exists
if [[ ! -f "$joblist" ]]; then
    echo "Error: $joblist not found."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

echo "Preparing to split files listed in $joblist..."
sleep 0.5

# Preview planned operations
while read -r jobnum; do
    infile="${input_prefix}.${jobnum}.slcio"
    if [[ -f "$infile" ]]; then
        filesize=$(stat -c%s "$infile")
        echo "$infile -> ${output_dir}/${input_prefix}.${jobnum}.slcio  (size: $filesize bytes)"
    else
        echo "Warning: missing input file $infile"
    fi
done < "$joblist"

echo
read -p "Proceed with splitting? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Actual splitting
while read -r jobnum; do
    infile="${input_prefix}.${jobnum}.slcio"
    outfile="${output_dir}/${input_prefix}_split.${jobnum}.slcio"

    if [[ -f "$infile" ]]; then
        filesize=$(stat -c%s "$infile")
        filesize_final=$((filesize / 1000)) # this gross overkill gaurantees one event per file.
        echo "Splitting $infile (size: $filesize bytes)..."
        lcio_split_file "$infile" "$outfile" "$filesize_final"
    else
        echo "Skipping missing file: $infile"
    fi
done < "$joblist"

echo "All done. Split files are in: $output_dir/"

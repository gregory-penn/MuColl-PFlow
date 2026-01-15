#!/bin/bash
# Renames split output files into a flat sequence: output.ZZ.slcio
# from files like output.XX.YY.slcio 

output_dir="./"
base_name="output_sim_neutronGun_E_50_250_split_split"

if [[ ! -d "$output_dir" ]]; then
    echo "Error: directory '$output_dir' not found."
    exit 1
fi

cd "$output_dir" || exit 1

# Get all matching files sorted naturally
files=($(ls ${base_name}.*.*.slcio 2>/dev/null | sort -V))

if [[ ${#files[@]} -eq 0 ]]; then
    echo "No files matching ${base_name}.*.*.slcio found in $output_dir/"
    exit 0
fi

echo "Renaming ${#files[@]} files..."

# Rename sequentially: output.00.slcio, output.01.slcio, etc.
counter=0
for f in "${files[@]}"; do
    newname=$(printf "%s.%03d.slcio" "$base_name" "$counter")
    mv -v "$f" "$newname"
    ((counter++))
done

echo "Done. Files renamed to sequential numbering from 000 to $(printf '%03d' $((counter-1)))."

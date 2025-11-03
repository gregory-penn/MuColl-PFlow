#!/bin/bash
# Sum LCIO event counts and optionally delete bad files

total=0
bad_files=()

for f in *.slcio; do
    if [[ -f "$f" ]]; then
        count=$(lcio_event_counter "$f" 2>/dev/null)
        if [[ "$count" =~ ^[0-9]+$ ]]; then
            total=$((total + count))
        else
            echo "Warning: $f produced non-integer output: '$count'"
            bad_files+=("$f")
        fi
    fi
done

echo "------------------------------------"
echo "Total events: $total"
echo "------------------------------------"

if (( ${#bad_files[@]} > 0 )); then
    echo "The following files produced invalid output:"
    printf '  %s\n' "${bad_files[@]}"
    read -p "Delete these files? (y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        rm -v "${bad_files[@]}"
        echo "Deleted ${#bad_files[@]} bad file(s)."
    else
        echo "Skipped deletion."
    fi
else
    echo "No bad files found."
fi

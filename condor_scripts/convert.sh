#!/bin/bash

SCRIPT="/scratch/gregorypenn/lccontent/maia_Geometry/MAIA_versions/v1_jun27/detector-simulation/utils/fluka_to_slcio_new.py"
DATADIR="/ospool/uc-shared/project/futurecolliders/data/fmeloni/FLUKA"

for i in $(seq 1 6667); do
    filename="summary${i}_DET_IP.dat"
    filepath="${DATADIR}/${filename}"
    outputname="BIBinput${i}.slcio"
    if [[ -f "$filepath" ]]; then
        python "$SCRIPT" "$filepath" "$outputname" -n 42.64
    else
        echo "Missing file: $filepath" >&2
    fi
done
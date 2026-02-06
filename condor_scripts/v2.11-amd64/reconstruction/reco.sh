#!/bin/bash
echo $HOSTNAME
echo "<<<Singularity ENVIRONMENT:" $SINGULARITY_NAME
echo "Local directory looks like: "
ls -lthr $PWD
echo "Setting up BIB utils"
source /opt/setup_mucoll.sh
echo "Setting up BIB utils"
rm -rf MyBIBUtils/build && mkdir MyBIBUtils/build && cd MyBIBUtils/build
cmake ..
make
export MARLIN_DLL=`readlink -e lib/libMyBIBUtils.so`:${MARLIN_DLL}
cd ../..
echo "check current directory"
ls -lthr $PWD
echo "<<<Check if we can find executables"
which ddsim
which Marlin
echo "<<<Check if input files were copied from the origin"
ls -lthr 
echo "Checking if PUBLIC is set"
echo $PUBLIC
echo "Checking if SHARED is set"
echo $SHARED
echo "Checking that BIB files are found"
ls -lthr /cvmfs/public-uc.osgstorage.org/ospool/uc-shared/public/futurecolliders/gregorypenn/BIB_v7_2026

#Initialize variables
input_file=""
chunks=""
n_events=""

pathToBIBTemp="/cvmfs/public-uc.osgstorage.org/ospool/uc-shared/public/futurecolliders/gregorypenn/BIB_v7_2026/"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --inputFile)
            input_file="$2"
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

input_file_string=

# Corrected command assignment
command="k4run digi_reco_condor.py --InFileName ${input_file} --ThresholdsPath MyBIBUtils/data/ --enableBIB --PathtoMuPlus ${pathToBIBTemp}/sim_mp_pruned --PathtoMuMinus ${pathToBIBTemp}/sim_mm_pruned --OutFileName reco_${input_file}"

# Print the constructed command
echo "Executing command: $command"

# Run the command
eval $command

# Print the directory after running the job. This is to check the file size before transferring. 
echo "Here is the directory after executing the job"
ls -lthr $PWD

#!/bin/bash
echo $HOSTNAME
echo "<<<Singularity ENVIRONMENT:" $SINGULARITY_NAME
echo "<<<Setup some environment"
echo "Setting up mucoll  --> "
source /opt/spack/opt/spack/linux-almalinux9-x86_64/gcc-11.5.0/mucoll-stack-master-h2ssl2yh2yduqnhsv2i2zcjws74v7mcq/setup.sh
echo ">>>completed"
echo "Local directory looks like: "
ls -lthr $PWD
echo "Geometry directory looks like: "
ls -lthr MAIA_v0/
echo "<<<<Exporting MAIA geometry"
export MAIA_GEO=$PWD/MAIA_v0/MAIA_v0.xml
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
echo $MAIA_GEO
echo "<<<Check if input files were copied from the origin"
ls -lthr 
echo "Checking if PUBLIC is set"
echo $PUBLIC
echo "Checking if SHARED is set"
echo $SHARED
echo "Checking that BIB sim files can be located"
ls -lthr /ospool/uc-shared/public/futurecolliders/v5/simBIB/mm_pruned
echo "Checking alternate path"
ls -lthr /cvmfs/public-uc.osgstorage.org/ospool/uc-shared/public/futurecolliders/v5/simBIB/

#Initialize variables
input_file=""
chunks=""
n_events=""

pathToBIBTemp="/cvmfs/public-uc.osgstorage.org/ospool/uc-shared/public/futurecolliders/v5/simBIB/mm_pruned"

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
command="k4run steer_digi_reco_BIB.py --InFileName split_gen_pions.${input_file}.slcio --ThresholdsPath MyBIBUtils/data/ --enableBIB --PathtoMuPlus ${pathToBIBTemp} --PathtoMuMinus ${pathToBIBTemp}"
# Print or execute the constructed command
echo "Command: $command"
# Print the constructed command
echo "Executing command: $command"

# Run the command
eval $command
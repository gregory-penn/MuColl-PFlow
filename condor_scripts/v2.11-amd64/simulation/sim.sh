#!/bin/bash
echo $HOSTNAME
echo "<<<Singularity ENVIRONMENT:" $SINGULARITY_NAME
echo "<<<Setup some environment"
echo "Setting up mucoll  --> "
source /opt/setup_mucoll.sh
# Source this setup below instead for the updated software
#source /opt/spack/opt/spack/linux-ubuntu24.04-x86_64/gcc-13.3.0/mucoll-stack-master-lvpbiuwr2cvt6zi6aotsoyf2oc47azct/setup.sh
echo ">>>completed"
echo "Local directory looks like: "
ls -lthr $PWD
echo "Checking that I can find the MAIA geometry: "
ls -lthr /opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/k4geo-00-23-dklehcszm7rspyzkfvnmnee4ergookmv/share/k4geo/MuColl/MAIA/compact/MAIA_v0//
echo "<<<<Exporting MAIA geometry"
export MAIA_GEO=/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/k4geo-00-23-dklehcszm7rspyzkfvnmnee4ergookmv/share/k4geo/MuColl/MAIA/compact/MAIA_v0/MAIA_v0.xml
echo "<<<Check if we can find executables"
which ddsim
which Marlin
echo $MAIA_GEO
echo "<<<Check if input files were copied from the origin"
ls -lthr 

# Initialize variables
input_file=""
chunks=""
n_events=""

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

command="ddsim --steeringFile steer_sim_MAIA_condor.py --inputFile ${input_file} --outputFile output_sim_${input_file} --numberOfEvents 1"

# Print the constructed command
echo "Executing command: $command"

# Run the command
eval $command
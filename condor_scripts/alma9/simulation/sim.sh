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
echo "Geometry directory looks like: "
ls -lthr MAIA_v0/
echo "<<<<Exporting MAIA geometry"
export export MAIA_GEO=$PWD/MAIA_v0/MAIA_v0.xml
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

command="ddsim --steeringFile steer_sim_tau_gun_MAIA.py --inputFile ${input_file} --outputFile output_sim_${input_file}.slcio --numberOfEvents 1"

# Print the constructed command
echo "Executing command: $command"

# Run the command
eval $command
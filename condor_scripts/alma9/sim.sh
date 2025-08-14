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
echo "<<<Check if we can find executables"
which ddsim
which Marlin
echo $MAIA_GEO
echo "<<<Check if input files were copied from the origin"
ls -lthr

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

# Corrected command assignment
command="ddsim --steeringFile steer_sim_tau_gun_MAIA.py --inputFile BIBinput${input_file}.slcio --outputFile BIBsim${input_file}.slcio --numberOfEvents 1"
# Print or execute the constructed command
echo "Command: $command"
# Print the constructed command
echo "Executing command: $command"

# Run the command
eval $command

# echo "<<<copy that local file back to the origin"
# echo "set stashcp client for non-OSG images"
# Copy finished sim file
# cat  /etc/*-release  | grep VERSION_ID
# export STASHCP=/cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/23/current/el8-x86_64/usr/bin/stashcp
# $STASHCP -d ${input_file}_sim${proc_id}.slcio osdf:///ospool/uc-shared/project/futurecolliders/larsonma/2500evSim/${input_file}_sim${proc_id}.slcio
# echo ">>> transfer completed"



#echo "<<<Delete input files so they don't get transferred twice on exit"
#rm -rf steer_baseline.py
#rm -rf $input_file.hepmc
#rm -rf $input_file.tbl
#rm -rf ${input_file}_sim${proc_id}.slcio
#echo ">>> Deletions complete. Test job complete"
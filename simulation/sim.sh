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
# below was for debugging the failed hosts. Unsuccessful.
# echo "Checking if DDG4 is present"
# ls -lthr /opt/spack/opt/spack/linux-almalinux9-x86_64/gcc-11.5.0/dd4hep-master-fzr6nyeeos2hpkhcx4w3gsptbvlsbhkt/lib
# echo "Printing LD Library Path" 
# echo $LD_LIBRARY_PATH
# echo "Checking dependencies of DDG4"
# ldd /opt/spack/opt/spack/linux-almalinux9-x86_64/gcc-11.5.0/dd4hep-master-fzr6nyeeos2hpkhcx4w3gsptbvlsbhkt/lib/libDDG4Plugins.so.1.32
# echo "Found that the problem is with libQt6Core, checking that the link is valid"
# ls /opt/spack/opt/spack/linux-almalinux9-x86_64/gcc-11.5.0/qt-base-6.8.1-wgi77vuqvm66nbaej3sq6d6fjlewpn7n/lib
# echo "Test 1"
# ls -l /opt/spack/opt/spack/linux-almalinux9-x86_64/gcc-11.5.0/qt-base-6.8.1-wgi77vuqvm66nbaej3sq6d6fjlewpn7n/lib/libQt6Core.so.6
# echo "Test 2"
# file /opt/spack/opt/spack/linux-almalinux9-x86_64/gcc-11.5.0/qt-base-6.8.1-wgi77vuqvm66nbaej3sq6d6fjlewpn7n/lib/libQt6Core.so.6
# echo "Test 3"
# ldd /opt/spack/opt/spack/linux-almalinux9-x86_64/gcc-11.5.0/qt-base-6.8.1-wgi77vuqvm66nbaej3sq6d6fjlewpn7n/lib/libQt6Core.so.6
# echo "Hail mary to update the path, in case that just works..."
# export LD_LIBRARY_PATH=/opt/spack/opt/spack/linux-almalinux9-x86_64/gcc-11.5.0/qt-base-6.8.1-wgi77vuqvm66nbaej3sq6d6fjlewpn7n/lib:$LD_LIBRARY_PATH

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

input_file_string=

# Corrected command assignment
command="ddsim --steeringFile steer_sim_tau_gun_MAIA.py --inputFile split_gen_pions.${input_file}.slcio --outputFile split_sim_pions.${input_file}.slcio --numberOfEvents 50"

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
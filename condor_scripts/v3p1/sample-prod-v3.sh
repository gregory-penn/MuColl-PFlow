#!/bin/bash
echo $HOSTNAME
echo "<<<Singularity ENVIRONMENT:" $SINGULARITY_NAME
tarname="$1"
echo "<<<unpacking tar file: ${tarname}"
tar xzf ${tarname}.tar.gz
echo "Local directory looks like: "
ls -lthr $PWD
# by-hand stack loading 
source /opt/setup_mucoll.sh
echo "Setting up MAIA  --> "
source setup_config.sh . MAIA_v0
echo "<<<Check that we can find MAIA geometry"
env | grep MUCOLL
bib_path="/cvmfs/public-uc.osgstorage.org/ospool/uc-shared/public/futurecolliders/gregorypenn/BIB_v9/"
echo "<<<Check that we can find BIB files"
ls -lthr ${bib_path}

echo "<<< Printing the Pandora settings used for this job"
cat configs/MAIAConfig/MAIAConfig/PandoraSettings/PandoraSettingsDefault.xml

# Set up random seed
randomseed="$2"
echo "Using random seed: ${randomseed}"
pdgID="$3"
echo "Generating particle guns of particles with pdgID: ${pdgID}"
name="$4"
echo "Your files will be saved with the string: ${name}"
ptMin="$5"
ptMax="$6"
thetaMin="$7"
thetaMax="$8"
echo "Generating particles with pT from ${ptMin} GeV to ${ptMax} GeV"
nevents="$9"
nOverlay="$11"
# Set up directory for output file copy
mkdir output/

gen_command="python generation/pgun/pgun_edm4hep.py -p 1 -e ${nevents} --pdg ${pdgID} --pt ${ptMin} ${ptMax} --theta ${thetaMin} ${thetaMax} -s ${randomseed} -- output/gen.${name}.${randomseed}.root"
sim_command="ddsim --steeringFile simulation/steer_baseline.py --inputFiles output/gen.${name}.${randomseed}.root --outputFile output/sim.${name}.${randomseed}.root --numberOfEvents ${nevents}"
# run with BIB or not
if [[ "$10" == "true" ]]; then
    echo "Running with full BIB (${nOverlay} files). Tracker coning is also on."
    reco_command="k4run $MUCOLL_CONFIG/$MUCOLL_CONFIG_NAME/digi_reco_steer.py --inputFiles output/sim.${name}.${randomseed}.root --outputFile output/reco.${name}.${randomseed}.edm4hep.root --histoFile output/reco_histo.${name}.${randomseed}.root --doOverlayFull --OverlayFullNumberBackground ${nOverlay} --OverlayFullPathToMuPlus ${bib_path}/sim_mp/ --OverlayFullPathToMuMinus ${bib_path}/sim_mm/ --doTrackerConing"
else
    echo "Running without BIB."
    reco_command="k4run $MUCOLL_CONFIG/$MUCOLL_CONFIG_NAME/digi_reco_steer.py --inputFiles output/sim.${name}.${randomseed}.root --outputFile output/reco.${name}.${randomseed}.edm4hep.root --histoFile output/reco_histo.${name}.${randomseed}.root"
fi
# Print and run
echo "Executing command: $gen_command"
eval $gen_command
echo "Executing command: $sim_command"
eval $sim_command
echo "Executing command: $reco_command"
eval $reco_command
echo "Done. Copying files back".
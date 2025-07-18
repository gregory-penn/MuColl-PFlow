import os
from Gaudi.Configuration import *

from Configurables import LcioEvent, EventDataSvc, MarlinProcessorWrapper
from k4FWCore.parseArgs import parser

parser.add_argument(
    "--DD4hepXMLFile",
    help="Compact detector description file",
    type=str,
    default=os.environ.get("MAIA_GEO", ""),
)

parser.add_argument(
    "--MatFile",
    help="Material maps file for tracking",
    type=str,
    default="/path/to/material-maps.json",
)

parser.add_argument(
    "--TGeoFile",
    help="TGeometry file for tracking",
    type=str,
    default="/path/to/tgeo.root",
)

the_args = parser.parse_known_args()[0]

algList = []
evtsvc = EventDataSvc()


read = LcioEvent()
read.OutputLevel = INFO
read.Files = ["input.slcio"]
algList.append(read)

DD4hep = MarlinProcessorWrapper("DD4hep")
DD4hep.OutputLevel = INFO
DD4hep.ProcessorType = "InitializeDD4hep"
DD4hep.Parameters = {
                     "DD4hepXMLFile": [the_args.DD4hepXMLFile],
                     "EncodingStringParameterName": ["GlobalTrackerReadoutID"]
                     }

# Config = MarlinProcessorWrapper("Config")
# Config.OutputLevel = INFO
# Config.ProcessorType = "CLICRecoConfig"
# Config.Parameters = {
#                      "VertexUnconstrained": ["OFF"],
#                      "VertexUnconstrainedChoices": ["ON", "OFF"]
#                      }

AIDA = MarlinProcessorWrapper("AIDA")
AIDA.OutputLevel = INFO
AIDA.ProcessorType = "AIDAProcessor"
AIDA.Parameters = {
                   "FileName": ["output_reco"],
                   "FileType": ["root"]
                   }

EventNumber = MarlinProcessorWrapper("EventNumber")
EventNumber.OutputLevel = INFO
EventNumber.ProcessorType = "Statusmonitor"
EventNumber.Parameters = {
                          "HowOften": ["1"] 
                          }

#https://github.com/iLCSoft/Marlin/blob/6f8703a389987082363206e41e5ff1054ed1f444/source/src/LCIOOutputProcessor.cc
LCIOWriter_all = MarlinProcessorWrapper("LCIOWriter_all")
LCIOWriter_all.OutputLevel = VERBOSE
LCIOWriter_all.ProcessorType = "LCIOOutputProcessor"
LCIOWriter_all.Parameters = {
                             "DropCollectionNames": [],
                             "DropCollectionTypes": [],
                             "FullSubsetCollections": [],
                             "KeepCollectionNames": ["SiTracks_Refitted", "SiTracks_Refitted_Relations", "MCParticle_SiTracks_Refitted", "RecoMCTruthLink"],
                             "LCIOOutputFile": ["output_reco.slcio"],
                             "LCIOWriteMode": ["WRITE_NEW"]
                             }

#https://github.com/MuonColliderSoft/ACTSTracking/blob/ce74f55a0ec320284ce8cc2d2d233a7f9c8b912d/src/ACTSSeededCKFTrackingProc.cxx#L45
# Adapted from Fede's config
CKFTracking = MarlinProcessorWrapper("CKFTracking")
CKFTracking.OutputLevel = INFO
CKFTracking.ProcessorType = "ACTSSeededCKFTrackingProc"
CKFTracking.Parameters = {
    "CKF_Chi2CutOff": ["10"],
    "CKF_NumMeasurementsCutOff": ["1"],
    "MatFile": [the_args.MatFile],
    "PropagateBackward": ["False"],
    "RunCKF": ["True"],
    "DetectorSchema": ["MAIA_v0"],
    "SeedFinding_CollisionRegion": ["6"],
    # "SeedFinding_DeltaRMax": ["60"],
    # "SeedFinding_DeltaRMin": ["2"],
    # "SeedFinding_DeltaRMaxBottom": ["50"],
    # "SeedFinding_DeltaRMaxTop": ["50"],
    # "SeedFinding_DeltaRMinBottom": ["5"],
    # "SeedFinding_DeltaRMinTop": ["2"],
    "SeedFinding_ImpactMax": ["3"],
    "SeedFinding_MinPt": ["500"],
    "SeedFinding_RMax": ["150"],
    "SeedFinding_ZMax": ["600"],
    "SeedFinding_RadLengthPerSeed": ["0.1"],
    # "SeedFinding_zBottomBinLen": ["1"],
    # "SeedFinding_zTopBinLen": ["1"],
    # "SeedFinding_phiBottomBinLen": ["1"],
    # "SeedFinding_phiTopBinLen": ["1"],
    "SeedFinding_SigmaScattering": ["50"],
    "SeedingLayers": ["13", "2", "13", "6", "13", "10", "13", "14",
                      "14", "2", "14", "6", "14", "8", "14", "10", 
                      "15", "2", "15", "6", "15", "10", "15", "14",
                      "8", "2",
                      "17", "2",
                      "18", "2"],
    "TGeoFile": [the_args.TGeoFile],
    "TGeoDescFile": ["/opt/spack/opt/spack/linux-ubuntu24.04-x86_64/gcc-13.3.0/actstracking-1.3.1-bqlvvdmew24gow2jqheahfpzxnp6xwbt/share/ACTSTracking/data/MAIA_v0.json"],
    "TrackCollectionName": ["AllTracks"],
    "TrackerHitCollectionNames": ["VBTrackerHitsConed", "IBTrackerHitsConed", "OBTrackerHitsConed", "VETrackerHitsConed", "IETrackerHitsConed", "OETrackerHitsConed"],
    "CaloFace_Radius": ["1857"],
    "CaloFace_Z": ["2307"]
}

TrackDeduplication = MarlinProcessorWrapper("TrackDeduplication")
TrackDeduplication.OutputLevel = INFO
TrackDeduplication.ProcessorType = "ACTSDuplicateRemoval"
TrackDeduplication.Parameters = {
                                 "InputTrackCollectionName": ["AllTracks"],
                                 "OutputTrackCollectionName": ["SiTracks"]
                                 }

# adding this to match the marlin workflow
TrackRefit = MarlinProcessorWrapper("TrackRefit")
TrackRefit.OutputLevel = INFO
TrackRefit.ProcessorType = "RefitFinal"
TrackRefit.Parameters = {
                                "EnergyLossOn": ["true"],
                                "DoCutsOnRedChi2Nhits": ["true"],
                                "ReducedChi2Cut": ["3."],
                                #"NHitsCuts": ["1,2", "1", "3,4", "1", "5,6", "0"],
                                "InputRelationCollectionName": ["SiTracksRelations"],
                                "InputTrackCollectionName": ["SiTracks"],
                                "Max_Chi2_Incr": ["1.79769e+30"],
                                "MultipleScatteringOn": ["true"],
                                "OutputRelationCollectionName": ["SiTracks_Refitted_Relations"],
                                "OutputTrackCollectionName": ["SiTracks_Refitted"],
                                "ReferencePoint": ["-1"],
                                "SmoothOn": ["false"],
                                "Verbosity": ["MESSAGE"],
                                "extrapolateForward": ["true"],
                                "MinClustersOnTrackAfterFit:": ["3"]
                                }

#adding track truth matching
# https://github.com/MuonColliderSoft/ACTSTracking/blob/ce74f55a0ec320284ce8cc2d2d233a7f9c8b912d/src/TrackTruthProc.cxx#L20
MyTrackTruth = MarlinProcessorWrapper("MyTrackTruth")
MyTrackTruth.OutputLevel = INFO
MyTrackTruth.ProcessorType = "TrackTruthProc"
MyTrackTruth.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "Particle2TrackRelationName": ["MCParticle_SiTracks_Refitted"],
    "TrackCollection": ["SiTracks_Refitted"],
    "TrackerHit2SimTrackerHitRelationName": ["VBTrackerHitsRelationsConed", "IBTrackerHitsRelationsConed", "OBTrackerHitsRelationsConed", "VETrackerHitsRelationsConed", "IETrackerHitsRelationsConed", "OETrackerHitsRelationsConed"]
}

# https://github.com/MuonColliderSoft/ACTSTracking/blob/ce74f55a0ec320284ce8cc2d2d233a7f9c8b912d/src/TrackTruthProc.cxx#L20
MyTrackTruthSiTracks = MarlinProcessorWrapper("MyTrackTruthSiTracks")
MyTrackTruthSiTracks.OutputLevel = INFO
MyTrackTruthSiTracks.ProcessorType = "TrackTruthProc"
MyTrackTruthSiTracks.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "Particle2TrackRelationName": ["MCParticle_SiTracks"],
    "TrackCollection": ["SiTracks"],
    "TrackerHit2SimTrackerHitRelationName": ["VBTrackerHitsRelationsConed", "IBTrackerHitsRelationsConed", "OBTrackerHitsRelationsConed", "VETrackerHitsRelationsConed", "IETrackerHitsRelationsConed", "OETrackerHitsRelationsConed"]
}

DDMarlinPandora = MarlinProcessorWrapper("DDMarlinPandora")
DDMarlinPandora.OutputLevel = INFO
DDMarlinPandora.ProcessorType = "DDPandoraPFANewProcessor"
DDMarlinPandora.Parameters = {
                              "Verbosity": ["MESSAGE"],
                              "ClusterCollectionName": ["PandoraClusters"],
                              "CreateGaps": ["false"],
                              "CurvatureToMomentumFactor": ["0.00015"], 
                              "D0TrackCut": ["200"], # cut for track CanFormPFO
                              "D0UnmatchedVertexTrackCut": ["5"], # used for CanFormClusterlessPFO
                              "DigitalMuonHits": ["0"],
                              "ECalBarrelNormalVector": ["0", "0", "1"],
                              "ECalCaloHitCollections": ["EcalBarrelCollectionRec", "EcalEndcapCollectionRec", "EcalPlugCollectionRec"], 
                              "ECalMipThreshold": ["0.5"],
                              "ECalScMipThreshold": ["0"],
                              "ECalScToEMGeVCalibration": ["1"],
                              "ECalScToHadGeVCalibrationBarrel": ["1"],
                              "ECalScToHadGeVCalibrationEndCap": ["1"],
                              "ECalScToMipCalibration": ["1"],
                              "ECalSiMipThreshold": ["0"],
                              "ECalSiToEMGeVCalibration": ["1"],
                              "ECalSiToHadGeVCalibrationBarrel": ["1"],
                              "ECalSiToHadGeVCalibrationEndCap": ["1"],
                              "ECalSiToMipCalibration": ["1"],
                              "ECalToEMGeVCalibration": ["1.02373335516"],
                              "ECalToHadGeVCalibrationBarrel": ["1.24223718397"],
                              "ECalToHadGeVCalibrationEndCap": ["1.24223718397"],
                              "ECalToMipCalibration": ["181.818"],
                              "EMConstantTerm": ["0.01"],
                              "EMStochasticTerm": ["0.17"],
                              "FinalEnergyDensityBin": ["110."],
                              "HCalBarrelNormalVector": ["0", "0", "1"],
                              "HCalCaloHitCollections": ["HcalBarrelCollectionRec", "HcalEndcapCollectionRec", "HcalRingCollectionRec"],
                              "HCalMipThreshold": ["0.3"],
                              "HCalToEMGeVCalibration": ["1.02373335516"],
                              "HCalToHadGeVCalibration": ["1.01799349172"],
                              "HCalToMipCalibration": ["40.8163"],
                              "HadConstantTerm": ["0.03"],
                              "HadStochasticTerm": ["0.6"],
                              "InputEnergyCorrectionPoints": [],
                              "KinkVertexCollections": ["KinkVertices"],
                              "LayersFromEdgeMaxRearDistance": ["250"],
                              "MCParticleCollections": ["MCParticle"],
                              "MaxBarrelTrackerInnerRDistance": ["200"], # for track CanFormPFO requirements
                              "MaxClusterEnergyToApplySoftComp": ["2000."],
                              "MaxHCalHitHadronicEnergy": ["1000000"],
                              "MaxTrackHits": ["5000"],
                              "MaxTrackSigmaPOverP": ["0.30"], # track quality cut. Upper bound. Default: 0.15. Better: 0.30. Needs further study.
                              "MinBarrelTrackerHitFractionOfExpected": ["0"],
                              "MinCleanCorrectedHitEnergy": ["0.1"],
                              "MinCleanHitEnergy": ["0.5"],
                              "MinCleanHitEnergyFraction": ["0.01"],
                              "MinFtdHitsForBarrelTrackerHitFraction": ["0"],
                              "MinFtdTrackHits": ["0"],
                              "MinMomentumForTrackHitChecks": ["0"],
                              "MinTpcHitFractionOfExpected": ["0"],
                              "MinTrackECalDistanceFromIp": ["0"], # track quality cut. Lower bound.
                              "MinTrackHits": ["0"],
                              "MuonBarrelBField": ["-1.34"],
                              "MuonCaloHitCollections": ["MuonHits"],
                              "MuonEndCapBField": ["0.01"],
                              "MuonHitEnergy": ["0.5"],
                              "MuonToMipCalibration": ["19607.8"],
                              "NEventsToSkip": ["0"],
                              "NOuterSamplingLayers": ["3"],
                              "OutputEnergyCorrectionPoints": [],
                              "PFOCollectionName": ["PandoraPFOs"],
                              "PandoraSettingsXmlFile": ["PandoraSettings/PandoraSettingsDefault.xml"],
                              "ProngVertexCollections": ["ProngVertices"],
                              "ReachesECalBarrelTrackerOuterDistance": ["-100"], # used to determine whether track reaches ECal. 
                              "ReachesECalBarrelTrackerZMaxDistance": ["-50"], # used to determine whether track reaches ECal
                              "ReachesECalFtdZMaxDistance": ["1"],  # used to determine whether track reaches ECal. Some sort of "wiggle" room when finding which endcap layer a hit is in. 
                              "ReachesECalMinFtdLayer": ["0"], # used to determine whether track reaches ECal. This is a lower bound - I think setting this to 0 effectively gives all tracks "reachesCalorimeter = True" propery.
                              "ReachesECalNBarrelTrackerHits": ["0"], # used to determine whether track reaches ECal. This is a lower threshold on the number of hits to be considered.
                              "ReachesECalNFtdHits": ["0"], # used to determine whether track reaches ECal. This is a lower threshold on the number of hits to be considered.
                              "RelCaloHitCollections": ["CaloHitsRelations", "MuonHitsRelations"],
                              "RelTrackCollections": ["SiTracks_Refitted_Relations"],# for track refitting
                              #"RelTrackCollections": ["SiTracks_Relations"],
                              "ShouldFormTrackRelationships": ["1"],
                              "SoftwareCompensationEnergyDensityBins": ["0", "2.", "5.", "7.5", "9.5", "13.", "16.", "20.", "23.5", "28.", "33.", "40.", "50.", "75.", "100."],
                              "SoftwareCompensationWeights": ["1.61741", "-0.00444385", "2.29683e-05", "-0.0731236", "-0.00157099", "-7.09546e-07", "0.868443", "1.0561", "-0.0238574"],
                              "SplitVertexCollections": ["SplitVertices"],
                              "StartVertexAlgorithmName": ["PandoraPFANew"],
                              "StartVertexCollectionName": ["PandoraStartVertices"],
                              "StripSplittingOn": ["0"],
                              "TrackCollections": ["SiTracks_Refitted"], #for track refitting
                              #"TrackCollections": ["SiTracks"],
                              "TrackCreatorName": ["DDTrackCreatorCLIC"],
                              "TrackStateTolerance": ["0"],
                              "TrackSystemName": ["DDKalTest"],
                              "UnmatchedVertexTrackMaxEnergy": ["5"], #for track CanFormClusterlessPFO requirements
                              "UseEcalScLayers": ["0"],
                              "UseNonVertexTracks": ["1"], # for track CanFormPFO requirements. Setting to 1 is the loose, 0 is tight. 
                              "UseOldTrackStateCalculation": ["0"],
                              "UseUnmatchedNonVertexTracks": ["0"], # for track CanFormClusterlessPFO requirements. Setting to 1 is loose, 0 is tight.
                              "UseUnmatchedVertexTracks": ["1"],
                              "V0VertexCollections": ["V0Vertices"],
                              "YokeBarrelNormalVector": ["0", "0", "1"],
                              "Z0TrackCut": ["200"], # for track CanFormPFO requirements
                              "Z0UnmatchedVertexTrackCut": ["5"], #for track CanFormClusterlessPFO requirements
                              "ZCutForNonVertexTracks": ["250"] # for track CanFormPFO requirements
                              }

PFOSelection = MarlinProcessorWrapper("PFOSelection")
PFOSelection.OutputLevel = INFO
PFOSelection.ProcessorType = "CLICPfoSelector"
PFOSelection.Parameters = {
                           "ChargedPfoLooseTimingCut": ["3"],
                           "ChargedPfoNegativeLooseTimingCut": ["-1"],
                           "ChargedPfoNegativeTightTimingCut": ["-0.5"],
                           "ChargedPfoPtCut": ["0"],
                           "ChargedPfoPtCutForLooseTiming": ["4"],
                           "ChargedPfoTightTimingCut": ["1.5"],
                           "CheckKaonCorrection": ["0"],
                           "CheckProtonCorrection": ["0"],
                           "ClusterLessPfoTrackTimeCut": ["10"],
                           "CorrectHitTimesForTimeOfFlight": ["0"],
                           "DisplayRejectedPfos": ["1"],
                           "DisplaySelectedPfos": ["1"],
                           "FarForwardCosTheta": ["0.975"],
                           "ForwardCosThetaForHighEnergyNeutralHadrons": ["0.95"],
                           "ForwardHighEnergyNeutralHadronsEnergy": ["10"],
                           "HCalBarrelLooseTimingCut": ["20"],
                           "HCalBarrelTightTimingCut": ["10"],
                           "HCalEndCapTimingFactor": ["1"],
                           "InputPfoCollection": ["PandoraPFOs"],
                           "KeepKShorts": ["1"],
                           "MaxMomentumForClusterLessPfos": ["2"],
                           "MinECalHitsForTiming": ["5"],
                           "MinHCalEndCapHitsForTiming": ["5"],
                           "MinMomentumForClusterLessPfos": ["0.5"],
                           "MinPtForClusterLessPfos": ["0.5"],
                           "MinimumEnergyForNeutronTiming": ["1"],
                           "Monitoring": ["0"],
                           "MonitoringPfoEnergyToDisplay": ["1"],
                           "NeutralFarForwardLooseTimingCut": ["2"],
                           "NeutralFarForwardTightTimingCut": ["1"],
                           "NeutralHadronBarrelPtCutForLooseTiming": ["3.5"],
                           "NeutralHadronLooseTimingCut": ["2.5"],
                           "NeutralHadronPtCut": ["0"],
                           "NeutralHadronPtCutForLooseTiming": ["8"],
                           "NeutralHadronTightTimingCut": ["1.5"],
                           "PhotonFarForwardLooseTimingCut": ["2"],
                           "PhotonFarForwardTightTimingCut": ["1"],
                           "PhotonLooseTimingCut": ["2"],
                           "PhotonPtCut": ["0"],
                           "PhotonPtCutForLooseTiming": ["4"],
                           "PhotonTightTimingCut": ["1"],
                           "PtCutForTightTiming": ["0.75"],
                           "SelectedPfoCollection": ["SelectedPandoraPFOs"],
                           "UseClusterLessPfos": ["1"],
                           "UseNeutronTiming": ["0"]
                           }

# this algorithm isn't added right now (reduces file size and run time). 
FastJetProcessor = MarlinProcessorWrapper("FastJetProcessor")
FastJetProcessor.OutputLevel = INFO
FastJetProcessor.ProcessorType = "FastJetProcessor"
FastJetProcessor.Parameters = {
    "algorithm": ["antikt_algorithm", "0.4"],
    "clusteringMode": ["Inclusive", "5"],
    "jetOut": ["JetOut"],
    "recParticleIn": ["SelectedPandoraPFOs"],
    "recombinationScheme": ["E_scheme"]
}

algList.append(AIDA)
algList.append(EventNumber)
#algList.append(Config)
algList.append(DD4hep)
algList.append(CKFTracking)
algList.append(TrackDeduplication)
algList.append(TrackRefit)
algList.append(MyTrackTruth)
algList.append(MyTrackTruthSiTracks)
algList.append(DDMarlinPandora)
algList.append(PFOSelection)
#algList.append(FastJetProcessor)
algList.append(LCIOWriter_all)

from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = algList,
                EvtSel = 'NONE',
                EvtMax   = -1, #-1 is all
                ExtSvc = [evtsvc],
                OutputLevel=INFO
              )

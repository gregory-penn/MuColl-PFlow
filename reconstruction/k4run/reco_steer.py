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

Config = MarlinProcessorWrapper("Config")
Config.OutputLevel = INFO
Config.ProcessorType = "CLICRecoConfig"
Config.Parameters = {
                     "VertexUnconstrained": ["OFF"],
                     "VertexUnconstrainedChoices": ["ON", "OFF"]
                     }

AIDA = MarlinProcessorWrapper("AIDA")
AIDA.OutputLevel = INFO
AIDA.ProcessorType = "AIDAProcessor"
AIDA.Parameters = {
                   "Compress": ["1"],
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

#https://github.com/iLCSoft/Marlin/blob/6f8703a389987082363206e41e5ff1054ed1f444/source/src/LCIOOutputProcessor.cc
LCIOWriter_light = MarlinProcessorWrapper("LCIOWriter_light")
LCIOWriter_light.OutputLevel = INFO
LCIOWriter_light.ProcessorType = "LCIOOutputProcessor"
LCIOWriter_light.Parameters = {
                               "DropCollectionNames": [],
                               "DropCollectionTypes": ["SimCalorimeterHit", "CalorimeterHit", "SimTrackerHit", "TrackerHitPlane", "Track", "LCRelation"],
                               "FullSubsetCollections": [],
                               "KeepCollectionNames": ["SiTracks_Refitted", "SiTracks_Refitted_Relations", "PandoraPFOs", "MCPhysicsParticle", "MCParticle_SiTracks_Refitted", "RecoMCTruthLink"],
                               "LCIOOutputFile": ["output_reco_light.slcio"],
                               "LCIOWriteMode": ["WRITE_NEW"]
                               }

#https://github.com/MuonColliderSoft/ACTSTracking/blob/ce74f55a0ec320284ce8cc2d2d233a7f9c8b912d/src/ACTSSeededCKFTrackingProc.cxx#L45
CKFTracking = MarlinProcessorWrapper("CKFTracking")
CKFTracking.OutputLevel = INFO
CKFTracking.ProcessorType = "ACTSSeededCKFTrackingProc"
CKFTracking.Parameters = {
    "CKF_Chi2CutOff": ["10"],
    "CKF_NumMeasurementsCutOff": ["1"],
    "MatFile": [the_args.MatFile],
    "PropagateBackward": ["False"],
    "RunCKF": ["True"],
    "SeedFinding_CollisionRegion": ["3.5"], #this is 5 on Fede's (https://github.com/madbaron/SteeringMacros/blob/master/k4Reco/steer_reco_BIB_CONDOR.py#L44)
    "SeedFinding_DeltaRMax": ["60"], #this is 80 on Fede's
    "SeedFinding_DeltaRMin": ["2"], #this is 5 on Fede's
    "SeedFinding_DeltaRMaxBottom": ["50"], #this doesn't exist on Fede's - it is 0 by default
    "SeedFinding_DeltaRMaxTop": ["50"], #this doesn't exist on Fede's - it is 0 by default
    "SeedFinding_DeltaRMinBottom": ["5"], #this doesn't exist on Fede's - it is 0 by default
    "SeedFinding_DeltaRMinTop": ["2"], #this doesn't exist on Fede's - it is 0 by default
    "SeedFinding_ImpactMax": ["3"],
    "SeedFinding_MinPt": ["500"],
    "SeedFinding_RMax": ["150"],
    "SeedFinding_ZMax": ["500"], #this doesn't exist on Fede's - it is 600 by default.
    "SeedFinding_RadLengthPerSeed": ["0.1"], #this doesn't exist on Fede's. 0.1 is the default value, so this is consistent.
    "SeedFinding_zBottomBinLen": ["1"], #this doesn't exist on Fede's. 1 is the default value, so this is consistent.
    "SeedFinding_zTopBinLen": ["1"], #this doesn't exist on Fede's. 1 is the default value, so this is consistent.
    "SeedFinding_phiBottomBinLen": ["1"], #this doesn't exist on Fede's. 1 is the default value, so this is consistent.
    "SeedFinding_phiTopBinLen": ["1"], #this doesn't exist on Fede's. 1 is the default value, so this is consistent.
    "SeedFinding_SigmaScattering": ["3"], #this is 50 on Fede's
    "SeedingLayers": [
        "13", "2", "13", "6", "13", "10", "13", "14", 
        "14", "2", "14", "6", "14", "10", "14", "14", 
        "15", "2", "15", "6", "15", "10", "15", "14",
        ], #this is different on Fede's
    "TGeoFile": [the_args.TGeoFile],
    "TrackCollectionName": ["AllTracks"],
    "TrackerHitCollectionNames": ["VXDBarrelHits", "ITBarrelHits", "OTBarrelHits", "VXDEndcapHits", "ITEndcapHits", "OTEndcapHits"], # Fede has different names - may want to consider adding digi and reco together to more clearly harmonize naming choices
    "CaloFace_Radius": ["1.857"], #should be 1857, which is default anyways.
    "CaloFace_Z": ["2.307"] #default 
    # 
    # below is Fede's config for tracking 
    # "CKF_Chi2CutOff": ["10"],
    # "CKF_NumMeasurementsCutOff": ["1"],
    # "MatFile": [the_args.MatFile],
    # "PropagateBackward": ["False"],
    # "RunCKF": ["True"],
    # "SeedFinding_CollisionRegion": ["5"],
    # "SeedFinding_DeltaRMax": ["80"],
    # "SeedFinding_DeltaRMin": ["5"],
    # "SeedFinding_ImpactMax": ["3"],
    # "SeedFinding_MinPt": ["500"],
    # "SeedFinding_RMax": ["150"],
    # "SeedFinding_RadLengthPerSeed": ["0.1"],
    # "SeedFinding_SigmaScattering": ["50"],
    # "SeedingLayers": ["13", "2", "13", "6", "13", "10", "13", "14", 
    #                   "14", "2", "14", "6", "14", "10", "14", "14", 
    #                   "15", "2", "15", "6", "15", "10", "15", "14",
    #                   "8", "2",
    #                   "17", "2",
    #                   "18", "2"],
    # "TGeoFile": [the_args.TGeoFile],
    # "TrackCollectionName": ["AllTracks"],
    # "TrackerHitCollectionNames": ["VBTrackerHits", "IBTrackerHits", "OBTrackerHits", "VETrackerHits", "IETrackerHits", "OETrackerHits"]
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
    "TrackerHit2SimTrackerHitRelationName": ["VXDBarrelHitsRelations", "ITBarrelHitsRelations", "OTBarrelHitsRelations", "VXDEndcapHitsRelations", "ITEndcapHitsRelations", "OTEndcapHitsRelations"]
}

# https://github.com/MuonColliderSoft/ACTSTracking/blob/ce74f55a0ec320284ce8cc2d2d233a7f9c8b912d/src/TrackTruthProc.cxx#L20
MyTrackTruthSiTracks = MarlinProcessorWrapper("MyTrackTruthSiTracks")
MyTrackTruthSiTracks.OutputLevel = INFO
MyTrackTruthSiTracks.ProcessorType = "TrackTruthProc"
MyTrackTruthSiTracks.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "Particle2TrackRelationName": ["MCParticle_SiTracks"],
    "TrackCollection": ["SiTracks"],
    "TrackerHit2SimTrackerHitRelationName": ["VXDBarrelHitsRelations", "ITBarrelHitsRelations", "OTBarrelHitsRelations", "VXDEndcapHitsRelations", "ITEndcapHitsRelations", "OTEndcapHitsRelations"]
}

print("BEWARE: Track sigma(P)/P is edited.")

DDMarlinPandora = MarlinProcessorWrapper("DDMarlinPandora")
DDMarlinPandora.OutputLevel = INFO
DDMarlinPandora.ProcessorType = "DDPandoraPFANewProcessor"
DDMarlinPandora.Parameters = {
                              "Verbosity": ["MESSAGE"],
                              "ClusterCollectionName": ["PandoraClusters"],
                              "CreateGaps": ["false"],
                              "CurvatureToMomentumFactor": ["0.00015"], #is this correct? Looks like it is off by a factor of 2... it was 0.00015, I think 0.0003 is correct.
                              "D0TrackCut": ["200"], # cut for track CanFormPFO
                              "D0UnmatchedVertexTrackCut": ["5"], # used for CanFormClusterlessPFO
                              "DigitalMuonHits": ["0"],
                              "ECalBarrelNormalVector": ["0", "0", "1"],
                              "ECalCaloHitCollections": ["EcalBarrelCollectionRec", "EcalEndcapCollectionRec", "EcalPlugCollectionRec"], #this is for k4run digi
                              # "ECalCaloHitCollections": ["ECALBarrelHits", "ECALEndcapHits", "ECALOtherHits"], #this is for marlin digi
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
                              "HCalCaloHitCollections": ["HcalBarrelCollectionRec", "HcalEndcapCollectionRec", "HcalRingCollectionRec"], #this is for k4run digi
                              # "HCalCaloHitCollections": ["HCALBarrelHits", "HCALEndcapHits", "HCALOtherHits"], #this is for marlin digi
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
                              "MaxTrackSigmaPOverP": ["0.30"], # track quality cut. Upper bound. Default: 0.15. Better: 0.30
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
                              "PandoraSettingsXmlFile": ["PandoraSettings/PandoraSettingsFullClustering.xml"],
                              "ProngVertexCollections": ["ProngVertices"],
                              "ReachesECalBarrelTrackerOuterDistance": ["-100"], # used to determine whether track reaches ECal. L
                              "ReachesECalBarrelTrackerZMaxDistance": ["-50"], # used to determine whether track reaches ECal
                              "ReachesECalFtdZMaxDistance": ["1"],  # used to determine whether track reaches ECal. Some sort of "wiggle" room when finding which endcap layer a hit is in. 
                              "ReachesECalMinFtdLayer": ["0"], # used to determine whether track reaches ECal. This is a lower bound - I think setting this to 0 effectively gives all tracks "reachesCalorimeter = True" propery.
                              "ReachesECalNBarrelTrackerHits": ["0"], # used to determine whether track reaches ECal. This is a lower threshold on the number of hits to be considered.
                              "ReachesECalNFtdHits": ["0"], # used to determine whether track reaches ECal. This is a lower threshold on the number of hits to be considered.
                              # "RelCaloHitCollections": ["CaloHitsRelations", "MuonHitsRelations"],
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

RecoMCTruthLinker = MarlinProcessorWrapper("MyRecoMCTruthLinker")
RecoMCTruthLinker.OutputLevel = INFO
RecoMCTruthLinker.ProcessorType = "RecoMCTruthLinker"
RecoMCTruthLinker.Parameters = {
                            "MyRecoMCTruthLinker": ["1"],
                            "CalohitMCTruthLinkName": ["CalohitMCTruthLink"],
                            "ClusterCollection": ["PandoraClusters"],
                            "ClusterMCTruthLinkName": ["ClusterMCTruthLink"],
                            "FullRecoRelation": ["false"],
                            "InvertedNonDestructiveInteractionLogic": ["false"],
                            "KeepDaughtersPDG": ["22", "111", "310", "13", "211", "321", "3120"],
                            "MCParticleCollection": ["MCParticle"],
                            "MCParticlesSkimmedName": ["MCParticlesSkimmed"],
                            "MCTruthClusterLinkName": [],
                            "MCTruthRecoLinkName": [],
                            "MCTruthTrackLinkName": [],
                            "RecoMCTruthLinkName": ["RecoMCTruthLink"],
                            "RecoParticleCollection": ["MergedRecoParticles"],
                            "SaveBremsstrahlungPhotons": ["false"],
                            "SimCaloHitCollections": ["ECalBarrelCollection", "ECalEndcapCollection", "ECalPlugCollection", "HCalBarrelCollection", "HCalEndcapCollection", "HCalRingCollection", "YokeBarrelCollection", "YokeEndcapCollection"],
                            "SimCalorimeterHitRelationNames": ["RelationCaloHit", "RelationMuonHit"],
                            "SimTrackerHitCollections": ["VertexBarrelCollection", "VertexEndcapCollection", "InnerTrackerBarrelCollection", "OuterTrackerBarrelCollection", "InnerTrackerEndcapCollection", "OuterTrackerEndcapCollection"],
                            # "TrackCollection": ["SiTracks_Refitted"], # crashes for some reason. Not sure why. 
                            "TrackMCTruthLinkName": ["SiTracksMCTruthLink"],
                            "TrackerHitsRelInputCollections": ["VXDTrackerHitRelations", "VXDEndcapTrackerHitRelations", "InnerTrackerBarrelHitsRelations", "OuterTrackerBarrelHitsRelations", "InnerTrackerEndcapHitsRelations", "OuterTrackerEndcapHitsRelations"],
                            "UseTrackerHitRelations": ["true"],
                            "UsingParticleGun": ["true"],
                            "Verbosity": ["DEBUG6"], #("DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT")
                            "daughtersECutMeV": ["10"]
                            }

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

#hacking in my own algorithm to skip over the first 5 events
#from skipEvents import SkipFirstNEvents
# skipAlg = SkipFirstNEvents("SkipFirst5")
# skipAlg.skip = 2

# algList.append(skipAlg)
algList.append(AIDA)
algList.append(EventNumber)
algList.append(Config)
algList.append(DD4hep)
algList.append(CKFTracking)
algList.append(TrackDeduplication)
algList.append(TrackRefit)
algList.append(MyTrackTruth)
algList.append(MyTrackTruthSiTracks)
algList.append(DDMarlinPandora)
algList.append(PFOSelection)
#algList.append(RecoMCTruthLinker)
#algList.append(FastJetProcessor)
algList.append(LCIOWriter_all)
#algList.append(LCIOWriter_light)

from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = algList,
                EvtSel = 'NONE',
                EvtMax   = 1, #-1 is all
                ExtSvc = [evtsvc],
                OutputLevel=INFO
              )

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
    "--OverlayFullPathToMuPlus",
    help="Path to files for muplus BIB overlay",
    type=str,
    default="/path/to/muplus/",
)

parser.add_argument(
    "--OverlayFullPathToMuMinus",
    help="Path to files for muminus BIB overlay",
    type=str,
    default="/path/to/muminus/",
)

parser.add_argument(
    "--OverlayFullNumberBackground",
    help="Number of background files used for BIB overlay",
    type=str,
    default="1666", #Magic number (1666) assumes BIB was created with -n 42.66 phi clones of each MC particle
)

parser.add_argument(
    "--OverlayIPBackgroundFileNames",
    help="Path to files used for incoherent pairs overlay",
    type=str,
    default="/path/to/pairs.slcio",
)

parser.add_argument(
    "--doOverlayFull",
    help="Do BIB overlay",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--doOverlayIP",
    help="Do incoherent pairs overlay",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--doFilterDL",
    help="Do double-layer filtering",
    action="store_true",
    default=False,
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

AIDA = MarlinProcessorWrapper("AIDA")
AIDA.OutputLevel = INFO
AIDA.ProcessorType = "AIDAProcessor"
AIDA.Parameters = {
                   "Compress": ["1"],
                   "FileName": ["output_digi"],
                   "FileType": ["root"]
                   }

EventNumber = MarlinProcessorWrapper("EventNumber")
EventNumber.OutputLevel = INFO
EventNumber.ProcessorType = "Statusmonitor"
EventNumber.Parameters = {
                          "HowOften": ["1"]
                          }

LCIOWriter_all = MarlinProcessorWrapper("LCIOWriter_all")
LCIOWriter_all.OutputLevel = INFO
LCIOWriter_all.ProcessorType = "LCIOOutputProcessor"
LCIOWriter_all.Parameters = {
                             # Dropping all non-coned tracker hits to save file size
                             "DropCollectionNames": ["VBTrackerHits", "VBTrackerHitsRelations", "VETrackerHits", "VETrackerHitsRelations", "VertexBarrelCollection", "VertexEndcapCollection",
                                                      "IBTrackerHits", "IBTrackerHitsRelations", "InnerTrackerBarrelCollection", "IETrackerHits", "IETrackerHitsRelations", "InnerTrackerEndcapCollection",
                                                      "OBTrackerHits", "OBTrackerHitsRelations", "OuterTrackerBarrelCollection", "OETrackerHits", "OETrackerHitsRelations", "OuterTrackerEndcapCollection",
                                                      ],
                             "DropCollectionTypes": [],
                             "FullSubsetCollections": [],
                             "KeepCollectionNames": [],
                             "LCIOOutputFile": ["output_digi_onlyConedTrackerHits.slcio"],
                             "LCIOWriteMode": ["WRITE_NEW"]
                             }

# LCIOWriter_light = MarlinProcessorWrapper("LCIOWriter_light")
# LCIOWriter_light.OutputLevel = INFO
# LCIOWriter_light.ProcessorType = "LCIOOutputProcessor"
# LCIOWriter_light.Parameters = {
#                                "DropCollectionNames": ["MCParticle", "MCPhysicsParticle"],
#                                "DropCollectionTypes": ["SimTrackerHit", "SimCalorimeterHit", "LCRelation"],
#                                "FullSubsetCollections": [],
#                                "KeepCollectionNames": [],
#                                "LCIOOutputFile": ["output_digi_light.slcio"],
#                                "LCIOWriteMode": ["WRITE_NEW"]
#                                }

VXDBarrelDigitiser = MarlinProcessorWrapper("VXDBarrelDigitiser")
VXDBarrelDigitiser.OutputLevel = INFO
VXDBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDBarrelDigitiser.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.03"],
    "ResolutionU": ["0.005"],
    "ResolutionV": ["0.005"],
    "SimTrackHitCollectionName": ["VertexBarrelCollection"],
    "SimTrkHitRelCollection": ["VBTrackerHitsRelations"],
    "SubDetectorName": ["Vertex"],
    "TimeWindowMax": ["0.15"],
    "TimeWindowMin": ["-0.09"],
    "TrackerHitCollectionName": ["VBTrackerHits"],
    "UseTimeWindow": ["true"]
}

VXDEndcapDigitiser = MarlinProcessorWrapper("VXDEndcapDigitiser")
VXDEndcapDigitiser.OutputLevel = INFO
VXDEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDEndcapDigitiser.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.03"],
    "ResolutionU": ["0.005"],
    "ResolutionV": ["0.005"],
    "SimTrackHitCollectionName": ["VertexEndcapCollection"],
    "SimTrkHitRelCollection": ["VETrackerHitsRelations"],
    "SubDetectorName": ["Vertex"],
    "TimeWindowMax": ["0.15"],
    "TimeWindowMin": ["-0.09"],
    "TrackerHitCollectionName": ["VETrackerHits"],
    "UseTimeWindow": ["true"]
}

InnerPlanarDigiProcessor = MarlinProcessorWrapper("InnerPlanarDigiProcessor")
InnerPlanarDigiProcessor.OutputLevel = INFO
InnerPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
InnerPlanarDigiProcessor.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.06"],
    "ResolutionU": ["0.007"],
    "ResolutionV": ["0.090"],
    "SimTrackHitCollectionName": ["InnerTrackerBarrelCollection"],
    "SimTrkHitRelCollection": ["IBTrackerHitsRelations"],
    "SubDetectorName": ["InnerTrackers"],
    "TimeWindowMax": ["0.3"],
    "TimeWindowMin": ["-0.18"],
    "TrackerHitCollectionName": ["IBTrackerHits"],
    "UseTimeWindow": ["true"]
}

InnerEndcapPlanarDigiProcessor = MarlinProcessorWrapper("InnerEndcapPlanarDigiProcessor")
InnerEndcapPlanarDigiProcessor.OutputLevel = INFO
InnerEndcapPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
InnerEndcapPlanarDigiProcessor.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.06"],
    "ResolutionU": ["0.007"],
    "ResolutionV": ["0.090"],
    "SimTrackHitCollectionName": ["InnerTrackerEndcapCollection"],
    "SimTrkHitRelCollection": ["IETrackerHitsRelations"],
    "SubDetectorName": ["InnerTrackers"],
    "TimeWindowMax": ["0.3"],
    "TimeWindowMin": ["-0.18"],
    "TrackerHitCollectionName": ["IETrackerHits"],
    "UseTimeWindow": ["true"]
}

OuterPlanarDigiProcessor = MarlinProcessorWrapper("OuterPlanarDigiProcessor")
OuterPlanarDigiProcessor.OutputLevel = INFO
OuterPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
OuterPlanarDigiProcessor.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.06"],
    "ResolutionU": ["0.007"],
    "ResolutionV": ["0.090"],
    "SimTrackHitCollectionName": ["OuterTrackerBarrelCollection"],
    "SimTrkHitRelCollection": ["OBTrackerHitsRelations"],
    "SubDetectorName": ["OuterTrackers"],
    "TimeWindowMax": ["0.3"],
    "TimeWindowMin": ["-0.18"],
    "TrackerHitCollectionName": ["OBTrackerHits"],
    "UseTimeWindow": ["true"]
}

OuterEndcapPlanarDigiProcessor = MarlinProcessorWrapper(
    "OuterEndcapPlanarDigiProcessor")
OuterEndcapPlanarDigiProcessor.OutputLevel = INFO
OuterEndcapPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
OuterEndcapPlanarDigiProcessor.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.06"],
    "ResolutionU": ["0.007"],
    "ResolutionV": ["0.090"],
    "SimTrackHitCollectionName": ["OuterTrackerEndcapCollection"],
    "SimTrkHitRelCollection": ["OETrackerHitsRelations"],
    "SubDetectorName": ["OuterTrackers"],
    "TimeWindowMax": ["0.3"],
    "TimeWindowMin": ["-0.18"],
    "TrackerHitCollectionName": ["OETrackerHits"],
    "UseTimeWindow": ["true"]
}

VXDBarrelConer = MarlinProcessorWrapper("VXDBarrelConer")
VXDBarrelConer.OutputLevel = INFO
VXDBarrelConer.ProcessorType = "FilterConeHits"
VXDBarrelConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["VBTrackerHits"],
    "TrackerSimHitInputCollections": ["VertexBarrelCollection"],
    "TrackerHitInputRelations": ["VBTrackerHitsRelations"],
    "TrackerHitOutputCollections": ["VBTrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["VertexBarrelCollectionConed"],
    "TrackerHitOutputRelations": ["VBTrackerHitsRelationsConed"],
    "DeltaRCut": ["1.0"], 
    "FillHistograms": ["true"]
}

VXDEndcapConer = MarlinProcessorWrapper("VXDEndcapConer")
VXDEndcapConer.OutputLevel = INFO
VXDEndcapConer.ProcessorType = "FilterConeHits"
VXDEndcapConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["VETrackerHits"],
    "TrackerSimHitInputCollections": ["VertexEndcapCollection"],
    "TrackerHitInputRelations": ["VETrackerHitsRelations"],
    "TrackerHitOutputCollections": ["VETrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["VertexEndcapCollectionConed"],
    "TrackerHitOutputRelations": ["VETrackerHitsRelationsConed"],
    "DeltaRCut": ["1.0"], 
    "FillHistograms": ["true"]
}

InnerPlanarConer = MarlinProcessorWrapper("InnerPlanarConer")
InnerPlanarConer.OutputLevel = INFO
InnerPlanarConer.ProcessorType = "FilterConeHits"
InnerPlanarConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["IBTrackerHits"],
    "TrackerSimHitInputCollections": ["InnerTrackerBarrelCollection"],
    "TrackerHitInputRelations": ["IBTrackerHitsRelations"],
    "TrackerHitOutputCollections": ["IBTrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["InnerTrackerBarrelCollectionConed"],
    "TrackerHitOutputRelations": ["IBTrackerHitsRelationsConed"],
    "DeltaRCut": ["1.0"], 
    "FillHistograms": ["true"]
}

InnerEndcapConer = MarlinProcessorWrapper("InnerEndcapConer")
InnerEndcapConer.OutputLevel = INFO
InnerEndcapConer.ProcessorType = "FilterConeHits"
InnerEndcapConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["IETrackerHits"],
    "TrackerSimHitInputCollections": ["InnerTrackerEndcapCollection"],
    "TrackerHitInputRelations": ["IETrackerHitsRelations"],
    "TrackerHitOutputCollections": ["IETrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["InnerTrackerEndcapCollectionConed"],
    "TrackerHitOutputRelations": ["IETrackerHitsRelationsConed"],
    "DeltaRCut": ["1.0"], 
    "FillHistograms": ["true"]
}

OuterPlanarConer = MarlinProcessorWrapper("OuterPlanarConer")
OuterPlanarConer.OutputLevel = INFO
OuterPlanarConer.ProcessorType = "FilterConeHits"
OuterPlanarConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["OBTrackerHits"],
    "TrackerSimHitInputCollections": ["OuterTrackerBarrelCollection"],
    "TrackerHitInputRelations": ["OBTrackerHitsRelations"],
    "TrackerHitOutputCollections": ["OBTrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["OuterTrackerBarrelCollectionConed"],
    "TrackerHitOutputRelations": ["OBTrackerHitsRelationsConed"],
    "DeltaRCut": ["1.0"], 
    "FillHistograms": ["true"]
}

OuterEndcapConer = MarlinProcessorWrapper("OuterEndcapConer")
OuterEndcapConer.OutputLevel = INFO
OuterEndcapConer.ProcessorType = "FilterConeHits"
OuterEndcapConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["OETrackerHits"],
    "TrackerSimHitInputCollections": ["OuterTrackerEndcapCollection"],
    "TrackerHitInputRelations": ["OETrackerHitsRelations"],
    "TrackerHitOutputCollections": ["OETrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["OuterTrackerEndcapCollectionConed"],
    "TrackerHitOutputRelations": ["OETrackerHitsRelationsConed"],
    "DeltaRCut": ["1.0"], 
    "FillHistograms": ["true"]
}


ECalBarrelDigi = MarlinProcessorWrapper("ECalBarrelDigi")
ECalBarrelDigi.OutputLevel = INFO
ECalBarrelDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalBarrelCollection"],
    "outputHitCollections": ["EcalBarrelCollectionDigi"],
    "outputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalBarrelReco = MarlinProcessorWrapper("ECalBarrelReco")
ECalBarrelReco.OutputLevel = INFO
ECalBarrelReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["EcalBarrelCollectionDigi"],
    "inputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["EcalBarrelCollectionRec"],
    "outputRelationCollections": ["EcalBarrelRelationsSimRec"]
}

ECalPlugDigi = MarlinProcessorWrapper("ECalPlugDigi")
ECalPlugDigi.OutputLevel = INFO
ECalPlugDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalPlugDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalPlugCollection"],
    "outputHitCollections": ["ECalPlugCollectionDigi"],
    "outputRelationCollections": ["ECalPlugRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalPlugReco = MarlinProcessorWrapper("ECalPlugReco")
ECalPlugReco.OutputLevel = INFO
ECalPlugReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalPlugReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["ECalPlugCollectionDigi"],
    "inputRelationCollections": ["ECalPlugRelationsSimDigi"],
    "outputHitCollections": ["ECalPlugCollectionRec"],
    "outputRelationCollections": ["ECalPlugRelationsSimRec"]
}

ECalEndcapDigi = MarlinProcessorWrapper("ECalEndcapDigi")
ECalEndcapDigi.OutputLevel = INFO
ECalEndcapDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalEndcapCollection"],
    "outputHitCollections": ["EcalEndcapCollectionDigi"],
    "outputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalEndcapReco = MarlinProcessorWrapper("ECalEndcapReco")
ECalEndcapReco.OutputLevel = INFO
ECalEndcapReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["EcalEndcapCollectionDigi"],
    "inputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["EcalEndcapCollectionRec"],
    "outputRelationCollections": ["EcalEndcapRelationsSimRec"]
}

HCalBarrelDigi = MarlinProcessorWrapper("HCalBarrelDigi")
HCalBarrelDigi.OutputLevel = INFO
HCalBarrelDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004925"],
    "inputHitCollections": ["HCalBarrelCollection"],
    "outputHitCollections": ["HcalBarrelCollectionDigi"],
    "outputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["2.5e-04"],
    "thresholdUnit": ["GeV"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalBarrelReco = MarlinProcessorWrapper("HCalBarrelReco")
HCalBarrelReco.OutputLevel = INFO
HCalBarrelReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0287783798145"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalBarrelCollectionDigi"],
    "inputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["HcalBarrelCollectionRec"],
    "outputRelationCollections": ["HcalBarrelRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

HCalEndcapDigi = MarlinProcessorWrapper("HCalEndcapDigi")
HCalEndcapDigi.OutputLevel = INFO
HCalEndcapDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalEndcapCollection"],
    "outputHitCollections": ["HcalEndcapCollectionDigi"],
    "outputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["2.5e-04"],
    "thresholdUnit": ["GeV"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalEndcapReco = MarlinProcessorWrapper("HCalEndcapReco")
HCalEndcapReco.OutputLevel = INFO
HCalEndcapReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0285819096797"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalEndcapCollectionDigi"],
    "inputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["HcalEndcapCollectionRec"],
    "outputRelationCollections": ["HcalEndcapRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

HCalRingDigi = MarlinProcessorWrapper("HCalRingDigi")
HCalRingDigi.OutputLevel = INFO
HCalRingDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalRingDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalRingCollection"],
    "outputHitCollections": ["HCalRingCollectionDigi"],
    "outputRelationCollections": ["HCalRingRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["2.5e-04"],
    "thresholdUnit": ["GeV"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalRingReco = MarlinProcessorWrapper("HCalRingReco")
HCalRingReco.OutputLevel = INFO
HCalRingReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalRingReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0285819096797"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HCalRingCollectionDigi"],
    "inputRelationCollections": ["HCalRingRelationsSimDigi"],
    "outputHitCollections": ["HCalRingCollectionRec"],
    "outputRelationCollections": ["HCalRingRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

# MyEcalBarrelConer = MarlinProcessorWrapper("MyEcalBarrelConer")
# MyEcalBarrelConer.OutputLevel = INFO
# MyEcalBarrelConer.ProcessorType = "CaloConer"
# MyEcalBarrelConer.Parameters = {
#     "MCParticleCollectionName": ["MCParticle"],
#     "CaloHitCollectionName": ["EcalBarrelCollectionRec"],
#     "CaloRelationCollectionName": ["EcalBarrelRelationsSimRec"],
#     "GoodHitCollection": ["EcalBarrelCollectionConed"],
#     "GoodRelationCollection": ["EcalBarrelRelationsSimConed"],
#     "ConeWidth": ["0.2"]
# }

# MyEcalEndcapConer = MarlinProcessorWrapper("MyEcalEndcapConer")
# MyEcalEndcapConer.OutputLevel = INFO
# MyEcalEndcapConer.ProcessorType = "CaloConer"
# MyEcalEndcapConer.Parameters = {
#     "MCParticleCollectionName": ["MCParticle"],
#     "CaloHitCollectionName": ["EcalEndcapCollectionRec"],
#     "CaloRelationCollectionName": ["EcalEndcapRelationsSimRec"],
#     "GoodHitCollection": ["EcalEndcapCollectionConed"],
#     "GoodRelationCollection": ["EcalEndcapRelationsSimConed"],
#     "ConeWidth": ["0.2"]
# }

# MyHcalBarrelConer = MarlinProcessorWrapper("MyHcalBarrelConer")
# MyHcalBarrelConer.OutputLevel = INFO
# MyHcalBarrelConer.ProcessorType = "CaloConer"
# MyHcalBarrelConer.Parameters = {
#     "MCParticleCollectionName": ["MCParticle"],
#     "CaloHitCollectionName": ["HcalBarrelCollectionRec"],
#     "CaloRelationCollectionName": ["HcalBarrelRelationsSimRec"],
#     "GoodHitCollection": ["HcalBarrelCollectionConed"],
#     "GoodRelationCollection": ["HcalBarrelRelationsSimConed"],
#     "ConeWidth": ["0.2"]
# }

# MyHcalEndcapConer = MarlinProcessorWrapper("MyHcalEndcapConer")
# MyHcalEndcapConer.OutputLevel = INFO
# MyHcalEndcapConer.ProcessorType = "CaloConer"
# MyHcalEndcapConer.Parameters = {
#     "MCParticleCollectionName": ["MCParticle"],
#     "CaloHitCollectionName": ["HcalEndcapCollectionRec"],
#     "CaloRelationCollectionName": ["HcalEndcapRelationsSimRec"],
#     "GoodHitCollection": ["HcalEndcapCollectionConed"],
#     "GoodRelationCollection": ["HcalEndcapRelationsSimConed"],
#     "ConeWidth": ["0.2"]
# }

MuonDigitiser = MarlinProcessorWrapper("MuonDigitiser")
MuonDigitiser.OutputLevel = INFO
MuonDigitiser.ProcessorType = "DDSimpleMuonDigi"
MuonDigitiser.Parameters = {
                            "CalibrMUON": ["70.1"],
                            "MUONCollections": ["YokeBarrelCollection", "YokeEndcapCollection"],
                            "MUONOutputCollection": ["MuonHits"],
                            "MaxHitEnergyMUON": ["2.0"],
                            "MuonThreshold": ["1e-06"],
                            "RelationOutputCollection": ["MuonHitsRelations"]
                            }

FilterDL_VXDB = MarlinProcessorWrapper("FilterDL_VXDB")
FilterDL_VXDB.OutputLevel = INFO
FilterDL_VXDB.ProcessorType = "FilterDoubleLayerHits"
FilterDL_VXDB.Parameters = {
                            "DoubleLayerCuts": ["0", "1", "2.0", "35.0", "2", "3", "1.7", "18.0", "4", "5", "1.5", "10.0", "6", "7", "1.4", "6.5"],
                            "FillHistograms": ["false"],
                            "InputCollection": ["VXDBarrelHits"],
                            "OutputCollection": ["VXDBarrelHits_DLFiltered"],
                            "SubDetectorName": ["Vertex"]
                            }

FilterDL_VXDE = MarlinProcessorWrapper("FilterDL_VXDE")
FilterDL_VXDE.OutputLevel = INFO
FilterDL_VXDE.ProcessorType = "FilterDoubleLayerHits"
FilterDL_VXDE.Parameters = {
                            "DoubleLayerCuts": ["0", "1", "2.2", "8.0", "2", "3", "1.4", "2.8", "4", "5", "0.86", "0.7", "6", "7", "0.7", "0.3"],
                            "FillHistograms": ["false"],
                            "InputCollection": ["VXDEndcapHits"],
                            "OutputCollection": ["VXDEndcapHits_DLFiltered"],
                            "SubDetectorName": ["Vertex"]
                            }

OverlayFull = MarlinProcessorWrapper("OverlayFull")
OverlayFull.OutputLevel = WARNING
OverlayFull.ProcessorType = "OverlayTimingRandomMix"
OverlayFull.Parameters = {
    "PathToMuPlus": [the_args.OverlayFullPathToMuPlus],
    "PathToMuMinus": [the_args.OverlayFullPathToMuMinus],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.5", "15.",
        "VertexEndcapCollection", "-0.5", "15.",
        "InnerTrackerBarrelCollection", "-0.5", "15.",
        "InnerTrackerEndcapCollection", "-0.5", "15.",
        "OuterTrackerBarrelCollection", "-0.5", "15.",
        "OuterTrackerEndcapCollection", "-0.5", "15.",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalPlugCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "HCalRingCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MergeMCParticles": ["false"],
    "NumberBackground": [the_args.OverlayFullNumberBackground]
}

OverlayIP = MarlinProcessorWrapper("OverlayIP")
OverlayIP.OutputLevel = INFO
OverlayIP.ProcessorType = "OverlayTimingGeneric"
OverlayIP.Parameters = {
    "AllowReusingBackgroundFiles": ["true"],
    "BackgroundFileNames": [the_args.OverlayIPBackgroundFileNames],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.5", "15.",
        "VertexEndcapCollection", "-0.5", "15.",
        "InnerTrackerBarrelCollection", "-0.5", "15.",
        "InnerTrackerEndcapCollection", "-0.5", "15.",
        "OuterTrackerBarrelCollection", "-0.5", "15.",
        "OuterTrackerEndcapCollection", "-0.5", "15.",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalPlugCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "HCalRingCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "Delta_t": ["10000"],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MCPhysicsParticleCollectionName": ["MCPhysicsParticles_IP"],
    "MergeMCParticles": ["true"],
    "NBunchtrain": ["1"],
    "NumberBackground": ["1"],
    "PhysicsBX": ["1"],
    "Poisson_random_NOverlay": ["false"],
    "RandomBx": ["false"],
    "StartBackgroundFileIndex": ["0"],
    "TPCDriftvelocity": ["0.05"]
}

algList.append(AIDA)
algList.append(EventNumber)
algList.append(DD4hep)
if the_args.doOverlayFull:
    algList.append(OverlayFull)   # Full BX BIB overlay
if the_args.doOverlayIP:
    algList.append(OverlayIP)     # Incoherent pairs full BX BIB overlay
algList.append(VXDBarrelDigitiser)
algList.append(VXDEndcapDigitiser)
algList.append(InnerPlanarDigiProcessor)
algList.append(InnerEndcapPlanarDigiProcessor)
algList.append(OuterPlanarDigiProcessor)
algList.append(OuterEndcapPlanarDigiProcessor)
algList.append(VXDBarrelConer)
algList.append(VXDEndcapConer)
algList.append(InnerPlanarConer)
algList.append(InnerEndcapConer)
algList.append(OuterPlanarConer)
algList.append(OuterEndcapConer)
if the_args.doFilterDL:
    algList.append(FilterDL_VXDB)
    algList.append(FilterDL_VXDE)
algList.append(ECalBarrelDigi)
algList.append(ECalBarrelReco)
algList.append(ECalPlugDigi)
algList.append(ECalPlugReco)
algList.append(ECalEndcapDigi)
algList.append(ECalEndcapReco)
algList.append(HCalBarrelDigi)
algList.append(HCalBarrelReco)
algList.append(HCalEndcapDigi)
algList.append(HCalEndcapReco)
algList.append(HCalRingDigi)
algList.append(HCalRingReco)
# algList.append(MyEcalBarrelConer)
# algList.append(MyEcalEndcapConer)
# algList.append(MyHcalBarrelConer)
# algList.append(MyHcalEndcapConer)
algList.append(MuonDigitiser)
algList.append(LCIOWriter_all)
#algList.append(LCIOWriter_light)

from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = algList,
                EvtSel = 'NONE',
                EvtMax   = -1,
                ExtSvc = [evtsvc],
                OutputLevel=INFO
              )

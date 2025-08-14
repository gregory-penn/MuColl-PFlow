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
    "--ThresholdsPath",
    help="Path to files for ECal thresholds",
    type=str,
    default="/path/to/thresholds/",
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
                                                      "EcalBarrelCollectionDigi","EcalBarrelRelationsSimDigi", "EcalBarrelCollectionRec", "EcalBarrelRelationsSimRec", 
                                                      "EcalEndcapCollectionDigi","EcalEndcapRelationsSimDigi", "EcalEndcapCollectionRec", "EcalEndcapRelationsSimRec", 
                                                      "HcalBarrelCollectionDigi","HcalBarrelRelationsSimDigi", "HcalBarrelCollectionRec", "HcalBarrelRelationsSimRec", 
                                                      "HcalEndcapCollectionDigi","HcalEndcapRelationsSimDigi", "HcalEndcapCollectionRec", "HcalEndcapRelationsSimRec", 
                                                    #   "HcalRingCollectionDigi","HcalRingRelationsSimDigi", "HcalRingCollectionRec", "HcalRingRelationsSimRec", 
                                                      ],
                             "DropCollectionTypes": [],
                             "FullSubsetCollections": [],
                             "KeepCollectionNames": ["VBTrackerHitsConed", "IBTrackerHitsConed", "OBTrackerHitsConed", "VETrackerHitsConed", "IETrackerHitsConed", "OETrackerHitsConed", 
                                                     "EcalBarrelCollectionSel", "EcalBarrelRelationsSimSel",
                                                     "EcalEndcapCollectionSel", "EcalEndcapRelationsSimSel",
                                                    #  "EcalBarrelCollectionConed", "EcalBarrelRelationsSimConed",
                                                    #  "EcalEndcapCollectionConed", "EcalEndcapRelationsSimConed", 
                                                    #  "EcalPlugCollectionConed", "EcalPlugRelationsSimConed",
                                                    #  "HcalBarrelCollectionConed", "HcalBarrelRelationsSimConed",
                                                    #  "HcalEndcapCollectionConed", "HcalEndcapRelationsSimConed", 
                                                    #  "HcalRingCollectionConed", "HcalRingRelationsSimConed",
                                                     ],
                             "LCIOOutputFile": ["output_digi.slcio"],
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
    "DeltaRCut": ["0.8"],
    "FillHistograms": ["false"]
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
    "DeltaRCut": ["0.8"],
    "FillHistograms": ["false"]
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
    "DeltaRCut": ["0.8"],
    "FillHistograms": ["false"]
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
    "DeltaRCut": ["0.8"],
    "FillHistograms": ["false"]
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
    "DeltaRCut": ["0.8"],
    "FillHistograms": ["false"]
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
    "DeltaRCut": ["0.8"],
    "FillHistograms": ["false"]
}


MyEcalBarrelDigi = MarlinProcessorWrapper("MyEcalBarrelDigi")
MyEcalBarrelDigi.OutputLevel = INFO
MyEcalBarrelDigi.ProcessorType = "RealisticCaloDigiSilicon"
MyEcalBarrelDigi.Parameters = {
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

MyEcalBarrelReco = MarlinProcessorWrapper("MyEcalBarrelReco")
MyEcalBarrelReco.OutputLevel = INFO
MyEcalBarrelReco.ProcessorType = "RealisticCaloRecoSilicon"
MyEcalBarrelReco.Parameters = {
    #    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_factorsMipGev": ["0.0066150"], #used for v3
    #"calibration_factorsMipGev": ["0.00826875"],
    "calibration_layergroups": ["50"],
    "inputHitCollections": ["EcalBarrelCollectionDigi"],
    "inputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["EcalBarrelCollectionRec"],
    "outputRelationCollections": ["EcalBarrelRelationsSimRec"]
}

MyEcalEndcapDigi = MarlinProcessorWrapper("MyEcalEndcapDigi")
MyEcalEndcapDigi.OutputLevel = INFO
MyEcalEndcapDigi.ProcessorType = "RealisticCaloDigiSilicon"
MyEcalEndcapDigi.Parameters = {
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

MyEcalEndcapReco = MarlinProcessorWrapper("MyEcalEndcapReco")
MyEcalEndcapReco.OutputLevel = INFO
MyEcalEndcapReco.ProcessorType = "RealisticCaloRecoSilicon"
MyEcalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    #    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_factorsMipGev": ["0.0066150"], #used for v3
    #"calibration_factorsMipGev": ["0.00826875"],
    "calibration_layergroups": ["50"],
    "inputHitCollections": ["EcalEndcapCollectionDigi"],
    "inputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["EcalEndcapCollectionRec"],
    "outputRelationCollections": ["EcalEndcapRelationsSimRec"]
}

MyHcalBarrelDigi = MarlinProcessorWrapper("MyHcalBarrelDigi")
MyHcalBarrelDigi.OutputLevel = INFO
MyHcalBarrelDigi.ProcessorType = "RealisticCaloDigiScinPpd"
MyHcalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalBarrelCollection"],
    "outputHitCollections": ["HcalBarrelCollectionDigi"],
    "outputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"]
}

MyHcalBarrelReco = MarlinProcessorWrapper("MyHcalBarrelReco")
MyHcalBarrelReco.OutputLevel = INFO
MyHcalBarrelReco.ProcessorType = "RealisticCaloRecoScinPpd"
MyHcalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    #    "calibration_factorsMipGev": ["0.0287783798145"],
    "calibration_factorsMipGev": ["0.024625"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalBarrelCollectionDigi"],
    "inputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["HcalBarrelCollectionRec"],
    "outputRelationCollections": ["HcalBarrelRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

MyHcalEndcapDigi = MarlinProcessorWrapper("MyHcalEndcapDigi")
MyHcalEndcapDigi.OutputLevel = INFO
MyHcalEndcapDigi.ProcessorType = "RealisticCaloDigiScinPpd"
MyHcalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalEndcapCollection"],
    "outputHitCollections": ["HcalEndcapCollectionDigi"],
    "outputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"]
}

MyHcalEndcapReco = MarlinProcessorWrapper("MyHcalEndcapReco")
MyHcalEndcapReco.OutputLevel = INFO
MyHcalEndcapReco.ProcessorType = "RealisticCaloRecoScinPpd"
MyHcalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    #   "calibration_factorsMipGev": ["0.0285819096797"],
    "calibration_factorsMipGev": ["0.024625"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalEndcapCollectionDigi"],
    "inputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["HcalEndcapCollectionRec"],
    "outputRelationCollections": ["HcalEndcapRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

MyEcalBarrelConer = MarlinProcessorWrapper("MyEcalBarrelConer")
MyEcalBarrelConer.OutputLevel = INFO
MyEcalBarrelConer.ProcessorType = "CaloConer"
MyEcalBarrelConer.Parameters = {
    "MCParticleCollectionName": ["MCParticle"],
    "CaloHitCollectionName": ["EcalBarrelCollectionRec"],
    "CaloRelationCollectionName": ["EcalBarrelRelationsSimRec"],
    "GoodHitCollection": ["EcalBarrelCollectionConed"],
    "GoodRelationCollection": ["EcalBarrelRelationsSimConed"],
    "ConeWidth": ["0.4"]
}

MyEcalEndcapConer = MarlinProcessorWrapper("MyEcalEndcapConer")
MyEcalEndcapConer.OutputLevel = INFO
MyEcalEndcapConer.ProcessorType = "CaloConer"
MyEcalEndcapConer.Parameters = {
    "MCParticleCollectionName": ["MCParticle"],
    "CaloHitCollectionName": ["EcalEndcapCollectionRec"],
    "CaloRelationCollectionName": ["EcalEndcapRelationsSimRec"],
    "GoodHitCollection": ["EcalEndcapCollectionConed"],
    "GoodRelationCollection": ["EcalEndcapRelationsSimConed"],
    "ConeWidth": ["0.4"]
}

MyHcalBarrelConer = MarlinProcessorWrapper("MyHcalBarrelConer")
MyHcalBarrelConer.OutputLevel = INFO
MyHcalBarrelConer.ProcessorType = "CaloConer"
MyHcalBarrelConer.Parameters = {
    "MCParticleCollectionName": ["MCParticle"],
    "CaloHitCollectionName": ["HcalBarrelCollectionRec"],
    "CaloRelationCollectionName": ["HcalBarrelRelationsSimRec"],
    "GoodHitCollection": ["HcalBarrelCollectionConed"],
    "GoodRelationCollection": ["HcalBarrelRelationsSimConed"],
    "ConeWidth": ["0.4"]
}

MyHcalEndcapConer = MarlinProcessorWrapper("MyHcalEndcapConer")
MyHcalEndcapConer.OutputLevel = INFO
MyHcalEndcapConer.ProcessorType = "CaloConer"
MyHcalEndcapConer.Parameters = {
    "MCParticleCollectionName": ["MCParticle"],
    "CaloHitCollectionName": ["HcalEndcapCollectionRec"],
    "CaloRelationCollectionName": ["HcalEndcapRelationsSimRec"],
    "GoodHitCollection": ["HcalEndcapCollectionConed"],
    "GoodRelationCollection": ["HcalEndcapRelationsSimConed"],
    "ConeWidth": ["0.4"]
}

MyEcalBarrelSelector = MarlinProcessorWrapper("MyEcalBarrelSelector")
MyEcalBarrelSelector.OutputLevel = INFO
MyEcalBarrelSelector.ProcessorType = "CaloHitSelector"
MyEcalBarrelSelector.Parameters = {
    "CaloHitCollectionName": ["EcalBarrelCollectionConed"],
    "CaloRelationCollectionName": ["EcalBarrelRelationsSimConed"],
    "GoodHitCollection": ["EcalBarrelCollectionSel"],
    "GoodRelationCollection": ["EcalBarrelRelationsSimSel"],
    "ThresholdsFilePath": [the_args.OverlayFullPathToMuMinus + "/ECAL_Thresholds_10TeV.root"],
    "Nsigma": ["0"],
    "DoBIBsubtraction": ["false"]
}

MyEcalEndcapSelector = MarlinProcessorWrapper("MyEcalEndcapSelector")
MyEcalEndcapSelector.OutputLevel = INFO
MyEcalEndcapSelector.ProcessorType = "CaloHitSelector"
MyEcalEndcapSelector.Parameters = {
    "CaloHitCollectionName": ["EcalEndcapCollectionConed"],
    "CaloRelationCollectionName": ["EcalEndcapRelationsSimConed"],
    "GoodHitCollection": ["EcalEndcapCollectionSel"],
    "GoodRelationCollection": ["EcalEndcapRelationsSimSel"],
    "ThresholdsFilePath": [the_args.OverlayFullPathToMuMinus + "/ECAL_Thresholds_10TeV.root"],
    "Nsigma": ["0"],
    "DoBIBsubtraction": ["false"]
}

MyDDSimpleMuonDigi = MarlinProcessorWrapper("MyDDSimpleMuonDigi")
MyDDSimpleMuonDigi.OutputLevel = INFO
MyDDSimpleMuonDigi.ProcessorType = "DDSimpleMuonDigi"
MyDDSimpleMuonDigi.Parameters = {
    "CalibrMUON": ["70.1"],
    "MUONCollections": ["YokeBarrelCollection", "YokeEndcapCollection"],
    "MUONOutputCollection": ["MUON"],
    "MaxHitEnergyMUON": ["2.0"],
    "MuonThreshold": ["1e-06"],
    "RelationOutputCollection": ["RelationMuonHit"]
}

OverlayFull = MarlinProcessorWrapper("OverlayFull")
OverlayFull.OutputLevel = WARNING
OverlayFull.ProcessorType = "OverlayTimingRandomMix"
OverlayFull.Parameters = {
    "PathToMuPlus": [the_args.OverlayFullPathToMuPlus],
    "PathToMuMinus": [the_args.OverlayFullPathToMuMinus],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.18", "0.18",
        "VertexEndcapCollection", "-0.18", "0.18",
        "InnerTrackerBarrelCollection", "-0.36", "0.36",
        "InnerTrackerEndcapCollection", "-0.36", "0.36",
        "OuterTrackerBarrelCollection", "-0.36", "0.36",
        "OuterTrackerEndcapCollection", "-0.36", "0.36",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MergeMCParticles": ["false"],
    "NumberBackground": [the_args.OverlayFullNumberBackground] # default should be 1666
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
algList.append(MyEcalBarrelDigi)
algList.append(MyEcalBarrelReco)
algList.append(MyEcalEndcapDigi)
algList.append(MyEcalEndcapReco)
algList.append(MyHcalBarrelDigi)
algList.append(MyHcalBarrelReco)
algList.append(MyHcalEndcapDigi)
algList.append(MyHcalEndcapReco)
algList.append(MyEcalBarrelConer)
algList.append(MyEcalEndcapConer)
# algList.append(MyHcalBarrelConer)
algList.append(MyHcalEndcapConer)
algList.append(MyDDSimpleMuonDigi)
algList.append(LCIOWriter_all)
#algList.append(LCIOWriter_light)

from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = algList,
                EvtSel = 'NONE',
                EvtMax   = 1,
                ExtSvc = [evtsvc],
                OutputLevel=INFO
              )

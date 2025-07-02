from pyLCIO import IOIMPL, EVENT, UTIL
from argparse import ArgumentParser
import math
import pickle
import os

# Command line arguments
parser = ArgumentParser()

# Input file
parser.add_argument('-i', '--inputFile', help='--inputFile input_reco.slcio', 
                  type=str, default='output_reco.slcio') 

args = parser.parse_args()

#print statements?
DEBUG = False

# global vars for MAIA B-field and factor to express momentum in GeV
BFIELD = 5.0 # Taking 5 T for MAIA and 3.57 T for MuColl_v1. 
FACTOR = 3e-4 # conversion factor to take T calculation to GeV pT
SiTrackContainer = "SiTracks_Refitted" # may want to read SiTracks. Depends on job.
particle_type = "pion"
file_name = "momentum_res_" + particle_type + SiTrackContainer + ".pkl" # name of output file

to_process = []

if os.path.isdir(args.inputFile):
  for r, d, f in os.walk(args.inputFile):
    for file in f:
      to_process.append(os.path.join(r, file))
else:
  to_process.append(args.inputFile)

# helper functions 
def get_theta(px, py, pz):
    pt = math.sqrt(px**2 + py**2)
    return math.atan2(pt, pz)

def get_phi(px, py):
    return math.atan2(py, px)

def getSigmaPOverP(track):
      wResStdDev = track.getCovMatrix()[5]
      tLResStdDev = track.getCovMatrix()[14]
      wtLRes = track.getCovMatrix()[12]
      omega, tan_lambda = (
            track.getOmega(), #signed curvature of track in 1/mm
            track.getTanLambda(), #"dip angle" in r-z at reference point
            )
      pt = BFIELD * FACTOR / abs(omega)
      pz = pt * tan_lambda
      p = math.sqrt(pt * pt + pz * pz)

    # below is for momentum resolution
    #   partialPOverWSquared = 1 / (omega**4) * (1 + tan_lambda**2)
    #   partialPOvertLSquared = tan_lambda**2/(omega**2 * (1 + tan_lambda**2))

    #   sigmaPOverP = BFIELD * FACTOR / p * math.sqrt(
    #      partialPOverWSquared * wResStdDev + 
    #      partialPOvertLSquared * tLResStdDev + 
    #      2 * math.sqrt(partialPOverWSquared * partialPOvertLSquared) * wtLRes)

    # below is for transverse momentum resolution
      sigmaPOverP = math.sqrt(wResStdDev) / math.fabs(omega)

      return(sigmaPOverP)

def getDr(MCP, track):
  trk_omega, trk_tan_lambda, trk_phi = (
    track.getOmega(), #signed curvature of track in 1/mm
    track.getTanLambda(), #"dip angle" in r-z at reference point
    track.getPhi(),
    )
  trk_theta = (math.pi / 2) - math.atan(trk_tan_lambda)
  mcx, mcy, mcz = (MCP.getMomentum()[0], MCP.getMomentum()[1], MCP.getMomentum()[2])
  mc_theta = get_theta(mcx, mcy, mcz)
  mc_phi = get_phi(mcx,mcy)

  dtheta = mc_theta - trk_theta
  dphi = mc_phi - trk_phi

  if dphi > math.pi:
     print("Hit loop case")
     print(dphi)
     dphi = math.fabs(dphi - 2 * math.pi)
     print(dphi)

  return math.sqrt(dtheta * dtheta + dphi * dphi)

# track-level quantities
trksigmaPOverP = []
trksigmad0 = []
trksigmaz0 = []
trkPt = []
trkTheta = []
trkChi2nDOF = []
trknHits = []
trkd0 = []
trkz0 = []


# event-level (truth-track level for a particle gun) variables
trackFound = []
truthpt = []
truththeta = []
matchedTrkdR = []

# for truth matching studies. Only plotting 
# matched_trk_pt_ratio = []
# matched_trk_nhits = []
# matched_trk_dr = []
# unmatched_trk_pt_ratio = []
# unmatched_trk_nhits = []
# unmatched_trk_dr = []

# begin loop over files

for file in to_process:
  reader = IOIMPL.LCFactory.getInstance().createLCReader()
  reader.open(file)

  # Loop through Events
  for ievt, event in enumerate(reader):
    #my_tracks = event.getCollection(SiTrackContainer)
    #my_mcp = event.getCollection("MCParticle")[0]
    my_truth_trks = event.getCollection("MCParticle_SiTracks_Refitted")
    my_mcp_list = []
    my_tracks = []

    # if my_truth_trks.getNumberOfElements() > 1:
    #    print("More than one truth track. There are: ", my_truth_trks.getNumberOfElements())

    for i in range(my_truth_trks.getNumberOfElements()):
       relationO = my_truth_trks.getElementAt(i)
       my_mcp = relationO.getFrom()
       my_mcp_list.append(relationO.getFrom())
       my_tracks.append(relationO.getTo())
       weight = relationO.getWeight() # weights != 1 when there exist multiple truth tracks. I assume the track with the higher weight contains "more" of the truth particle

      #  if weight != 1.0:
      #     print("Weight different from 1! It is: ", weight)
      #     print("There are ", my_truth_trks.getNumberOfElements() , " tracks")
      #     print("\n")

    if len(my_tracks) == 0:
       continue

    if abs(my_mcp.getPDG()) != 211:
       print("my_mcp PDG ID: ", my_mcp.getPDG())
       print("First MCP isn't a", particle_type , ". There are ", len(my_mcp_list), " MC particles.")
       print("The second PDG ID is: ", my_mcp_list[1].getPDG())
       print("It seems that this occurs when there is either a missing track or mutliple tracks")
       print("I've noticed that when this happens, the first  ")
       print("Maybe there's a missing track? Number of tracks: ", len(my_tracks))
       print("\n")
      #  exit()

    mcx, mcy, mcz = (my_mcp.getMomentum()[0], my_mcp.getMomentum()[1], my_mcp.getMomentum()[2])
    truthpt.append(math.sqrt(mcx*mcx + mcy*mcy))
    truththeta.append(get_theta(mcx, mcy, mcz))

    if len(my_tracks) == 0:
       trackFound.append(0)
       continue
    if len(my_tracks) > 1:
       dRTracks = []
       for i in range(0,len(my_tracks)):
          dRTracks.append(getDr(my_mcp, my_tracks[i]))
      # find closest track to truth pion
      #  print(dRTracks)
      #  print(min(dRTracks))
      #  print(dRTracks.index(min(dRTracks)))
       myTrack = my_tracks[dRTracks.index(min(dRTracks))]
       trackFound.append(1)

    elif len(my_tracks) != 0:
       myTrack = my_tracks[0]    
       trackFound.append(1)

    omega, tan_lambda, phi = (
          myTrack.getOmega(), #signed curvature of track in 1/mm
          myTrack.getTanLambda(), #"dip angle" in r-z at reference point
          myTrack.getPhi(),
          )
    theta = (math.pi / 2) - math.atan(tan_lambda)
    pt = BFIELD * FACTOR / abs(omega)
    pz = pt * tan_lambda
    p = math.sqrt(pt * pt + pz * pz)

    chi2, ndf, nHits = myTrack.getChi2(), myTrack.getNdf(), len(myTrack.getTrackerHits())

    trksigmaPOverP.append(getSigmaPOverP(myTrack))
    trksigmad0.append(myTrack.getCovMatrix()[0])
    trksigmaz0.append(myTrack.getCovMatrix()[6])
    trkPt.append(pt)
    trkTheta.append(theta)
    trkChi2nDOF.append(chi2 / ndf)
    trknHits.append(nHits)
    trkd0.append(myTrack.getD0())
    trkz0.append(myTrack.getZ0())
    matchedTrkdR.append(getDr(my_mcp, myTrack))

      # a bunch of print statements
    if DEBUG: 
        print("track momentum: ", pt)
        print("track sigma(pT)/pT is: ", getSigmaPOverP(myTrack))
        print("\n")


#I guess pickle is good with this? Note for self - supposedly this isn't secure.
with open(file_name, "wb") as f:
    pickle.dump((trksigmaPOverP, trksigmad0, trksigmaz0, trkPt, trkTheta, trkChi2nDOF, trknHits, trkd0, trkz0, trackFound, truthpt, truththeta, matchedTrkdR), f)

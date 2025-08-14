# in this variation, I largely want to study charged pion efficiency and calorimeter resolution in the presence of BIB
# some form of truth matching must be made.
# truth matching done in paper: objects identified as X are truth matched to a truth X if it is within dR < 0.1 and reco energy > some threshold (20 GeV for photons)

from pyLCIO import IOIMPL, EVENT, UTIL
from argparse import ArgumentParser
import math
import pickle
import os

# Command line arguments
parser = ArgumentParser()

# Input file
parser.add_argument('-i', '--inputFile', help='--inputFil input_reco.slcio', 
                  type=str, default='output_reco.slcio') 

args = parser.parse_args()

#print statements?
DEBUG = True

# global vars for MAIA B-field and factor to express momentum in GeV
BFIELD = 5.0 # Taking 5 T for MAIA and 3.57 T for MuColl_v1. 
FACTOR = 3e-4 # conversion factor to take T calculation to GeV pT
SiTrackContainer = "SiTracks_Refitted" # input tracking container to pandora.
particle_type = "pion" # what truth particle we're looking for. only matters for naming.
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

# may not be necessary? delete if not.
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

# necessary for truth matching, but I probably want between an MCP and a PFO.
def getDr(MCP, pfo):
  mcx, mcy, mcz = (MCP.getMomentum()[0], MCP.getMomentum()[1], MCP.getMomentum()[2])
  mc_theta = get_theta(mcx, mcy, mcz)
  mc_phi = get_phi(mcx,mcy)

  pfox, pfoy, pfoz = (pfo.getMomentum()[0], pfo.getMomentum()[1], pfo.getMomentum()[2])
  pfo_theta = get_theta(pfox, pfoy, pfoz)
  pfo_phi = get_phi(pfox, pfoy)


  dtheta = mc_theta - pfo_theta
  dphi = mc_phi - pfo_phi

  if dphi > math.pi:
     #print("Hit loop case")
     #print(dphi)
     dphi = math.fabs(dphi - 2 * math.pi)
     #print(dphi)

  return math.sqrt(dtheta * dtheta + dphi * dphi)

# event-level (truth-track level for a particle gun) variables
truthpt = []
truththeta = []

# begin loop over files

for file in to_process:
  reader = IOIMPL.LCFactory.getInstance().createLCReader()
  reader.open(file)

  # Loop through Events
  for ievt, event in enumerate(reader):
    my_tracks = event.getCollection(SiTrackContainer)
    my_mcp = event.getCollection("MCParticle")[0] # confirmed through looping through and finding MCP with no parents that first in list is the generated particle
    my_truth_trks = event.getCollection("MCParticle_SiTracks_Refitted")
    my_cluster = event.getCollection('PandoraClusters')
    my_pfos = event.getCollection('PandoraPFOs')

    truthE = my_mcp.getEnergy()
    print("truth MCP energy: " , truthE)

    n_ele = 0
    n_muon = 0
    n_photon = 0
    n_pion = 0
    n_neutron = 0
    n_other = 0

    n_close_ele = 0
    n_close_muon = 0
    n_close_photon = 0
    n_close_pion = 0
    n_close_neutron = 0


    truth_match_cone = 0.1
    pfos_close_to_MCP = [] # list of PFOs that are within some dR  (above variable) of the truth particle

    for pfo in my_pfos:
       pfo_type = pfo.getType()
       drTruth = getDr(my_mcp, pfo)
       if abs(pfo_type) == 211:
          n_pion += 1
       elif abs(pfo_type) == 11:
          n_ele += 1
       elif abs(pfo_type) == 13:
          n_muon += 1
       elif abs(pfo_type) == 22:
          n_photon += 1
       elif abs(pfo_type) == 2112:
          n_neutron += 1
       else:
        print("some other particle, PDG ID = ", pfo_type) 
        n_other += 1
      
       if drTruth < 0.1:
          pfos_close_to_MCP.append(pfo)

        
    if DEBUG:
      print("Number of PFOs within dR < ", truth_match_cone, " of the MCP: ", len(pfos_close_to_MCP))
      print("Number of PFOs: ", len(my_pfos))
      print("Number of tracks: ", len(my_tracks))    
      print("Number of reco electrons: ", n_ele)
      print("Number of reco muons: ", n_muon)
      print("Number of reco photons: ", n_photon)
      print("Number of reco pions: ", n_pion)
      print("Number of reco neutrons: ", n_neutron)    
#    print("Number of other stuff: ", n_other)
      print("\n")

    for pfo in pfos_close_to_MCP:
       pfo_type = pfo.getType()
       if abs(pfo_type) == 11:
          n_close_ele += 1
       elif abs(pfo_type) == 13:
          n_close_muon += 1
       elif abs(pfo_type) == 22:
          n_close_photon += 1
       elif abs(pfo_type) == 2112:
          n_close_neutron += 1
       elif abs(pfo_type) == 211:
          n_close_pion += 1
          if DEBUG:
            print("Reco pion energy: ", pfo.getEnergy())
            print("residual w.r.t. truth: ", (pfo.getEnergy() - truthE) / truthE)

       # should be one cluster per PFO, but just in case, loop over
          for pion_cls in pfo.getClusters():
            cluster_E = pion_cls.getEnergy()

            print("Calo E of reco pion: ", cluster_E)
            print("Residual with truth E: ", (cluster_E - truthE) / truthE)
          
       
    # print("Number of close reco electrons: ", n_close_ele)
    # print("Number of close reco muons: ", n_close_muon)
    # print("Number of close reco photons: ", n_close_photon)
    # print("Number of close reco pions: ", n_close_pion)
    # print("Number of close reco neutrons: ", n_close_neutron)    
    print("\n")


#I guess pickle is good with this? Note for self - supposedly this isn't secure.
# with open(file_name, "wb") as f:
#     pickle.dump((trksigmaPOverP, trksigmad0, trksigmaz0, trkPt, trkTheta, trkChi2nDOF, trknHits, trkd0, trkz0, trackFound, truthpt, truththeta, matchedTrkdR), f)

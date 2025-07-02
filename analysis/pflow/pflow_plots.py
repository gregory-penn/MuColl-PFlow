from pyLCIO import IOIMPL, EVENT, UTIL
from ROOT import TH1F, TFile, TCanvas, gStyle, TLegend, TLatex
from argparse import ArgumentParser
import os
import math

# Command line arguments
parser = ArgumentParser()

# Input file
parser.add_argument('-i', '--inputFile', help='--inputFile input_reco.slcio', 
                  type=str, default='output_reco.slcio') 

# Output file
parser.add_argument('-o', '--outputFile', help='--outputFile plot.root', 
                  type=str, default='plot.root')
args = parser.parse_args()

#set global style
gStyle.SetTitleSize(0.042, "X")
gStyle.SetTitleSize(0.042, "Y")
#disabling plot titles - personal preference
gStyle.SetOptTitle(0)
gStyle.SetLineWidth(2)
gStyle.SetOptStat(0) # remove stat box at upper right corner 
gStyle.SetPadLeftMargin(0.13)
gStyle.SetPadRightMargin(0.07)

pl1Color = 30
pl2Color = 46
pl3Color = 38

#helper functions for calculating theta and phi
def get_theta(px, py, pz):
    pt = math.sqrt(px**2 + py**2)
    return math.atan2(pt, pz)

def get_phi(px, py):
    return math.atan2(py, px)

hists = []

nClusters = TH1F('number of clusters', 'nClusters', 9, 0, 9)
nClusters.SetXTitle('n_{clusters}')
nClusters.SetMinimum(0.0)
# nClusters.SetMaximum(650.0)
nClusters.SetLineColor(1);
nClusters.SetLineWidth(2)
nClusters.SetMarkerStyle(8)
nClusters.SetMarkerColor(1)
nClusters.GetYaxis().SetTitle("Entries")
hists.append(nClusters)

nPFOs = TH1F('number of PFOs', 'nPFOs', 15, 0, 15)
nPFOs.SetXTitle('# of PFOs')
nPFOs.SetMinimum(0.0)
#nPFOs.SetMaximum(550.0)
nPFOs.SetLineColor(pl1Color);
nPFOs.SetLineWidth(2)
nPFOs.SetMarkerStyle(8)
nPFOs.SetMarkerColor(pl1Color)
nPFOs.GetYaxis().SetTitle("Entries")
hists.append(nPFOs)

fRecoPiPt = TH1F('RecoPiPt', 'RecoPiPt', 20, 0, 350)
fRecoPiPt.SetXTitle('\pi^{-} p_{T} (GeV)')
fRecoPiPt.SetMinimum(0.0)
fRecoPiPt.GetYaxis().SetTitle("Entries")
hists.append(fRecoPiPt)

fRecoPiTheta = TH1F('RecoPiTheta', 'RecoPiTheta', 20, 0, 3.14159)
fRecoPiTheta.SetXTitle('\pi^{-} #theta (rad)')
fRecoPiTheta.SetMinimum(0.0)
fRecoPiTheta.GetYaxis().SetTitle("Entries")
hists.append(fRecoPiTheta)

fRecoPiPhi = TH1F('RecoPiPhi', 'RecoPiPhi', 20, -3.14159, 3.14159)
fRecoPiPhi.SetXTitle('\pi^{-} #phi (rad)')
fRecoPiPhi.SetMinimum(0.0)
fRecoPiPhi.GetYaxis().SetTitle("Entries")
hists.append(fRecoPiPhi)

jetLikeE = TH1F('jetLikeE', 'jetLikeE', 40, 0, 350)
jetLikeE.SetXTitle('Jet-like Energy (GeV)')
jetLikeE.SetMinimum(0.0)
jetLikeE.GetYaxis().SetTitle("Entries")
hists.append(jetLikeE)

jetLikeERatio = TH1F('jetLikeERatio', 'jetLikeERatio', 40, 0., 5.)
jetLikeERatio.SetXTitle('E^{reco} / E^{truth}')
jetLikeERatio.SetMinimum(0.0)
jetLikeERatio.GetYaxis().SetTitle("Entries")
hists.append(jetLikeERatio)

pfoPDG = TH1F('pfos_pdgID', 'pfos_PDGID', 3000, 0., 3000.)
pfoPDG.SetXTitle('PDG ID')
pfoPDG.SetMinimum(0.0)
pfoPDG.GetYaxis().SetTitle("Entries")
hists.append(pfoPDG)

pfoPDGMisID = TH1F('pfos_pdgID_MisID', 'pfos_PDGID_MisID', 3000, 0., 3000.)
pfoPDGMisID.SetXTitle('PDG ID')
pfoPDGMisID.SetMinimum(0.0)
pfoPDGMisID.GetYaxis().SetTitle("Entries")
hists.append(pfoPDGMisID)


######################################################################################################
BFIELD = 5 # Taking 5 T for MAIA and 3.57 T for MuColl_v1. I think this is correct?
FACTOR = 3e-4 #some conversion factor to take T calculation to GeV pT?

to_process = []

if os.path.isdir(args.inputFile):
  for r, d, f in os.walk(args.inputFile):
    for file in f:
      to_process.append(os.path.join(r, file))
else:
  to_process.append(args.inputFile)

#SiTrackContainer = "SiTracks"
SiTrackContainer = "SiTracks_Refitted"
print("Reading", SiTrackContainer, "as the track container!")
counter = 0

# Open input file(s)
for file in to_process:
  reader = IOIMPL.LCFactory.getInstance().createLCReader()
  reader.open(file)

  # Loop through Events
  for ievt, event in enumerate(reader):
    counter += 1
    # if counter > 5:
    #    break
    mc_pis = []
    reco_pis = []
    pfo_pi_trks = []
    pfo_w_trks = []
    
    mc_particles = event.getCollection('MCParticle')
    my_clusters = event.getCollection('PandoraClusters')
    pfos = event.getCollection('PandoraPFOs')
    my_tracks = event.getCollection(SiTrackContainer)

    nClusters.Fill(len(my_clusters))
    nPFOs.Fill(len(pfos))
    
    # quick sanity check
    if len(my_clusters) == 0:
      print("There are no clusters in an event!")
      #exit()

    check_centrality = []

    # Loop over MC
    for mcp in mc_particles:
        p = mcp.getMomentum()
        px = p[0]
        py = p[1]
        pz = p[2]
        phi = get_phi(px,py)
        theta = get_theta(px,py,pz)
        pt = math.sqrt(px**2 + py**2)

        if abs(mcp.getPDG()) == 211:
          mc_pis.append(mcp)

    # the generated pion is always the first one - this has been confirmed
    piE = mc_pis[0].getEnergy() 
    p = mc_pis[0].getMomentum()
    px = p[0]
    py = p[1]
    pz = p[2]
    ptMCPion = math.sqrt(px**2 + py**2)
    phiMCPion = get_phi(px,py)
    thetaMCPion = get_theta(px,py,pz)

    # enforcing a theta region
    
    if thetaMCPion <= 1 or thetaMCPion >= 2: # Corresponds to central barrel region, from MAIA paper photon results.
      check_centrality.append(1)
      continue

    # to skip over events with > 1 trk (TODO: Add proper truth matching.)
    nChargedPFOCounter = 0
    chargedE = 0
    neutralE = 0
    found_pion = 0

    # Loop over PFOs 
    for pfo in pfos:
      pfoPDG.Fill(pfo.getType())
      if len(pfo.getTracks()) == 1:
        # print(len(pfo.getClusters()), pfo.getClusters()[0].getEnergy())
        nChargedPFOCounter += 1
        pfo_w_trks.append(pfo)
        p = pfo.getMomentum()
        px = p[0]
        py = p[1]
        pz = p[2]
        phiPFO = get_phi(px,py)
        thetaPFO = get_theta(px,py,pz)
        ptPFO = math.sqrt(px**2 + py**2)

         # Filling this with the MC pion pt - TODO: Add proper truth matching.
        if abs(pfo.getType()) == 211:
          fRecoPiPt.Fill(ptMCPion)
          fRecoPiTheta.Fill(thetaMCPion)
          fRecoPiPhi.Fill(phiMCPion)
          found_pion = 1

        # I'd be surprised if a charged particle is being tagged by anything but a charged pion or electron
        if abs(pfo.getType()) != 211 and abs(pfo.getType()) != 11:
          print("Reconstructed particle with a track isn't an electron or a pion")
          if abs(pfo.getType()) == 13:
            print("It's a muon.")
          else:
            print("It has pdg ID: ", pfo.getType())
            print("Exiting so that you can think")
            exit()

        # Filling the charged momentum as that from the track 
        pfosTrk = pfo.getTracks()[0] 
        omegaNF, tan_lambdaNF, phiNF = (
            pfosTrk.getOmega(), #signed curvature of track in 1/mm
            pfosTrk.getTanLambda(), #"dip angle" in r-z at reference point
            pfosTrk.getPhi(),
            )
  
        ptNF = BFIELD * FACTOR / abs(omegaNF)
        pzNF = ptNF * tan_lambdaNF
        pNF = math.sqrt(ptNF * ptNF + pzNF * pzNF)

        # Approximating that pions and electrons are massless: E = p.
        chargedE += pNF
    
      if len(pfo.getTracks()) == 0:
        neutralE += pfo.getEnergy()

    totalE = chargedE + neutralE 
    if nChargedPFOCounter == 0:
      jetLikeE.Fill(totalE)
      jetLikeERatio.Fill(totalE / piE)

    # wasteful second loop over pfos in case of mis-ID
    if nChargedPFOCounter == 1 and found_pion == 0:
      for pfo in pfos:
        pfoPDGMisID.Fill(pfo.getType())



    if nChargedPFOCounter > 1:
      print("More than one charged PFO. Skipping this event.")
      continue

    # print("Charged energy: ", chargedE)
    # print("Neutral energy: ", neutralE)
    # print("MC Pion Energy: ", piE)
    # print("Event number: ", counter)
    # print(" ")

  reader.close()


######################################################################################################
myCanvas = TCanvas("scoobyDoo", "Canvas", 800, 600)
myCanvas.SetFrameLineWidth(2)

for hist in hists:
  filename = hist.GetTitle() + '.png'
  canvas = TCanvas()
  hist.Draw("E1")
  canvas.SaveAs(filename)
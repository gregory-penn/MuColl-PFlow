from pyLCIO import IOIMPL, EVENT, UTIL
from ROOT import TH1F, TFile, TCanvas, gStyle, TLegend, TLatex
from argparse import ArgumentParser
import os
import math

# Command line arguments
parser = ArgumentParser()

BFIELD = 5.0 # Taking 5 T for MAIA and 3.57 T for MuColl_v1. I think this is correct?
FACTOR = 3e-4 #some conversion factor to take T calculation to GeV pT?


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

#helper functions for calculating theta and phi
def get_theta(px, py, pz):
    pt = math.sqrt(px**2 + py**2)
    return math.atan2(pt, pz)

def get_phi(px, py):
    return math.atan2(py, px)

geo_label = TLatex()
geo_label.SetNDC()
geo_label.SetTextSize(0.04)

gen_label = TLatex()
gen_label.SetNDC()
gen_label.SetTextSize(0.03)

hists = []

fCls1VsPiEn = TH1F('ratio of cluster 1 and pion energy', 'ClsVsPiEnergy', 28, 0, 1.4)
fCls1VsPiEn.SetXTitle('E^{cluster} / E^{\pi^{-}}')
fCls1VsPiEn.SetMinimum(0.0)
fCls1VsPiEn.SetMaximum(500.0)
pl1Color = 30
fCls1VsPiEn.SetLineColor(pl1Color);
fCls1VsPiEn.SetLineWidth(2)
fCls1VsPiEn.SetMarkerStyle(8)
fCls1VsPiEn.SetMarkerColor(pl1Color)
fCls1VsPiEn.GetYaxis().SetTitle("Entries")

fCls2VsPiEn = TH1F('ratio of cluster 2 and pion energy', 'ClsVsPiEnergy', 28, 0, 1.4)
fCls2VsPiEn.SetXTitle('E^{cluster} / E^{\pi^{-}}')
fCls2VsPiEn.SetMinimum(0.0)
fCls2VsPiEn.SetMaximum(500.0)
pl2Color = 46
fCls2VsPiEn.SetLineColor(pl2Color);
fCls2VsPiEn.SetLineWidth(2)
fCls2VsPiEn.SetMarkerStyle(8)
fCls2VsPiEn.SetMarkerColor(pl2Color)
fCls2VsPiEn.GetYaxis().SetTitle("Entries")

fCls3VsPiEn = TH1F('ratio of cluster 3 and pion energy', 'ClsVsPiEnergy', 28, 0, 1.4)
fCls3VsPiEn.SetXTitle('E^{cluster} / E^{\pi^{-}}')
fCls3VsPiEn.SetMinimum(0.0)
fCls3VsPiEn.SetMaximum(500.0)
pl3Color = 38
fCls3VsPiEn.SetLineColor(pl3Color);
fCls3VsPiEn.SetLineWidth(2)
fCls3VsPiEn.SetMarkerStyle(8)
fCls3VsPiEn.SetMarkerColor(pl3Color)
fCls3VsPiEn.GetYaxis().SetTitle("Entries")

fNClusters = TH1F('number of clusters', 'nClusters', 9, 0, 9)
fNClusters.SetXTitle('n_{clusters}')
fNClusters.SetMinimum(0.0)
#fNClusters.SetMaximum(650.0)
fNClusters.SetLineColor(1);
fNClusters.SetLineWidth(2)
fNClusters.SetMarkerStyle(8)
fNClusters.SetMarkerColor(1)
fNClusters.GetYaxis().SetTitle("Entries")
hists.append(fNClusters)

fRatioTrkMCPionPt = TH1F('ratio of track and mc pion pt', 'TrkVsMCPionPt', 20, 0, 3.0)
fRatioTrkMCPionPt.SetXTitle('p_{T}^{trk} / p_{T}^{\pi truth}')
fRatioTrkMCPionPt.SetMinimum(0.0)
#fRatioTrkMCPionPt.SetMaximum(400.0)
fRatioTrkMCPionPt.SetLineColor(pl3Color);
fRatioTrkMCPionPt.SetLineWidth(2)
fRatioTrkMCPionPt.SetMarkerStyle(8)
fRatioTrkMCPionPt.SetMarkerColor(pl3Color)
fRatioTrkMCPionPt.GetYaxis().SetTitle("Entries")
hists.append(fRatioTrkMCPionPt)

fRatioTrkMCPionPt280= TH1F('ratio of track and mc pion pt, w/ trk p_{T} > 280 GeV', 'TrkVsMCPionPt280', 20, 0, 3.0)
fRatioTrkMCPionPt280.SetXTitle('p_{T}^{trk} / p_{T}^{\pi truth}')
fRatioTrkMCPionPt280.SetMinimum(0.0)
#fRatioTrkMCPionPt280.SetMaximum(400.0)
fRatioTrkMCPionPt280.SetLineColor(pl3Color);
fRatioTrkMCPionPt280.SetLineWidth(2)
fRatioTrkMCPionPt280.SetMarkerStyle(8)
fRatioTrkMCPionPt280.SetMarkerColor(pl3Color)
fRatioTrkMCPionPt280.GetYaxis().SetTitle("Entries")
hists.append(fRatioTrkMCPionPt280)

fTrkThetaRes = TH1F('difference between track and mc pion theta', 'TrkThetaRes', 20, -2.0, 2.0)
fTrkThetaRes.SetXTitle('#theta^{trk} - #theta{\pi truth}')
fTrkThetaRes.SetMinimum(0.0)
#fTrkThetaRes.SetMaximum(400.0)
fTrkThetaRes.SetLineColor(pl3Color);
fTrkThetaRes.SetLineWidth(2)
fTrkThetaRes.SetMarkerStyle(8)
fTrkThetaRes.SetMarkerColor(pl3Color)
fTrkThetaRes.GetYaxis().SetTitle("Entries")
hists.append(fTrkThetaRes)

fTrkPhiRes = TH1F('difference between track and mc pion phi', 'TrkPhiRes', 20, -2.0, 2.0)
fTrkPhiRes.SetXTitle('#phi^{trk} - #phi{\pi truth}')
fTrkPhiRes.SetMinimum(0.0)
#fTrkPhiRes.SetMaximum(400.0)
fTrkPhiRes.SetLineColor(pl3Color);
fTrkPhiRes.SetLineWidth(2)
fTrkPhiRes.SetMarkerStyle(8)
fTrkPhiRes.SetMarkerColor(pl3Color)
fTrkPhiRes.GetYaxis().SetTitle("Entries")
hists.append(fTrkPhiRes)


nRecoPion1Cls = TH1F('number of reco pions, events with 1 cluster', 'nPions1Cls', 5, 0, 5)
nRecoPion1Cls.SetXTitle('# of Reco Pions')
nRecoPion1Cls.SetMinimum(0.0)
nRecoPion1Cls.SetMaximum(550.0)
nRecoPion1Cls.SetLineColor(pl1Color);
nRecoPion1Cls.SetLineWidth(2)
nRecoPion1Cls.SetMarkerStyle(8)
nRecoPion1Cls.SetMarkerColor(pl1Color)
nRecoPion1Cls.GetYaxis().SetTitle("Entries")

nRecoPion2Cls = TH1F('number of reco pions, events with 2 clusters', 'nPions2Cls', 5, 0, 5)
nRecoPion2Cls.SetXTitle('# of Reco Pions')
nRecoPion2Cls.SetMinimum(0.0)
nRecoPion2Cls.SetMaximum(550.0)
nRecoPion2Cls.SetLineColor(pl2Color);
nRecoPion2Cls.SetLineWidth(2)
nRecoPion2Cls.SetMarkerStyle(8)
nRecoPion2Cls.SetMarkerColor(pl2Color)
nRecoPion2Cls.GetYaxis().SetTitle("Entries")

nRecoPion3Cls = TH1F('number of reco pions, events with 3 clusters', 'nPions3Cls', 5, 0, 5)
nRecoPion3Cls.SetXTitle('# of Reco Pions')
nRecoPion3Cls.SetMinimum(0.0)
nRecoPion2Cls.SetMaximum(550.0)
nRecoPion3Cls.SetLineColor(pl3Color);
nRecoPion3Cls.SetLineWidth(2)
nRecoPion3Cls.SetMarkerStyle(8)
nRecoPion3Cls.SetMarkerColor(pl3Color)
nRecoPion3Cls.GetYaxis().SetTitle("Entries")

nTrkRecoPion = TH1F('number of tracks per reco pion', 'nTrkPerRecoPion', 5, 0, 5)
nTrkRecoPion.SetXTitle('# of Tracks')
nTrkRecoPion.SetMinimum(0.0)
nTrkRecoPion.SetMaximum(550.0)
nTrkRecoPion.SetLineColor(pl3Color);
nTrkRecoPion.SetLineWidth(2)
nTrkRecoPion.SetMarkerStyle(8)
nTrkRecoPion.SetMarkerColor(pl3Color)
nTrkRecoPion.GetYaxis().SetTitle("Entries")

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

nMCPis = TH1F('number of MC Pis', 'nMCPis', 5, 0, 5)
nMCPis.SetXTitle('# of MC Charged Pions')
nMCPis.SetMinimum(0.0)
#nMCPis.SetMaximum(550.0)
nMCPis.SetLineColor(pl1Color);
nMCPis.SetLineWidth(2)
nMCPis.SetMarkerStyle(8)
nMCPis.SetMarkerColor(pl1Color)
nMCPis.GetYaxis().SetTitle("Entries")
hists.append(nMCPis)

nTrks = TH1F('number of tracks', 'nTrks', 5, 0, 5)
nTrks.SetXTitle('# of Tracks')
nTrks.SetMinimum(0.0)
#nTrks.SetMaximum(550.0)
nTrks.SetLineColor(pl1Color);
nTrks.SetLineWidth(2)
nTrks.SetMarkerStyle(8)
nTrks.SetMarkerColor(pl1Color)
nTrks.GetYaxis().SetTitle("Entries")
hists.append(nTrks)

nTrk1PFO = TH1F('number of tracks for 1 PFO', 'nTrk1PFO', 5, 0, 5)
nTrk1PFO.SetXTitle('# of tracks associated to all clusters')
nTrk1PFO.SetMinimum(0.0)
nTrk1PFO.SetMaximum(550.0)
nTrk1PFO.SetLineColor(pl1Color);
nTrk1PFO.SetLineWidth(2)
nTrk1PFO.SetMarkerStyle(8)
nTrk1PFO.SetMarkerColor(pl1Color)
nTrk1PFO.GetYaxis().SetTitle("Entries")
hists.append(nTrk1PFO)

nTrk2PFO = TH1F('number of tracks for 2 PFOs', 'nTrk2PFOs', 5, 0, 5)
nTrk2PFO.SetXTitle('# of tracks associated to all clusters')
nTrk2PFO.SetMinimum(0.0)
nTrk2PFO.SetMaximum(550.0)
nTrk2PFO.SetLineColor(pl2Color);
nTrk2PFO.SetLineWidth(2)
nTrk2PFO.SetMarkerStyle(8)
nTrk2PFO.SetMarkerColor(pl2Color)
nTrk2PFO.GetYaxis().SetTitle("Entries")
hists.append(nTrk2PFO)

nTrk3PFO = TH1F('number of tracks for 3 PFOs', 'nTrk3PFOs', 5, 0, 5)
nTrk3PFO.SetXTitle('# of tracks associated to all clusters')
nTrk3PFO.SetMinimum(0.0)
nTrk3PFO.SetMaximum(550.0)
nTrk3PFO.SetLineColor(pl3Color);
nTrk3PFO.SetLineWidth(2)
nTrk3PFO.SetMarkerStyle(8)
nTrk3PFO.SetMarkerColor(pl3Color)
nTrk3PFO.GetYaxis().SetTitle("Entries")
hists.append(nTrk3PFO)

fSiTrkPtNoFake = TH1F('track p_{T}', 'TrackPtNoFake', 10, 0, 1000)
fSiTrkPtNoFake.SetXTitle('track p_{T} (GeV)')
fSiTrkPtNoFake.SetMinimum(0.0)
fSiTrkPtNoFake.GetYaxis().SetTitle("Entries")
hists.append(fSiTrkPtNoFake)

fSiTrkThetaNoFake = TH1F('track theta', 'TrackThetaNoFake', 10, 0, 3.14159)
fSiTrkThetaNoFake.SetXTitle('track #theta (rad)')
fSiTrkThetaNoFake.SetMinimum(0.0)
fSiTrkThetaNoFake.GetYaxis().SetTitle("Entries")
hists.append(fSiTrkThetaNoFake)

fSiTrkPhiNoFake = TH1F('track phi', 'TrackPhiNoFake', 10, -3.14159, 3.14159)
fSiTrkPhiNoFake.SetXTitle('track #phi (rad)')
fSiTrkPhiNoFake.SetMinimum(0.0)
fSiTrkPhiNoFake.GetYaxis().SetTitle("Entries")
hists.append(fSiTrkPhiNoFake)

fMCPiE = TH1F('mc_pi_E', 'MCPionE', 10, 0, 1000)
fMCPiE.SetXTitle('Truth Charged Pion E (GeV)')
fMCPiE.SetMinimum(0.0)
fMCPiE.GetYaxis().SetTitle("Entries")

fMCPiPt = TH1F('mc_pi_pt', 'MCPionPt', 10, 0, 1000)
fMCPiPt.SetXTitle('Truth Charged Pion p_{T} (GeV)')
fMCPiPt.SetMinimum(0.0)
fMCPiPt.GetYaxis().SetTitle("Entries")
hists.append(fMCPiPt)

fMCPiTheta = TH1F('mc_pi_theta', 'MCPionTheta', 20, 0, 3.14159)
fMCPiTheta.SetXTitle('Truth Charged Pion #theta (rad)')
fMCPiTheta.SetMinimum(0.0)
fMCPiTheta.GetYaxis().SetTitle("Entries")
hists.append(fMCPiTheta)

fMCPiPhi = TH1F('mc_pi_phi', 'MCPionPhi', 20, -3.14159, 3.14159)
fMCPiPhi.SetXTitle('Truth Charged Pion #phi (rad)')
fMCPiPhi.SetMinimum(0.0)
fMCPiPhi.GetYaxis().SetTitle("Entries")
hists.append(fMCPiPhi)

nRecoPFOwTrk = TH1F('PFO_trk', 'PFO_trk', 5, 0, 5)
nRecoPFOwTrk.SetXTitle('Number of PFOs with tracks')
nRecoPFOwTrk.SetMinimum(0.0)
nRecoPFOwTrk.GetYaxis().SetTitle("Entries")
hists.append(nRecoPFOwTrk)

fPFOwTrkPt = TH1F('PFOwTrkPt', 'PFOwTrkPt', 10, 0, 1000)
fPFOwTrkPt.SetXTitle('p_{T} of PFOs w/ trks (GeV)')
fPFOwTrkPt.SetMinimum(0.0)
fPFOwTrkPt.GetYaxis().SetTitle("Entries")
hists.append(fPFOwTrkPt)

fPFOwTrkTheta = TH1F('PFOwTrkTheta', 'PFOwTrkTheta', 20, 0, 3.14159)
fPFOwTrkTheta.SetXTitle('#theta of PFOs w/ trks (rad)')
fPFOwTrkTheta.SetMinimum(0.0)
fPFOwTrkTheta.GetYaxis().SetTitle("Entries")
hists.append(fPFOwTrkTheta)

fPFOwTrkPhi = TH1F('PFOwTrkPhi', 'PFOwTrkPhi', 20, -3.14159, 3.14159)
fPFOwTrkPhi.SetXTitle('#phi of PFOs w/ trks (GeV)')
fPFOwTrkPhi.SetMinimum(0.0)
fPFOwTrkPhi.GetYaxis().SetTitle("Entries")
hists.append(fPFOwTrkPhi)

nRecoPerPFOwTrk = TH1F('nPions', 'nPions', 5, 0, 5)
nRecoPerPFOwTrk.SetXTitle('Number of Reco Pions')
nRecoPerPFOwTrk.SetMinimum(0.0)
nRecoPerPFOwTrk.GetYaxis().SetTitle("Entries")
hists.append(nRecoPerPFOwTrk)

fRecoPiPt = TH1F('RecoPiPt', 'RecoPiPt', 10, 0, 1000)
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

#plots for creating efficiency plots, without the effects of poor resolution
fMCPiWTrkPt = TH1F('MCPiwTrkPt', 'MCPiwTrkPt', 10, 0, 1000)
fMCPiWTrkPt.SetXTitle('Truth Charged Pion p_{T}')
fMCPiWTrkPt.SetMinimum(0.0)
#fMCPiWTrkPt.SetMaximum(550.0)
# fMCPiWTrkPt.SetLineColor(pl1Color);
# fMCPiWTrkPt.SetLineWidth(2)
# fMCPiWTrkPt.SetMarkerStyle(8)
# fMCPiWTrkPt.SetMarkerColor(pl1Color)
fMCPiWTrkPt.GetYaxis().SetTitle("Entries")
hists.append(fMCPiWTrkPt)

fMCPiWTrkTheta = TH1F('MCPiwTrkTheta', 'MCPiwTrkTheta', 20, 0, 3.14159)
fMCPiWTrkTheta.SetXTitle('Truth Charged Pion #theta (rad)')
fMCPiWTrkTheta.SetMinimum(0.0)
#fMCPiWTrkTheta.SetMaximum(550.0)
# fMCPiWTrkTheta.SetLineColor(pl2Color);
# fMCPiWTrkTheta.SetLineWidth(2)
# fMCPiWTrkTheta.SetMarkerStyle(8)
# fMCPiWTrkTheta.SetMarkerColor(pl2Color)
fMCPiWTrkTheta.GetYaxis().SetTitle("Entries")
hists.append(fMCPiWTrkTheta)

fMCPiWTrkPhi = TH1F('MCPiwTrkPhi', 'MCPiwTrkPhi', 20, -3.14159, 3.14159)
fMCPiWTrkPhi.SetXTitle('Truth Charged Pion #phi (rad)')
fMCPiWTrkPhi.SetMinimum(0.0)
#fMCPiWTrkPhi.SetMaximum(550.0)
# fMCPiWTrkPhi.SetLineColor(pl2Color);
# fMCPiWTrkPhi.SetLineWidth(2)
# fMCPiWTrkPhi.SetMarkerStyle(8)
# fMCPiWTrkPhi.SetMarkerColor(pl2Color)
fMCPiWTrkPhi.GetYaxis().SetTitle("Entries")
hists.append(fMCPiWTrkPhi)

fChi2pDOFTrk = TH1F('Chi2pDOFTrk', 'Chi2pDOFTrk', 10, 0.0, 3.0)
fChi2pDOFTrk.SetXTitle('Track #chi^{2}/n_{dof}')
fChi2pDOFTrk.SetMinimum(0.0)
#fChi2pDOFTrk.SetMaximum(550.0)
# fChi2pDOFTrk.SetLineColor(pl2Color);
# fChi2pDOFTrk.SetLineWidth(2)
# fChi2pDOFTrk.SetMarkerStyle(8)
# fChi2pDOFTrk.SetMarkerColor(pl2Color)
fChi2pDOFTrk.GetYaxis().SetTitle("Entries")
hists.append(fChi2pDOFTrk)

fnHitsTrk = TH1F('nHitsTrk', 'nHitsTrk', 20, 0, 20)
fnHitsTrk.SetXTitle('Track n_{hits}')
fnHitsTrk.SetMinimum(0.0)
#fnHitsTrk.SetMaximum(550.0)
# fnHitsTrk.SetLineColor(pl2Color);
# fnHitsTrk.SetLineWidth(2)
# fnHitsTrk.SetMarkerStyle(8)
# fnHitsTrk.SetMarkerColor(pl2Color)
fnHitsTrk.GetYaxis().SetTitle("Entries")
hists.append(fnHitsTrk)

eRes = TH1F('eRes', 'eRes', 50, -1.5, 1.5)
eRes.SetXTitle('(E^{calo}_{reco} - E_{truth}) / E_{truth}')
eRes.SetMinimum(0.0)
# eRes.SetMaximum(550.0)
eRes.SetLineColor(pl2Color);
eRes.SetLineWidth(2)
# eRes.SetMarkerStyle(8)
# eRes.SetMarkerColor(pl2Color)
eRes.GetYaxis().SetTitle("Entries")
hists.append(eRes)

def getSigmaPOverP(track):
      wResStdDev = my_tracks[0].getCovMatrix()[5]
      tLResStdDev = my_tracks[0].getCovMatrix()[14]
      wtLRes = my_tracks[0].getCovMatrix()[12]
      omegaNF, tan_lambdaNF = (
            my_tracks[0].getOmega(), #signed curvature of track in 1/mm
            my_tracks[0].getTanLambda(), #"dip angle" in r-z at reference point
            )
      ptNF = BFIELD * FACTOR / abs(omegaNF)
      pzNF = ptNF * tan_lambdaNF
      pNF = math.sqrt(ptNF * ptNF + pzNF * pzNF)
      partialPOverWSquared = 1 / (omegaNF**4) * (1 + tan_lambdaNF**2)
      partialPOvertLSquared = tan_lambdaNF**2/(omegaNF**2 * (1 + tan_lambdaNF**2))

      sigmaPOverP = BFIELD * FACTOR / pNF * math.sqrt(
         partialPOverWSquared * wResStdDev + 
         partialPOvertLSquared * tLResStdDev + 
         2 * math.sqrt(partialPOverWSquared * partialPOvertLSquared) * wtLRes)

      print("\n")
      print("track sigma(p)/p is: ", sigmaPOverP)
      return(sigmaPOverP)
   


######################################################################################################

to_process = []
test1 = 0
test2 = 0
totalMCPis = 0
totalTrks = 0

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
    test1 += 1
    mc_pis = []
    reco_pis = []
    pfo_pi_trks = []
    pfo_w_trks = []
    
    mc_particles = event.getCollection('MCParticle')
    my_cluster = event.getCollection('PandoraClusters')
    pfos = event.getCollection('PandoraPFOs')
    my_tracks = event.getCollection(SiTrackContainer)

    # quick sanity check
    # if len(my_cluster) == 0:
    #   print("There are no clusters in an event!")
      #exit()

    nPFOs.Fill(len(pfos))

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



    # Performing sanity checks early on
    # if len(mc_pis) == 0:
       # print("Error! There are 0 MC pions in event: ", test1)
       #exit()

    totalMCPis += 1

    nMCPis.Fill(len(mc_pis))
    # the generated pion is always the first one - this has been confirmed
    piE = mc_pis[0].getEnergy() 
    p = mc_pis[0].getMomentum()
    px = p[0]
    py = p[1]
    pz = p[2]
    ptMCPion = math.sqrt(px**2 + py**2)
    phiMCPion = get_phi(px,py)
    thetaMCPion = get_theta(px,py,pz)

    # if thetaMCPion < .698 or thetaMCPion > 2.44: # barrel region: 40 to 140 degrees / .698 to 2.44 rad. Central barrel: 1 to 2 rad.
    #   check_centrality.append(1)
    #   continue
    # test2 += 1

    fNClusters.Fill(len(my_cluster))

    fMCPiE.Fill(piE)
    fMCPiPt.Fill(ptMCPion)
    fMCPiTheta.Fill(thetaMCPion)
    fMCPiPhi.Fill(phiMCPion)
    
    #filling in tracking efficiency plots: fill if there's a track, don't fill else
    if len(my_tracks) > 0:
       fMCPiWTrkPt.Fill(ptMCPion)
       fMCPiWTrkTheta.Fill(thetaMCPion)
       fMCPiWTrkPhi.Fill(phiMCPion)
      
    # if len(pfos) == 3:
    #    nTrk3PFO.Fill( len(pfos[0].getTracks()) + len(pfos[1].getTracks()) + len(pfos[2].getTracks()) )
    # elif len(pfos) == 2:
    #    nTrk2PFO.Fill( len(pfos[0].getTracks()) + len(pfos[1].getTracks()) )
    # elif len(pfos) == 1:
    #    nTrk1PFO.Fill( len(pfos[0].getTracks()) )    

    # for keeping track of how many PFOs with tracks there are - to avoid counting 2 in one event as double efficiency
    nPFOwithTracks = 0             
    pfoCalE = 0
    foundMCPion = 0

    # Loop over PFOs 
    for pfo in pfos:
      pfo_clusters = pfo.getClusters()
      if len(pfo.getTracks()) == 1:
         nPFOwithTracks += 1
         pfo_w_trks.append(pfo)
         nRecoPFOwTrk.Fill(1)
         p = pfo.getMomentum()
         px = p[0]
         py = p[1]
         pz = p[2]
         phiPFO = get_phi(px,py)
         thetaPFO = get_theta(px,py,pz)
         ptPFO = math.sqrt(px**2 + py**2)

         # WARNING: THESE PLOTS ARE FILLES WITH THE PT OF THE MC PION FOR EFFICIENCY PLOTS! NEED BETTER WORKAROUND.
         # just count PFO w track once per event
         if nPFOwithTracks == 1:
           fPFOwTrkPt.Fill(ptMCPion)
           fPFOwTrkPhi.Fill(phiMCPion) #
           fPFOwTrkTheta.Fill(thetaMCPion)

           if abs(pfo.getType()) == 211:
            #  print("There's a charged pion in here!")
             foundMCPion = 1
             nRecoPerPFOwTrk.Fill(1)
             fRecoPiPt.Fill(ptMCPion)
             fRecoPiTheta.Fill(thetaMCPion)
             fRecoPiPhi.Fill(phiMCPion)
             for pfoCls in pfo_clusters:
                pfoCalE += pfoCls.getEnergy()

    if foundMCPion: 
      tempEres = (pfoCalE - ptMCPion) / ptMCPion
      eRes.Fill(tempEres)
      # if tempEres < -.99:
      #   print(tempEres)
      #   print(pfoCalE)
      #   print(ptMCPion)
      #   print("nPfos: ", len(pfos))
      

    if not pfo_w_trks: #if list is empty
       nRecoPFOwTrk.Fill(0)        

    if len(my_cluster) == 1:
        fCls1VsPiEn.Fill(my_cluster[0].getEnergy() / piE)
        nRecoPion1Cls.Fill(len(reco_pis))

    elif len(my_cluster) == 2:
        nRecoPion2Cls.Fill(len(reco_pis))
        for cluster in my_cluster:
            fCls2VsPiEn.Fill(cluster.getEnergy() / piE)

    # elif len(my_cluster) == 3:
    #     nRecoPion3Cls.Fill(len(reco_pis))
    #     for cluster in my_cluster:
    #         fCls3VsPiEn.Fill(cluster.getEnergy()/ piE)

    # tracking plots are removed. I have a different script for that in trackPlots.


  reader.close()


######################################################################################################
myCanvas = TCanvas("scoobyDoo", "Canvas", 800, 600)
myCanvas.SetFrameLineWidth(2)

fCls1VsPiEn.Draw("E")
fCls2VsPiEn.Draw("E SAME")
fCls3VsPiEn.Draw("E SAME")

legend = TLegend(0.7, 0.7, 0.89, 0.89)
legend.AddEntry(fCls1VsPiEn, "1 cluster", "lep")
legend.AddEntry(fCls2VsPiEn, "2 clusters", "lep")
legend.AddEntry(fCls3VsPiEn, "3 clusters", "lep")
legend.SetBorderSize(0)
legend.Draw()

myCanvas.Update()
myCanvas.SaveAs("e_ratio.png")

myCanvas2 = TCanvas("scoobyDoo2", "Canvas", 800, 600)
myCanvas2.SetFrameLineWidth(2)

nRecoPion1Cls.Draw("E")
nRecoPion2Cls.Draw("E SAME")
nRecoPion3Cls.Draw("E SAME")

legend.Draw()

myCanvas2.Update()
myCanvas2.SaveAs("n_reco_pions.png")

myCanvas3 = TCanvas("scoobyDoo3", "Canvas", 800, 600)
myCanvas3.SetFrameLineWidth(2)

nTrk1PFO.Draw("E")
nTrk2PFO.Draw("E SAME")
nTrk3PFO.Draw("E SAME")

legend.Draw()

myCanvas3.Update()
myCanvas3.SaveAs("n_trk_per_cluster.png")

# Tracking efficiency plots
fTrkPtEff = fMCPiWTrkPt.Clone('pi_eff')
fTrkPtEff.Divide(fTrkPtEff, fMCPiPt, 1, 1, 'B')
fTrkPtEff.SetLineColor(pl1Color)
fTrkPtEff.SetLineWidth(3)
fTrkPtEff.SetTitle('TrackEfficiencyVsPt')
fTrkPtEff.SetMarkerStyle(21)
fTrkPtEff.SetMarkerColor(pl1Color)
fTrkPtEff.GetXaxis().SetTitle('Truth Charged Pion p_{T} (GeV)')
fTrkPtEff.GetYaxis().SetTitle("Efficiency")
fTrkPtEff.SetMinimum(0.0)
fTrkPtEff.SetMaximum(1.4)

fTrkThetaEff = fMCPiWTrkTheta.Clone('pi_eff')
fTrkThetaEff.Divide(fTrkThetaEff, fMCPiTheta, 1, 1, 'B')
fTrkThetaEff.SetLineColor(pl1Color)
fTrkThetaEff.SetLineWidth(2)
fTrkThetaEff.SetTitle('TrackEfficiencyVsTheta')
fTrkThetaEff.SetMarkerStyle(21)
fTrkThetaEff.SetMarkerColor(pl1Color)
fTrkThetaEff.GetXaxis().SetTitle('Truth Charged Pion #theta (rad)')
fTrkThetaEff.GetYaxis().SetTitle("Efficiency")
fTrkThetaEff.SetMinimum(0.0)
fTrkThetaEff.SetMaximum(1.4)

fTrkPhiEff = fMCPiWTrkPhi.Clone('pi_eff')
fTrkPhiEff.Divide(fTrkPhiEff, fMCPiPhi, 1, 1, 'B')
fTrkPhiEff.SetLineColor(pl1Color)
fTrkPhiEff.SetTitle('TrackEfficiencyVsPhi')
fTrkPhiEff.SetMarkerStyle(21)
fTrkPhiEff.SetMarkerColor(pl1Color)
fTrkPhiEff.GetXaxis().SetTitle('Truth Charged Pion #phi (rad)')
fTrkPhiEff.GetYaxis().SetTitle("Efficiency")
fTrkPhiEff.SetMinimum(0.0)
fTrkPhiEff.SetMaximum(1.4)

# Duplicate for individual plotting... want different y-titles. Ugly hack.
fTrkPtEffDupe = fMCPiWTrkPt.Clone('pi_eff')
fTrkPtEffDupe.Divide(fTrkPtEffDupe, fMCPiPt, 1, 1, 'B')
fTrkPtEffDupe.SetLineColor(1)
fTrkPtEffDupe.SetLineWidth(3)
fTrkPtEffDupe.SetTitle('TrackEfficiencyVsPt')
fTrkPtEffDupe.SetMarkerStyle(22)
fTrkPtEffDupe.SetMarkerColor(1)
fTrkPtEffDupe.GetXaxis().SetTitle('Truth Charged Pion p_{T} (GeV)')
fTrkPtEffDupe.GetYaxis().SetTitle("Tracking Efficiency")
fTrkPtEffDupe.SetMinimum(0.0)
fTrkPtEffDupe.SetMaximum(1.4)
hists.append(fTrkPtEffDupe)

fTrkThetaEffDupe = fMCPiWTrkTheta.Clone('pi_eff')
fTrkThetaEffDupe.Divide(fTrkThetaEffDupe, fMCPiTheta, 1, 1, 'B')
fTrkThetaEffDupe.SetLineColor(1)
fTrkThetaEffDupe.SetTitle('TrackEfficiencyVsTheta')
fTrkThetaEffDupe.SetMarkerStyle(22)
fTrkThetaEffDupe.SetMarkerColor(1)
fTrkThetaEffDupe.GetXaxis().SetTitle('Truth Charged Pion #theta (rad)')
fTrkThetaEffDupe.GetYaxis().SetTitle("Tracking Efficiency")
fTrkThetaEffDupe.SetMinimum(0.0)
fTrkThetaEffDupe.SetMaximum(1.4)
hists.append(fTrkThetaEffDupe)

fTrkPhiEffDupe = fMCPiWTrkPhi.Clone('pi_eff')
fTrkPhiEffDupe.Divide(fTrkPhiEffDupe, fMCPiPhi, 1, 1, 'B')
fTrkPhiEffDupe.SetLineColor(1)
fTrkPhiEffDupe.SetTitle('TrackEfficiencyVsPhi')
fTrkPhiEffDupe.SetMarkerStyle(22)
fTrkPhiEffDupe.SetMarkerColor(1)
fTrkPhiEffDupe.GetXaxis().SetTitle('Truth Charged Pion #phi (rad)')
fTrkPhiEffDupe.GetYaxis().SetTitle("Tracking Efficiency")
fTrkPhiEffDupe.SetMinimum(0.0)
fTrkPhiEffDupe.SetMaximum(1.4)
hists.append(fTrkPhiEffDupe)

# Create pi ID, given PFO with track plot
fPiEffPt = fRecoPiPt.Clone('pi_eff')
fPiEffPt.Divide(fPiEffPt, fPFOwTrkPt, 1, 1, 'B')
fPiEffPt.SetLineColor(pl2Color)
fPiEffPt.SetLineWidth(3)
fPiEffPt.SetTitle('ChargedPionEffVsPt')
fPiEffPt.SetMarkerStyle(22)
fPiEffPt.SetMarkerColor(pl2Color)
fPiEffPt.GetXaxis().SetTitle('Truth p_{T} (GeV)')
fPiEffPt.GetYaxis().SetTitle("Efficiency")
fPiEffPt.SetMinimum(0.0)
fPiEffPt.SetMaximum(1.4)
hists.append(fPiEffPt)

fPiEffTheta = fRecoPiTheta.Clone('pi_eff')
fPiEffTheta.Divide(fPiEffTheta, fPFOwTrkTheta, 1, 1, 'B')
fPiEffTheta.SetLineColor(pl2Color)
fPiEffTheta.SetLineWidth(2)
fPiEffTheta.SetTitle('ChargedPionEffVsTheta')
fPiEffTheta.SetMarkerStyle(22)
fPiEffTheta.SetMarkerColor(pl2Color)
fPiEffTheta.GetXaxis().SetTitle('PFO (w/ trk) #theta (rad)')
fPiEffTheta.GetYaxis().SetTitle("Efficiency")
fPiEffTheta.SetMinimum(0.0)
fPiEffTheta.SetMaximum(1.4)
hists.append(fPiEffTheta)

fPiEffPhi = fRecoPiPhi.Clone('pi_eff')
fPiEffPhi.Divide(fPiEffPhi, fPFOwTrkPhi, 1, 1, 'B')
fPiEffPhi.SetLineColor(pl2Color)
fPiEffPhi.SetLineWidth(2)
fPiEffPhi.SetTitle('ChargedPionEffVsPhi')
fPiEffPhi.SetMarkerStyle(8)
fPiEffPhi.SetMarkerColor(pl2Color)
fPiEffPhi.GetXaxis().SetTitle('PFO (w/ trk) #phi (rad)')
fPiEffPhi.GetYaxis().SetTitle("Efficiency")
fPiEffPhi.SetMinimum(0.0)
fPiEffPhi.SetMaximum(1.4)
hists.append(fPiEffPhi)

# Efficiency to create a PFO with a track
fPFOTrkEffPt = fPFOwTrkPt.Clone('pi_eff')
fPFOTrkEffPt.Divide(fPFOTrkEffPt, fMCPiWTrkPt, 1, 1, 'B')
fPFOTrkEffPt.SetLineColor(pl3Color)
fPFOTrkEffPt.SetLineWidth(3)
fPFOTrkEffPt.SetTitle('PFOwTrkEffVsPt')
fPFOTrkEffPt.SetMarkerStyle(8)
fPFOTrkEffPt.SetMarkerColor(pl3Color)
fPFOTrkEffPt.GetXaxis().SetTitle('MC Charged Pion p_{T} (GeV)')
fPFOTrkEffPt.GetYaxis().SetTitle("Track-Cluster Matching Efficiency")
fPFOTrkEffPt.SetMinimum(0.0)
fPFOTrkEffPt.SetMaximum(1.4)
hists.append(fPFOTrkEffPt)

fPFOTrkEffTheta = fPFOwTrkTheta.Clone('pi_eff')
fPFOTrkEffTheta.Divide(fPFOTrkEffTheta, fMCPiWTrkTheta, 1, 1, 'B')
fPFOTrkEffTheta.SetLineColor(pl3Color)
fPFOTrkEffTheta.SetLineWidth(2)
fPFOTrkEffTheta.SetTitle('PFOwTrkEffVsTheta')
fPFOTrkEffTheta.SetMarkerStyle(8)
fPFOTrkEffTheta.SetMarkerColor(pl3Color)
fPFOTrkEffTheta.GetXaxis().SetTitle('MC Charged Pion #theta (rad)')
fPFOTrkEffTheta.GetYaxis().SetTitle("Track-Cluster Matching Efficiency")
fPFOTrkEffTheta.SetMinimum(0.0)
fPFOTrkEffTheta.SetMaximum(1.4)
hists.append(fPFOTrkEffTheta)

fPFOTrkEffPhi = fPFOwTrkPhi.Clone('pi_eff')
fPFOTrkEffPhi.Divide(fPFOTrkEffPhi, fMCPiWTrkPhi, 1, 1, 'B')
fPFOTrkEffPhi.SetLineColor(pl3Color)
fPFOTrkEffPhi.SetLineWidth(2)
fPFOTrkEffPhi.SetTitle('PFOwTrkEffVsPhi')
fPFOTrkEffPhi.SetMarkerStyle(8)
fPFOTrkEffPhi.SetMarkerColor(pl3Color)
fPFOTrkEffPhi.GetXaxis().SetTitle('MC Charged Pion #phi (rad)')
fPFOTrkEffPhi.GetYaxis().SetTitle("Track-Cluster Matching Efficiency")
fPFOTrkEffPhi.SetMinimum(0.0)
fPFOTrkEffPhi.SetMaximum(1.4)
hists.append(fPFOTrkEffPhi)

# Total charged pion reconstruction efficienecy
fTotalPiEffPt = fRecoPiPt.Clone('pi_eff')
fTotalPiEffPt.Divide(fTotalPiEffPt, fMCPiPt, 1, 1, 'B')
fTotalPiEffPt.SetLineColor(1)
fTotalPiEffPt.SetLineWidth(3)
fTotalPiEffPt.SetTitle('TotalPiEffPt')
fTotalPiEffPt.SetMarkerStyle(34)
fTotalPiEffPt.SetMarkerColor(1)
fTotalPiEffPt.GetXaxis().SetTitle('MC Charged Pion p_{T} (GeV)')
fTotalPiEffPt.GetYaxis().SetTitle("Total Charged Pion Reco. Eff.")
fTotalPiEffPt.SetMinimum(0.0)
fTotalPiEffPt.SetMaximum(1.4)
hists.append(fTotalPiEffPt)

fTotalPiEffTheta = fRecoPiTheta.Clone('pi_eff')
fTotalPiEffTheta.Divide(fTotalPiEffTheta, fMCPiTheta, 1, 1, 'B')
fTotalPiEffTheta.SetLineColor(1)
fTotalPiEffTheta.SetLineWidth(2)
fTotalPiEffTheta.SetTitle('TotalPiEffTheta')
fTotalPiEffTheta.SetMarkerStyle(34)
fTotalPiEffTheta.SetMarkerColor(1)
fTotalPiEffTheta.GetXaxis().SetTitle('MC Charged Pion #theta (rad)')
fTotalPiEffTheta.GetYaxis().SetTitle("Total Charged Pion Reco. Eff.")
fTotalPiEffTheta.SetMinimum(0.0)
fTotalPiEffTheta.SetMaximum(1.4)
hists.append(fTotalPiEffTheta)

fTotalPiEffPhi = fRecoPiPhi.Clone('pi_eff')
fTotalPiEffPhi.Divide(fTotalPiEffPhi, fMCPiPhi, 1, 1, 'B')
fTotalPiEffPhi.SetLineColor(1)
fTotalPiEffPhi.SetLineWidth(2)
fTotalPiEffPhi.SetTitle('TotalPiEffPhi')
fTotalPiEffPhi.SetMarkerStyle(34)
fTotalPiEffPhi.SetMarkerColor(1)
fTotalPiEffPhi.GetXaxis().SetTitle('MC Charged Pion #phi (rad)')
fTotalPiEffPhi.GetYaxis().SetTitle("Total Charged Pion Reco. Eff.")
fTotalPiEffPhi.SetMinimum(0.0)
fTotalPiEffPhi.SetMaximum(1.4)
hists.append(fTotalPiEffPhi)

myCanvas4 = TCanvas("scoobyDoo4", "Canvas", 800, 600)
myCanvas4.SetFrameLineWidth(2)

#fTrkPtEff.Draw("E")
fPiEffPt.Draw("E")
fPFOTrkEffPt.Draw("E SAME")
fTotalPiEffPt.Draw("E SAME")

legend2 = TLegend(0.55, 0.7, 0.89, 0.89)
#legend2.AddEntry(fTrkPtEff, "Tracking", "lep")
legend2.AddEntry(fPFOTrkEffPt, "Track-Cluster Matching", "lep")
legend2.AddEntry(fPiEffPt, "Identification of PFOs", "lep")
legend2.AddEntry(fTotalPiEffPt, "Charged Pion ID", "lep")
legend2.SetBorderSize(0)
legend2.Draw()

geo_label.DrawLatex(0.17, 0.84, "#it{MAIA} #bf{Work in Progress}")
gen_label.DrawLatex(0.17, 0.80, "#bf{Charged Pion Gun, no BIB}")
gen_label.DrawLatex(0.17, 0.76, "#bf{Barrel Region (40^{#circ} < #theta < 140^{#circ})}")

myCanvas4.Update()
myCanvas4.SaveAs("all_efficiencies_pt.png")

myCanvas5 = TCanvas("scoobyDoo5", "Canvas", 800, 600)
myCanvas5.SetFrameLineWidth(2)

fTrkThetaEff.Draw("E")
fPiEffTheta.Draw("E SAME")
fPFOTrkEffTheta.Draw("E SAME")
fTotalPiEffTheta.Draw("E SAME")
legend2.Draw()

geo_label.DrawLatex(0.17, 0.84, "#it{MAIA} #bf{Work in Progress}")
gen_label.DrawLatex(0.17, 0.80, "#bf{Charged Pion Gun, no BIB}")
gen_label.DrawLatex(0.17, 0.76, "#bf{Barrel Region (40^{#circ} < #theta < 140^{#circ})}")

myCanvas5.Update()
myCanvas5.SaveAs("all_efficiencies_theta.png")

myCanvas6 = TCanvas("scoobyDoo6", "Canvas", 800, 600)
myCanvas6.SetFrameLineWidth(2)

fTrkPhiEff.Draw("E")
fPiEffPhi.Draw("E SAME")
fPFOTrkEffPhi.Draw("E SAME")
fTotalPiEffPhi.Draw("E SAME")

legend2.Draw()

geo_label.DrawLatex(0.17, 0.84, "#it{MAIA} #bf{Work in Progress}")
gen_label.DrawLatex(0.17, 0.80, "#bf{Charged Pion Gun, no BIB}")
gen_label.DrawLatex(0.17, 0.76, "#bf{Barrel Region (40^{#circ} < #theta < 140^{#circ})}")

myCanvas6.Update()
myCanvas6.SaveAs("all_efficiencies_phi.png")

myCanvas7 = TCanvas("scoobyDoo7", "Canvas", 800, 600)
myCanvas7.SetFrameLineWidth(2)

eRes.Draw("E1")

geo_label.DrawLatex(0.17, 0.84, "#it{MAIA} #bf{Work in Progress}")
gen_label.DrawLatex(0.17, 0.80, "#bf{Charged Pion Gun, no BIB}")
gen_label.DrawLatex(0.17, 0.76, "#bf{Barrel Region (40^{#circ} < #theta < 140^{#circ})}")

myCanvas7.Update()
myCanvas7.SaveAs("energy_resolution.png")


for hist in hists:
  filename = hist.GetTitle() + '.png'
  canvas = TCanvas()
  hist.Draw("E1")
  canvas.SaveAs(filename)


print("number of total events: ", test1)
print("events after cutting on theta: ", test2)
print("Number of MC Pis: ", totalMCPis)
print("Number of Tracks: ", totalTrks)

#print("number of total events, after track cleaning: ", test2)

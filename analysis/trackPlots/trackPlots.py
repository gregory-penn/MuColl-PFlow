import numpy as np
import ROOT
from ROOT import TLatex, gStyle, TLegend
import pickle

with open("momentum_res_muonSiTracks_Refitted.pkl", "rb") as f:
    sigmaPOverP_refit, trackSigmaD0_refit, trackSigmaZ0_refit, trackPt_refit, trackTheta_refit, trkChi2nDOF_refit, trknHits_refit, trkd0_refit, trkz0_refit, trackFound_refit, truthpt_refit, truththeta_refit, matchedTrkdR_refit = pickle.load(f)

with open("momentum_res_muonSiTracks.pkl", "rb") as f:
    sigmaPOverP, trackSigmaD0, trackSigmaZ0, trackPt, trackTheta, trkChi2nDOF, trknHits, trkd0, trkz0, trackFound, truthpt, truththeta, matchedTrkdR = pickle.load(f)

trackPt_refit = np.array(trackPt_refit)
sigmaPOverP_refit = np.array(sigmaPOverP_refit)
trackTheta_refit = np.array(trackTheta_refit) * 180 / np.pi
trkChi2nDOF_refit = np.array(trkChi2nDOF_refit)
trknHits_refit = np.array(trknHits_refit)
trackSigmaD0_refit = np.array(trackSigmaD0_refit)
trackSigmaZ0_refit = np.array(trackSigmaZ0_refit)
trackFound = np.array(trackFound)
trackFound_refit = np.array(trackFound_refit)
matchedTrkdR_refit = np.array(matchedTrkdR_refit)

trackPt = np.array(trackPt)
sigmaPOverP = np.array(sigmaPOverP)
trackTheta = np.array(trackTheta) * 180 / np.pi
trkChi2nDOF = np.array(trkChi2nDOF)
trknHits = np.array(trknHits)
trackSigmaD0 = np.array(trackSigmaD0)
trackSigmaZ0 = np.array(trackSigmaZ0)
trackFound = np.array(trackFound)
truthpt = np.array(truthpt)
truththeta = np.array(truththeta) * 180 / np.pi
matchedTrkdR = np.array(matchedTrkdR)


# splitting theta into pt regions
theta_pt_0_50 = trackTheta_refit[trackPt_refit < 50.0]
theta_pt_50_250 = trackTheta_refit[(50 <= trackPt_refit) & (trackPt_refit < 250.0)]
theta_pt_250_1000 = trackTheta_refit[250 <= trackPt_refit]
# print(len(theta_pt_0_50))
# print(len(theta_pt_50_250))
# print(len(theta_pt_250_1000))
# print(len(theta_pt_0_50) + len(theta_pt_250_1000) + len(theta_pt_50_250) - len(trackTheta_refit))

# splitting pt into theta regions
trackFound_barrel = trackFound[(40 <= truththeta) & (truththeta <= 140)]
trackFound_endcap = trackFound[(40 > truththeta) | (truththeta > 140)]

trackFound_refit_barrel = trackFound_refit[(40 <= truththeta) & (truththeta <= 140)]
trackFound_refit_endcap = trackFound_refit[(40 > truththeta) | (truththeta > 140)]

truthpt_barrel = truthpt[(40 <= truththeta) & (truththeta < 140)]
truthpt_endcap = truthpt[(40 > truththeta) | (truththeta > 140)]

nbins = 11

bins = np.linspace(np.min(trackTheta_refit), np.max(trackTheta_refit), nbins) # --> rad values of barrel region: 0.698 to 2.44 rad.
bin_centers = 0.5 * (bins[:-1] + bins[1:])

bins_truth = np.linspace(np.min(truththeta), np.max(truththeta), nbins) # --> rad values of barrel region: 0.698 to 2.44 rad.
bin_centers_truth = 0.5 * (bins_truth[:-1] + bins_truth[1:])

nbins_pt = 14
bins_pt = np.linspace(np.min(truthpt), np.max(truthpt), nbins_pt) 
bin_centers_pt = 0.5 * (bins_pt[:-1] + bins_pt[1:])
nbins_pt_endcap = 7
bins_pt_endcap = np.linspace(np.min(truthpt_endcap), np.max(truthpt_endcap), nbins_pt_endcap) 
bin_centers_pt_endcap = 0.5 * (bins_pt_endcap[:-1] + bins_pt_endcap[1:])

mean_pt_res = np.empty(len(bins))
res_pt_err = np.empty(len(bins))
mean_pt_res_refit = np.empty(len(bins))
res_pt_err_refit = np.empty(len(bins))

mean_d0_res = np.empty(len(bins))
res_d0_err = np.empty(len(bins))
mean_d0_res_refit = np.empty(len(bins))
res_d0_err_refit = np.empty(len(bins))

mean_z0_res = np.empty(len(bins))
res_z0_err = np.empty(len(bins))
mean_z0_res_refit = np.empty(len(bins))
res_z0_err_refit = np.empty(len(bins))

# track eff vs. theta
track_eff = np.empty(len(bins))
track_eff_err = np.empty(len(bins))
track_eff_refit = np.empty(len(bins))
track_eff_err_refit = np.empty(len(bins))

# track eff vs. pt
track_eff_pt = np.empty(len(bins_pt))
track_eff_err_pt = np.empty(len(bins_pt))
track_eff_refit_pt = np.empty(len(bins_pt))
track_eff_err_refit_pt = np.empty(len(bins_pt))

track_eff_pt_barrel = np.empty(len(bins_pt))
track_eff_err_pt_barrel = np.empty(len(bins_pt))
track_eff_refit_pt_barrel = np.empty(len(bins_pt))
track_eff_err_refit_pt_barrel = np.empty(len(bins_pt))

track_eff_pt_endcap = np.empty(len(bins_pt))
track_eff_err_pt_endcap = np.empty(len(bins_pt))
track_eff_refit_pt_endcap = np.empty(len(bins_pt))
track_eff_err_refit_pt_endcap = np.empty(len(bins_pt))

indices = np.digitize(trackTheta, bins) - 1
indices_refit = np.digitize(trackTheta_refit, bins) - 1
indices_truth = np.digitize(truththeta, bins_truth) - 1
indices_pt = np.digitize(truthpt, bins_pt) - 1
indices_pt_barrel = np.digitize(truthpt_barrel, bins_pt) - 1
indices_pt_endcap = np.digitize(truthpt_endcap, bins_pt_endcap) - 1

for i in range(len(bin_centers)):
    in_bin = (indices == i)
    in_bin_refit = (indices_refit == i)
    in_bin_truth = (indices_truth == i)

    res_pt_vals = sigmaPOverP[in_bin]
    mean_pt_res[i] = np.mean(res_pt_vals)
    res_pt_err[i] = np.std(res_pt_vals) / np.sqrt(len(res_pt_vals))

    res_pt_vals_refit = sigmaPOverP_refit[in_bin_refit]
    mean_pt_res_refit[i] = np.mean(res_pt_vals_refit)
    res_pt_err_refit[i] = np.std(res_pt_vals_refit) / np.sqrt(len(res_pt_vals_refit))

    res_d0_vals = trackSigmaD0[in_bin]
    mean_d0_res[i] = np.mean(res_d0_vals)
    res_d0_err[i] = np.std(res_d0_vals) / np.sqrt(len(res_d0_vals))

    res_d0_vals_refit = trackSigmaD0_refit[in_bin_refit]
    mean_d0_res_refit[i] = np.mean(res_d0_vals_refit)
    res_d0_err_refit[i] = np.std(res_d0_vals_refit) / np.sqrt(len(res_d0_vals_refit))

    res_z0_vals = trackSigmaZ0[in_bin]
    mean_z0_res[i] = np.mean(res_z0_vals)
    res_z0_err[i] = abs(np.std(res_z0_vals)) / np.sqrt(len(res_z0_vals))

    res_z0_vals_refit = trackSigmaZ0_refit[in_bin_refit]
    mean_z0_res_refit[i] = np.mean(res_z0_vals_refit)
    res_z0_err_refit[i] = abs(np.std(res_z0_vals_refit)) / np.sqrt(len(res_z0_vals_refit))

    track_eff[i] = np.mean(trackFound[in_bin_truth])
    track_eff_err[i] = np.std(trackFound[in_bin_truth]) / np.sqrt(len(trackFound[in_bin_truth]))
    track_eff_refit[i] = np.mean(trackFound_refit[in_bin_truth])
    track_eff_err_refit[i] = np.std(trackFound_refit[in_bin_truth]) / np.sqrt(len(trackFound_refit[in_bin_truth]))

for i in range(len(bin_centers_pt)):
    in_bin_pt = (indices_pt == i)
    in_bin_pt_barrel = (indices_pt_barrel == i)

    track_eff_pt[i] = np.mean(trackFound[in_bin_pt])
    track_eff_err_pt[i] = np.std(trackFound[in_bin_pt]) / np.sqrt(len(trackFound[in_bin_pt]))
    track_eff_refit_pt[i] = np.mean(trackFound_refit[in_bin_pt])
    track_eff_err_refit_pt[i] = np.std(trackFound_refit[in_bin_pt]) / np.sqrt(len(trackFound_refit[in_bin_pt]))

    track_eff_pt_barrel[i] = np.mean(trackFound_barrel[in_bin_pt_barrel])
    track_eff_err_pt_barrel[i] = np.std(trackFound_barrel[in_bin_pt_barrel]) / np.sqrt(len(trackFound_barrel[in_bin_pt_barrel]))
    track_eff_refit_pt_barrel[i] = np.mean(trackFound_refit_barrel[in_bin_pt_barrel])
    track_eff_err_refit_pt_barrel[i] = np.std(trackFound_refit_barrel[in_bin_pt_barrel]) / np.sqrt(len(trackFound_refit_barrel[in_bin_pt_barrel]))

for i in range(len(bin_centers_pt_endcap)):
    in_bin_pt_endcap = (indices_pt_endcap == i)

    track_eff_pt_endcap[i] = np.mean(trackFound_endcap[in_bin_pt_endcap])
    track_eff_err_pt_endcap[i] = np.std(trackFound_endcap[in_bin_pt_endcap]) / np.sqrt(len(trackFound_endcap[in_bin_pt_endcap]))
    track_eff_refit_pt_endcap[i] = np.mean(trackFound_refit_endcap[in_bin_pt_endcap])
    track_eff_err_refit_pt_endcap[i] = np.std(trackFound_refit_endcap[in_bin_pt_endcap]) / np.sqrt(len(trackFound_refit_endcap[in_bin_pt_endcap]))


##### PLOTTING #####

#set global style
gStyle.SetTitleSize(0.042, "X")
gStyle.SetTitleSize(0.042, "Y")
#disabling plot titles - personal preference
gStyle.SetOptTitle(0)
gStyle.SetLineWidth(2)
gStyle.SetOptStat(0) # remove stat box at upper right corner 
gStyle.SetPadLeftMargin(0.13)
gStyle.SetPadRightMargin(0.07)
gStyle.SetMarkerStyle(8)

# Defining some labels
FirstLabel = "#it{MAIA} #bf{Work in Progress}"
SecondLabel = "#bf{Muon Gun, no BIB}"
ThirdLabel = "#bf{1 GeV < p_{T} < 1000 GeV}"

legend = TLegend(0.6, 0.7, 0.89, 0.89)
legend.SetBorderSize(0)

geo_label = TLatex()
geo_label.SetNDC()
geo_label.SetTextSize(0.04)

gen_label = TLatex()
gen_label.SetNDC()
gen_label.SetTextSize(0.03)
    
##### Pt res vs. theta #####

hSigmaptOverpt_vs_theta = ROOT.TH1F("h_momres", ";Track #theta (#circ);Track #sigma(p_{T})/p_{T}", len(bins)-1, bins)
hSigmaptOverpt_vs_theta.SetMarkerColor(46)
hSigmaptOverpt_vs_theta.SetMarkerStyle(8)
hSigmaptOverpt_vs_theta.SetLineColor(46)
hSigmaptOverpt_vs_theta.SetLineWidth(4)
hSigmaptOverpt_vs_theta.GetXaxis().SetRangeUser(0., 180.)
hSigmaptOverpt_vs_theta.SetMaximum(1.0)

hSigmaptOverpt_vs_theta_refit = ROOT.TH1F("h_momres_refit", ";Track #theta (#circ);Track #sigma(p_{T})/p_{T}", len(bins)-1, bins)
hSigmaptOverpt_vs_theta_refit.SetMarkerStyle(8)
hSigmaptOverpt_vs_theta_refit.SetMarkerColor(38)
hSigmaptOverpt_vs_theta_refit.SetLineColor(38)
hSigmaptOverpt_vs_theta_refit.SetLineWidth(4)
hSigmaptOverpt_vs_theta_refit.GetXaxis().SetRangeUser(0., 180.)
hSigmaptOverpt_vs_theta_refit.SetMaximum(1.0)

for i in range(len(mean_pt_res)):
    hSigmaptOverpt_vs_theta.SetBinContent(i + 1, mean_pt_res[i])
    hSigmaptOverpt_vs_theta.SetBinError(i + 1, res_pt_err[i])
    hSigmaptOverpt_vs_theta_refit.SetBinContent(i + 1, mean_pt_res_refit[i])
    hSigmaptOverpt_vs_theta_refit.SetBinError(i + 1, res_pt_err_refit[i])

cSigmaptOverpt_vs_pt = ROOT.TCanvas("cSigmaptOverpt_vs_pt", "canvas", 1600, 1200)

hSigmaptOverpt_vs_theta.Draw("E")
hSigmaptOverpt_vs_theta_refit.Draw("E SAME")

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)

legend.AddEntry(hSigmaptOverpt_vs_theta, "SiTracks Container", "lep")
legend.AddEntry(hSigmaptOverpt_vs_theta_refit, "SiTracks_Refitted Container", "lep")
legend.Draw()

cSigmaptOverpt_vs_pt.SetLogy(True)
cSigmaptOverpt_vs_pt.Update()
cSigmaptOverpt_vs_pt.SaveAs("sigmapT_vs_theta.png")

##### d0 res vs. theta #####

hSigmad0_vs_theta = ROOT.TH1F("h_d0res", ";Track #theta (#circ);Track #sigma(d_{0}) (mm)", len(bins)-1, bins)
hSigmad0_vs_theta.SetMarkerColor(46)
hSigmad0_vs_theta.SetMarkerStyle(8)
hSigmad0_vs_theta.SetLineColor(46)
hSigmad0_vs_theta.SetLineWidth(4)
hSigmad0_vs_theta.GetXaxis().SetRangeUser(0., 180.)
hSigmad0_vs_theta.SetMaximum(1.0)

hSigmad0_vs_theta_refit = ROOT.TH1F("h_d0res_refit", ";Track #theta (#circ);Track #sigma(d_{0}) (mm)", len(bins)-1, bins)
hSigmad0_vs_theta_refit.SetMarkerStyle(8)
hSigmad0_vs_theta_refit.SetMarkerColor(38)
hSigmad0_vs_theta_refit.SetLineColor(38)
hSigmad0_vs_theta_refit.SetLineWidth(4)
hSigmad0_vs_theta_refit.GetXaxis().SetRangeUser(0., 180.)
hSigmad0_vs_theta_refit.SetMaximum(1.0)

for i in range(len(mean_d0_res)):
    hSigmad0_vs_theta.SetBinContent(i + 1, mean_d0_res[i])
    hSigmad0_vs_theta.SetBinError(i + 1, res_d0_err[i])
    hSigmad0_vs_theta_refit.SetBinContent(i + 1, mean_d0_res_refit[i])
    hSigmad0_vs_theta_refit.SetBinError(i + 1, res_d0_err_refit[i])

cSigmad0_vs_theta = ROOT.TCanvas("cSigmad0_vs_theta", "canvas", 1600, 1200)

hSigmad0_vs_theta.SetMinimum(0.000001)
hSigmad0_vs_theta_refit.SetMinimum(0.000001)
hSigmad0_vs_theta.Draw("E")
hSigmad0_vs_theta_refit.Draw("E SAME")

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)

legend.Draw()

cSigmad0_vs_theta.SetLogy(True)
cSigmad0_vs_theta.Update()
cSigmad0_vs_theta.SaveAs("sigmad0_vs_theta.png")

##### z0 res vs. theta #####

hSigmaz0_vs_theta = ROOT.TH1F("h_z0res", ";Track #theta (#circ);Track #sigma(z_{0}) (mm)", len(bins)-1, bins)
hSigmaz0_vs_theta.SetMarkerColor(46)
hSigmaz0_vs_theta.SetMarkerStyle(8)
hSigmaz0_vs_theta.SetLineColor(46)
hSigmaz0_vs_theta.SetLineWidth(4)
hSigmaz0_vs_theta.GetXaxis().SetRangeUser(0., 180.)
hSigmaz0_vs_theta.SetMaximum(1.0)

hSigmaz0_vs_theta_refit = ROOT.TH1F("h_z0res_refit", ";Track #theta (#circ);Track #sigma(z_{0}) (mm)", len(bins)-1, bins)
hSigmaz0_vs_theta_refit.SetMarkerStyle(8)
hSigmaz0_vs_theta_refit.SetMarkerColor(38)
hSigmaz0_vs_theta_refit.SetLineColor(38)
hSigmaz0_vs_theta_refit.SetLineWidth(4)
hSigmaz0_vs_theta_refit.GetXaxis().SetRangeUser(0., 180.)
hSigmaz0_vs_theta_refit.SetMaximum(1.0)

for i in range(len(mean_z0_res)):
    hSigmaz0_vs_theta.SetBinContent(i + 1, abs(mean_z0_res[i]))
    hSigmaz0_vs_theta.SetBinError(i + 1, res_z0_err[i])
    hSigmaz0_vs_theta_refit.SetBinContent(i + 1, abs(mean_z0_res_refit[i]))
    hSigmaz0_vs_theta_refit.SetBinError(i + 1, res_z0_err_refit[i])

cSigmaz0_vs_theta = ROOT.TCanvas("cSigmaz0_vs_theta", "canvas", 1600, 1200)

hSigmaz0_vs_theta.SetMinimum(1e-8)
hSigmaz0_vs_theta.SetMaximum(1e-3)
hSigmaz0_vs_theta.SetStats(False)

hSigmaz0_vs_theta_refit.SetMinimum(1e-8)
hSigmaz0_vs_theta_refit.SetMaximum(1e-3)
hSigmaz0_vs_theta_refit.SetStats(False)

hSigmaz0_vs_theta.Draw("E1")
hSigmaz0_vs_theta_refit.Draw("E1 SAME")

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)

legend.Draw()

cSigmaz0_vs_theta.SetLogy(True)
cSigmaz0_vs_theta.Update()
cSigmaz0_vs_theta.SaveAs("sigmaz0_vs_theta.png")

###### TRACK MOM RES. PLOTTING ######

hMomRes = ROOT.TH1F("h1", ";Track #sigma(p_{T})/p_{T}; Normalized Count", 26, 0, 0.5)
hMomRes.SetMarkerStyle(8)
hMomRes.SetMarkerColor(46)
hMomRes.SetLineColor(46)
hMomRes.SetLineWidth(4)

hMomRes_refit = ROOT.TH1F("h1_refit", ";Track #sigma(p_{T})/p_{T}; Normalized Count", 26, 0, 0.5)
hMomRes_refit.SetMarkerStyle(8)
hMomRes_refit.SetMarkerColor(38)
hMomRes_refit.SetLineColor(38)
hMomRes_refit.SetLineWidth(4)

for val in sigmaPOverP:
    hMomRes.Fill(val, 1 / len(sigmaPOverP))
for val in sigmaPOverP_refit:
    hMomRes_refit.Fill(val, 1 / len(sigmaPOverP_refit))

cMomRes = ROOT.TCanvas("cMomRes", "canvas", 1600, 1200)
cMomRes.SetLeftMargin(0.15)

hMomRes.SetMaximum(11.0)
hMomRes_refit.SetMaximum(11.0)
hMomRes.Draw("E ")
hMomRes_refit.Draw("E SAME")
cMomRes.SetLogy(True)

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)
legend.Draw()

cMomRes.Update()
cMomRes.SaveAs("sigmapT.png")

###### TRACK CHI2 PLOTTING ######

hChi2 = ROOT.TH1F("hChi2", ";Track #chi^{2}/ n_{dof}; Normalized Count", 15, 0, 3.0)
hChi2.SetMarkerStyle(8)
hChi2.SetMarkerColor(46)
hChi2.SetLineColor(46)
hChi2.SetLineWidth(4)

hChi2_refit = ROOT.TH1F("hChi2_refit", ";Track #chi^{2}/ n_{dof}; Normalized Count", 15, 0, 3.0)
hChi2_refit.SetMarkerStyle(8)
hChi2_refit.SetMarkerColor(38)
hChi2_refit.SetLineColor(38)
hChi2_refit.SetLineWidth(4)

for val in trkChi2nDOF:
    hChi2.Fill(val, 1 / len(sigmaPOverP))
for val in trkChi2nDOF_refit:
    hChi2_refit.Fill(val, 1 / len(sigmaPOverP_refit))

cChi2 = ROOT.TCanvas("cChi2", "canvas", 1600, 1200)
cChi2.SetLeftMargin(0.15)

hChi2.SetMaximum(0.3)
hChi2_refit.SetMaximum(0.3)
hChi2.Draw("HIST E")
hChi2_refit.Draw("HIST E SAME")

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)
legend.Draw()

cChi2.Update()
cChi2.SaveAs("chi2.png")

###### TRACK nHITS PLOTTING ######

nbinsHits = 22 

hnHits = ROOT.TH1F("hnHits", ";Track n_{hits}; Normalized Count", nbinsHits, 0, nbinsHits)
hnHits.SetMarkerStyle(8)
hnHits.SetMarkerColor(46)
hnHits.SetLineColor(46)
hnHits.SetLineWidth(4)

hnHits_refit = ROOT.TH1F("hnHits_refit", ";Track #chi^{2}/ n_{dof}; Normalized Count", nbinsHits, 0, nbinsHits)
hnHits_refit.SetMarkerStyle(8)
hnHits_refit.SetMarkerColor(38)
hnHits_refit.SetLineColor(38)
hnHits_refit.SetLineWidth(4)

for val in trknHits:
    hnHits.Fill(val, 1 / len(trknHits))
for val in trknHits_refit:
    hnHits_refit.Fill(val, 1 / len(trknHits_refit))

cnHits = ROOT.TCanvas("cnHits", "canvas", 1600, 1200)
cnHits.SetLeftMargin(0.15)

hnHits.SetMaximum(0.3)
hnHits_refit.SetMaximum(0.3)
hnHits.Draw("HIST E")
hnHits_refit.Draw("HIST E SAME")

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)
legend.Draw()

cnHits.Update()
cnHits.SaveAs("nHits.png")

### 3D: nHits, pt, track pt resolution ### 

lowerNHit = 4
upperNHit = 16
lowerTrkPt = 0
UpperTrkPt = 1000

nHitBins = 7
TrkPtBins = 5

nHitBins = np.linspace(lowerNHit, upperNHit, nHitBins)
TrkPBins = np.linspace(lowerTrkPt, UpperTrkPt, TrkPtBins)

#hnHit_trackpt_res = ROOT.TH2F("nHit_trackpt_res", "Track #sigma(p_{T}/p_{T});Track n_{Hits}; Track p_{T} (GeV)", nHitBins - 1, lowerNHit, upperNHit, TrkPtBins - 1, lowerTrkPt, UpperTrkPt)
hnHit_trackpt_res = ROOT.TH2F("nHit_trackpt_res", "Track #sigma(p_{T}/p_{T});Track n_{Hits}; Track p_{T} (GeV)", 6, 4, 16, 4, 0, 1000)
hnHit_trackpt_res.GetZaxis().SetTitle("Track #sigma(p_{T}/p_{T})")
hnHit_trackpt_res.GetZaxis().SetTitleOffset(1.2)   
hnHit_trackpt_res.GetZaxis().SetTitleSize(0.045)   

hCorr_nHit_pt = ROOT.TH2F("hCorr_nHit_pt", "Entries;Track n_{Hits}; Track p_{T} (GeV)", 6, 4, 16, 4, 0, 1000)
hCorr_nHit_pt.GetZaxis().SetTitle("Normalized Entries")
hCorr_nHit_pt.GetZaxis().SetTitleOffset(1.2)   
hCorr_nHit_pt.GetZaxis().SetTitleSize(0.045)   

normFactor = len(sigmaPOverP_refit[(lowerNHit < trknHits_refit) & (upperNHit >= trknHits_refit) & (lowerTrkPt < trackPt_refit) & (UpperTrkPt >= trackPt_refit)])
print(normFactor)

nevents = 0 
for ix in range(len(nHitBins) - 1):
    lowerX = nHitBins[ix]
    upperX = nHitBins[ix+1]
    xBin = (upperX + lowerX) / 2
    for iy in range(len(TrkPBins) - 1):
        lowerY = TrkPBins[iy]
        upperY = TrkPBins[iy + 1]
        yBin = (upperY + lowerY) / 2
        trkMomResTemp = sigmaPOverP_refit[(lowerX < trknHits_refit) & (upperX >= trknHits_refit) & (lowerY < trackPt_refit) & (upperY >= trackPt_refit)]
        zBin = np.mean(trkMomResTemp)
        nevents += len(trkMomResTemp)
        binx = hnHit_trackpt_res.GetXaxis().FindBin(xBin)
        biny = hnHit_trackpt_res.GetYaxis().FindBin(yBin)
        hnHit_trackpt_res.SetBinContent(binx, biny, zBin)
        hCorr_nHit_pt.SetBinContent(binx,biny, round(len(trkMomResTemp) / normFactor, 3))

cHit_trackpt_res = ROOT.TCanvas("cHit_trackpt_res", "cHit_trackpt_res", 800, 600)
cHit_trackpt_res.SetRightMargin(0.18)
hnHit_trackpt_res.Draw("COLZ TEXT")
cHit_trackpt_res.SaveAs("3D_nHit_pT_res.png")

cCorr_nHit_pt = ROOT.TCanvas("cCorr_nHit_pt", "cCorr_nHit_pt", 800, 600)
cCorr_nHit_pt.SetRightMargin(0.18)
hCorr_nHit_pt.Draw("COLZ TEXT")
cCorr_nHit_pt.SaveAs("3D_nHit_pT_count.png")

### EFFICIENCY PLOTS ###

### TRACKING EFF VS THETA ### 

hEffVsTheta = ROOT.TH1F("h_eff_theta", ";Truth #theta (#circ);Tracking Efficiency",len(bins)-1, bins)
hEffVsTheta.SetMarkerColor(46)
hEffVsTheta.SetMarkerStyle(8)
hEffVsTheta.SetLineColor(46)
hEffVsTheta.SetLineWidth(4)
hEffVsTheta.GetXaxis().SetRangeUser(0., 180.)
hEffVsTheta.SetMaximum(1.4)

hEffVsTheta_refit = ROOT.TH1F("h_eff_theta_refit", ";Truth #theta (#circ);Tracking Efficiency", len(bins)-1, bins)
hEffVsTheta_refit.SetMarkerStyle(8)
hEffVsTheta_refit.SetMarkerColor(38)
hEffVsTheta_refit.SetLineColor(38)
hEffVsTheta_refit.SetLineWidth(4)
hEffVsTheta_refit.GetXaxis().SetRangeUser(0., 180.)
hEffVsTheta_refit.SetMaximum(1.4)

for i in range(len(mean_pt_res)):
    hEffVsTheta.SetBinContent(i + 1, track_eff[i])
    hEffVsTheta.SetBinError(i + 1, track_eff_err[i])
    hEffVsTheta_refit.SetBinContent(i + 1, track_eff_refit[i])
    hEffVsTheta_refit.SetBinError(i + 1, track_eff_err_refit[i])

cTrackEffVsTheta = ROOT.TCanvas("cTrackEffVsTheta", "canvas", 1600, 1200)

hEffVsTheta.Draw("E")
hEffVsTheta_refit.Draw("E SAME")

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)

legend.Draw()

cTrackEffVsTheta.Update()
cTrackEffVsTheta.SaveAs("eff_theta.png")

### TRACKING EFF VS PT ### 

hEffVsPt = ROOT.TH1F("h_eff_pt", ";Truth p_{T} (GeV);Tracking Efficiency", nbins_pt - 1, np.min(truthpt), np.max(truthpt))
hEffVsPt.SetMarkerColor(46)
hEffVsPt.SetMarkerStyle(8)
hEffVsPt.SetLineColor(46)
hEffVsPt.SetLineWidth(4)
hEffVsPt.SetMaximum(1.4)
hEffVsPt.GetXaxis().SetRangeUser(0., 1000.)


hEffVsPt_refit = ROOT.TH1F("h_eff_pt_refit", ";Truth p_{T} (GeV);Tracking Efficiency", nbins_pt - 1, np.min(truthpt), np.max(truthpt))
hEffVsPt_refit.SetMarkerStyle(8)
hEffVsPt_refit.SetMarkerColor(38)
hEffVsPt_refit.SetLineColor(38)
hEffVsPt_refit.SetLineWidth(4)
hEffVsPt_refit.SetMaximum(1.4)
hEffVsPt_refit.GetXaxis().SetRangeUser(0., 1000.)

for i in range(len(track_eff_pt) - 1):
    hEffVsPt.SetBinContent(i + 1, track_eff_pt[i])
    hEffVsPt.SetBinError(i + 1, track_eff_err_pt[i])
    hEffVsPt_refit.SetBinContent(i + 1, track_eff_refit_pt[i])
    hEffVsPt_refit.SetBinError(i + 1, track_eff_err_refit_pt[i])

cTrackEffVsPt = ROOT.TCanvas("cTrackEffVsPt", "canvas", 1600, 1200)

hEffVsPt.Draw("E")
hEffVsPt_refit.Draw("E SAME")

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)

legend.Draw()

cTrackEffVsPt.Update()
cTrackEffVsPt.SaveAs("eff_pt.png")

### TRACKING EFF VS PT, BARREL AND ENDCAP ### 

hEffVsPtB = ROOT.TH1F("h_eff_pt_barrel", ";Truth p_{T} (GeV);Tracking Efficiency", nbins_pt - 1, np.min(truthpt), np.max(truthpt))
hEffVsPtB.SetMarkerColor(46)
hEffVsPtB.SetMarkerStyle(8)
hEffVsPtB.SetLineColor(46)
hEffVsPtB.SetLineWidth(4)
hEffVsPtB.SetLineStyle(1)
hEffVsPtB.SetMaximum(1.4)
hEffVsPtB.GetXaxis().SetRangeUser(0., 1000.)


hEffVsPtB_refit = ROOT.TH1F("h_eff_pt_refit_barrel", ";Truth p_{T} (GeV);Tracking Efficiency", nbins_pt - 1, np.min(truthpt), np.max(truthpt))
hEffVsPtB_refit.SetMarkerStyle(8)
hEffVsPtB_refit.SetMarkerColor(38)
hEffVsPtB_refit.SetLineColor(38)
hEffVsPtB_refit.SetLineWidth(4)
hEffVsPtB_refit.SetLineStyle(1)
hEffVsPtB_refit.SetMaximum(1.4)
hEffVsPtB_refit.GetXaxis().SetRangeUser(0., 1000.)

hEffVsPtE = ROOT.TH1F("h_eff_pt_endcap", ";Truth p_{T} (GeV);Tracking Efficiency", nbins_pt_endcap - 1, np.min(truthpt), np.max(truthpt))
hEffVsPtE.SetMarkerColor(46)
hEffVsPtE.SetMarkerStyle(8)
hEffVsPtE.SetLineColor(46)
hEffVsPtE.SetLineWidth(4)
hEffVsPtE.SetLineStyle(2)
hEffVsPtE.SetMaximum(1.4)
hEffVsPtE.GetXaxis().SetRangeUser(0., 1000.)

hEffVsPtE_refit = ROOT.TH1F("h_eff_pt_refit_endcap", ";Truth p_{T} (GeV);Tracking Efficiency", nbins_pt_endcap - 1, np.min(truthpt), np.max(truthpt))
hEffVsPtE_refit.SetMarkerStyle(8)
hEffVsPtE_refit.SetMarkerColor(38)
hEffVsPtE_refit.SetLineColor(38)
hEffVsPtE_refit.SetLineWidth(4)
hEffVsPtE_refit.SetLineStyle(2)
hEffVsPtE_refit.SetMaximum(1.4)
hEffVsPtE_refit.GetXaxis().SetRangeUser(0., 1000.)

for i in range(len(track_eff_pt) - 1):
    hEffVsPtB.SetBinContent(i + 1, track_eff_pt_barrel[i])
    hEffVsPtB.SetBinError(i + 1, track_eff_err_pt_barrel[i])
    hEffVsPtB_refit.SetBinContent(i + 1, track_eff_refit_pt_barrel[i])
    hEffVsPtB_refit.SetBinError(i + 1, track_eff_err_refit_pt_barrel[i])

    hEffVsPtE.SetBinContent(i + 1, track_eff_pt_endcap[i])
    hEffVsPtE.SetBinError(i + 1, track_eff_err_pt_endcap[i])
    hEffVsPtE_refit.SetBinContent(i + 1, track_eff_refit_pt_endcap[i])
    hEffVsPtE_refit.SetBinError(i + 1, track_eff_err_refit_pt_endcap[i])


cTrackEffVsPt_Sep = ROOT.TCanvas("cTrackEffVsPt_Sep", "canvas", 1600, 1200)

hEffVsPtB.Draw("E")
hEffVsPtB_refit.Draw("E SAME")
hEffVsPtE.Draw("E SAME")
hEffVsPtE_refit.Draw("E SAME")

geo_label.DrawLatex(0.18, 0.84, FirstLabel)
gen_label.DrawLatex(0.18, 0.80, SecondLabel)
gen_label.DrawLatex(0.18, 0.76, ThirdLabel)

legendSplit = TLegend(0.6, 0.7, 0.89, 0.89)
legendSplit.SetBorderSize(0)

legendSplit.AddEntry(hEffVsPtB, "SiTracks, Barrel", "lep")
legendSplit.AddEntry(hEffVsPtE, "SiTracks, Endcap", "lep")
legendSplit.AddEntry(hEffVsPtB_refit, "SiTracks_Refitted, Barrel", "lep")
legendSplit.AddEntry(hEffVsPtE_refit, "SiTracks_Refitted, Endcap", "lep")
legendSplit.Draw()

cTrackEffVsPt_Sep.Update()
cTrackEffVsPt_Sep.SaveAs("eff_pt_splitTheta.png")

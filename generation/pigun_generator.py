#####################################
#
# simple script to create lcio files with single particle
# events - modify as needed
# @author F.Gaede, DESY
# @date 1/07/2014
#
# initialize environment:
#  export PYTHONPATH=${LCIO}/src/python:${ROOTSYS}/lib
#
#####################################
import numpy as np
import random
from array import array
from g4units import deg, s

# --- LCIO dependencies ---
from pyLCIO import EVENT, IMPL, IOIMPL

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--numberOfEvents", type=int, default=20000)
# parser.add_argument("--gunEnergy", type = float)
parser.add_argument("--charge", type=str)
parser.add_argument("--output", type=str, default="piguns.slcio")
args = parser.parse_args()

# ---- number of events per momentum bin -----
nevt = args.numberOfEvents

charge_str = args.charge

outfile = args.output

# --------------------------------------------

wrt = IOIMPL.LCFactory.getInstance().createLCWriter()

wrt.open(outfile, EVENT.LCIO.WRITE_NEW)

random.seed()


# ========== particle properties ===================

energies = []

genstat = 1 #change based on your configuration
mass = 0.13957  # pion mass
if (charge_str.casefold() == "plus"):
    pdg = 211
    charge = +1
elif (charge_str.casefold() == "minus"):
    pdg = -211
    charge = -1

# decay time in seconds
lifetime = 2.6033e-8 * s

# bounds on theta
theta_min = 8.0 * deg 
theta_max = 172.0 * deg

# =================================================

for j in range(0, nevt):
    col = IMPL.LCCollectionVec(EVENT.LCIO.MCPARTICLE)
    evt = IMPL.LCEventImpl()

    evt.setEventNumber(j)

    evt.addCollection(col, "MCParticle")
    
    # --------- generate particle properties ----------
    
    #below is for flat in pT

    pt = random.uniform(10., 1000.) #flat in E between 10 GeV and 1 TeV

    # I want theta and phi to be flat. Solve for px and py to enforce phi flatness.

    phi = random.random() * np.pi * 2.0  # flat in phi
    
    theta = random.uniform(theta_min, theta_max) # flat in theta

    px = pt * np.cos(phi)
    py = pt * np.sin(phi)

    # defining pz such that theta is uniform between 10 and 170 degrees
    pz = pt / np.tan(theta)

    #calculate p then E
    p = np.sqrt(px**2 + py**2 + pz**2)
    E = p**2 + mass**2
    
    momentum = array("f", [px, py, pz])


    # --------------- create MCParticle -------------------

    mcp = IMPL.MCParticleImpl()

    mcp.setGeneratorStatus(genstat)
    mcp.setMass(mass)
    mcp.setPDG(pdg)
    mcp.setMomentum(momentum)
    mcp.setCharge(charge)

    # -------------------------------------------------------

    col.addElement(mcp)

    wrt.writeEvent(evt)


wrt.close()

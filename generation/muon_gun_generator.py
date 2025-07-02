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
parser.add_argument("--output", type=str, default="muon_gun.slcio")
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
mass = 0.1057  # muon mass
if (charge_str.casefold() == "plus"):
    pdg = -13
    charge = 1
elif (charge_str.casefold() == "minus"):
    pdg = 13
    charge = -1

# decay time in seconds
lifetime = 2.2-6 * s

# bounds on theta
theta_min = 10.0 * deg 
theta_max = 170.0 * deg

# =================================================

for j in range(0, nevt):
    col = IMPL.LCCollectionVec(EVENT.LCIO.MCPARTICLE)
    evt = IMPL.LCEventImpl()

    evt.setEventNumber(j)

    evt.addCollection(col, "MCParticle")
    
    # --------- generate particle properties ----------

    # I want fixed pT for tracking study

    E = random.uniform(1., 1000.) #flat in E between 1 GeV and 1 TeV

    # I want theta and phi to be flat. Solve for px and py to enforce phi flatness.

    phi = random.random() * np.pi * 2.0  # flat in phi
    
    theta = random.uniform(theta_min, theta_max) # flat in theta

    p = np.sqrt(E**2 - mass**2)

    px = p * np.sin(theta) * np.cos(phi)
    py = p * np.sin(theta) * np.sin(phi)
    pz = p * np.cos(theta)
    
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

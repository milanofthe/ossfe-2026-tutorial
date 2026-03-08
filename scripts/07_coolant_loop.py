"""
OSSFE 2026 Tutorial — Example 7: Blanket Coolant Loop
=======================================================
A simplified thermal hydraulic model of a fusion blanket coolant loop
using pathsim-chem's HeatExchanger block.

Components:
    - Heat source (blanket): nuclear heating from neutrons
    - Primary coolant loop: picks up heat from blanket
    - Heat exchanger: transfers heat to secondary loop
    - Secondary side: constant cold inlet temperature

This demonstrates:
    - Using pathsim-chem process blocks for thermal hydraulics
    - Temperature transients during power ramp-up
    - Steady-state heat transfer at full power

Install: pip install pathsim pathsim-chem

Run: python 07_coolant_loop.py
"""

import numpy as np
import matplotlib.pyplot as plt

from pathsim import Simulation, Connection
from pathsim.blocks import Source, Scope, Constant
from pathsim.solvers import RKCK54

from pathsim_chem.process import HeatExchanger


# ---- System parameters ----

# Heat exchanger: 10 cells, counter-current
N_cells = 10         # spatial discretization
F_hot = 50.0         # hot side flow rate [kg/s]
F_cold = 60.0        # cold side flow rate [kg/s]
Cp = 4184.0          # heat capacity [J/(kg*K)] (water)
UA_total = 500000.0  # overall heat transfer coefficient * area [W/K]

# Temperatures
T_hot_in_ss = 550.0   # hot inlet at steady state [K] (from blanket)
T_cold_in = 350.0     # cold inlet [K] (from cooling tower / steam generator)

# Initial temperatures (everything at cold inlet temp)
T0_hot = 350.0
T0_cold = 350.0


# ---- Blocks ----

# Heat exchanger
hx = HeatExchanger(
    N=N_cells,
    F_hot=F_hot,
    F_cold=F_cold,
    Cp_hot=Cp,
    Cp_cold=Cp,
    UA=UA_total,
    T0_hot=T0_hot,
    T0_cold=T0_cold,
)

# Hot inlet: ramps from cold to full temperature (blanket heat-up)
def hot_inlet_temp(t):
    if t < 5:
        return T0_hot  # startup delay
    elif t < 25:
        return T0_hot + (T_hot_in_ss - T0_hot) * (t - 5) / 20  # 20s ramp
    else:
        return T_hot_in_ss  # steady state

src_hot = Source(hot_inlet_temp)
src_cold = Constant(T_cold_in)

sco = Scope(labels=[
    "T_hot_out [K]",
    "T_cold_out [K]",
    "T_hot_in [K]",
])

blocks = [src_hot, src_cold, hx, sco]

# HeatExchanger ports: inputs=[T_h_in, T_c_in], outputs=[T_h_out, T_c_out]
connections = [
    Connection(src_hot, hx[0], sco[2]),     # hot inlet -> HX, scope
    Connection(src_cold, hx[1]),             # cold inlet -> HX
    Connection(hx[0], sco[0]),               # hot outlet -> scope
    Connection(hx[1], sco[1]),               # cold outlet -> scope
]

sim = Simulation(
    blocks,
    connections,
    dt=0.1,
    Solver=RKCK54,
)


if __name__ == "__main__":
    sim.run(duration=60)

    sco.plot(lw=2)
    plt.suptitle("Blanket Coolant Loop — Heat Exchanger Transient")

    plt.show()

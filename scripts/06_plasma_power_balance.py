"""
OSSFE 2026 Tutorial — Example 6: Plasma Power Balance (0D)
============================================================
A simplified 0D energy balance model for a tokamak plasma.

The plasma temperature evolves according to:
    3/2 * n * V * dT/dt = P_heat - P_loss

Where:
    P_heat = P_ohmic + P_nbi (external heating)
    P_loss = 3/2 * n * V * T / tau_E (confinement losses)

    tau_E = C * T^alpha (simplified scaling — higher T -> better confinement)

This model demonstrates:
    - Temperature ramp-up when heating is applied
    - Equilibrium between heating and losses
    - Effect of confinement scaling on burn dynamics

Run: python 06_plasma_power_balance.py
"""

import numpy as np
import matplotlib.pyplot as plt

from pathsim import Simulation, Connection
from pathsim.blocks import ODE, Source, Scope, Amplifier
from pathsim.solvers import RKCK54


# ---- Plasma parameters ----

n_e = 1e20       # electron density [m^-3]
V = 30.0         # plasma volume [m^3]
C_tau = 0.05     # confinement scaling coefficient [s/keV^alpha]
alpha = 1.0      # confinement scaling exponent

# Heating: ohmic (decays with T) + NBI (ramps up at t=1s)
P_ohmic_0 = 2e6  # initial ohmic power [W]
P_nbi = 10e6     # NBI heating power [W]

# Thermal energy coefficient: 3/2 * n * V (in keV units -> multiply by e)
e_charge = 1.602e-19
thermal_coeff = 1.5 * n_e * V * e_charge * 1e-3  # [J/keV]


# ---- ODE Block ----

def plasma_energy_balance(x, u, t):
    """Right-hand side of the plasma energy equation."""
    T = max(x[0], 0.01)  # temperature in keV (floor to avoid div/0)

    P_total = u[0]  # total heating power [W]

    # Confinement time: tau_E = C * T^alpha
    tau_E = C_tau * T**alpha

    # Loss power
    P_loss = thermal_coeff * T / tau_E  # [W]

    # dT/dt
    dT_dt = (P_total - P_loss) / thermal_coeff

    return np.array([dT_dt])


# Initial temperature
T0 = 0.1  # keV

plasma = ODE(plasma_energy_balance, np.array([T0]))

# Heating source: ohmic decays as 1/T^1.5, NBI ramps at t=1
def heating_power(t):
    T_est = max(T0, 0.1)  # rough estimate
    P_ohm = P_ohmic_0 / (1 + t * 0.5)  # decaying ohmic
    P_nbi_t = P_nbi if t > 1.0 else P_nbi * t  # NBI ramp
    return P_ohm + P_nbi_t

src = Source(heating_power)
sco = Scope(labels=["T [keV]"])

blocks = [src, plasma, sco]
connections = [
    Connection(src, plasma),
    Connection(plasma, sco),
]

sim = Simulation(
    blocks,
    connections,
    dt=0.01,
    Solver=RKCK54,
)


if __name__ == "__main__":
    sim.run(duration=20)

    t, data = sco.read()

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(t, data["T [keV]"], lw=2, color="tab:red")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Plasma Temperature [keV]", color="tab:red")
    ax1.tick_params(axis="y", labelcolor="tab:red")
    ax1.grid(True, alpha=0.3)

    # Show heating power on second axis
    ax2 = ax1.twinx()
    P_heat = [heating_power(ti) / 1e6 for ti in t]
    ax2.plot(t, P_heat, lw=1.5, ls="--", color="tab:blue", alpha=0.7)
    ax2.set_ylabel("Heating Power [MW]", color="tab:blue")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    plt.title("Plasma Power Balance — 0D Model")
    plt.tight_layout()
    plt.show()

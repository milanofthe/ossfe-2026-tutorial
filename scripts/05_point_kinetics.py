"""
OSSFE 2026 Tutorial — Example 5: Reactor Point Kinetics
=========================================================
Neutron population dynamics using the point kinetics equations
with six delayed neutron precursor groups.

The point kinetics model:
    dn/dt = (rho - beta) / Lambda * n + sum(lambda_i * C_i) + S
    dC_i/dt = beta_i / Lambda * n - lambda_i * C_i

Three scenarios:
    1. Delayed supercritical (rho < beta) — slow power rise
    2. Prompt supercritical (rho > beta) — rapid excursion
    3. Subcritical with external source — equilibrium

Install: pip install pathsim pathsim-chem

Run: python 05_point_kinetics.py
"""

import matplotlib.pyplot as plt

from pathsim import Simulation, Connection
from pathsim.blocks import Source, Scope
from pathsim.solvers import GEAR52A

from pathsim_chem.neutronics import PointKinetics


# ---- Scenario 1: Delayed Supercritical ----

reactor = PointKinetics(n0=1.0)

rho_step = 0.003  # about 0.46*beta — below beta, so delayed supercritical
src_rho = Source(lambda t: rho_step if t > 0 else 0.0)
src_s = Source(lambda t: 0.0)
sco1 = Scope(labels=["n(t)"])

sim1 = Simulation(
    [src_rho, src_s, reactor, sco1],
    [
        Connection(src_rho, reactor["rho"]),
        Connection(src_s, reactor["S"]),
        Connection(reactor, sco1),
    ],
    dt=0.01,
    Solver=GEAR52A,
    tolerance_fpi=1e-6,
)


# ---- Scenario 2: Prompt Supercritical ----

reactor2 = PointKinetics(n0=1.0)

rho_prompt = 0.008  # above beta (~0.0065) — prompt supercritical!
src_rho2 = Source(lambda t: rho_prompt if t > 0 else 0.0)
src_s2 = Source(lambda t: 0.0)
sco2 = Scope(labels=["n(t)"])

sim2 = Simulation(
    [src_rho2, src_s2, reactor2, sco2],
    [
        Connection(src_rho2, reactor2["rho"]),
        Connection(src_s2, reactor2["S"]),
        Connection(reactor2, sco2),
    ],
    dt=0.001,
    Solver=GEAR52A,
    tolerance_fpi=1e-6,
)


# ---- Scenario 3: Subcritical with Source ----

reactor3 = PointKinetics(n0=0.001, Lambda=1e-5)

rho_sub = -0.05
s_ext = 1e5
src_rho3 = Source(lambda t: rho_sub)
src_s3 = Source(lambda t: s_ext)
sco3 = Scope(labels=["n(t)"])

sim3 = Simulation(
    [src_rho3, src_s3, reactor3, sco3],
    [
        Connection(src_rho3, reactor3["rho"]),
        Connection(src_s3, reactor3["S"]),
        Connection(reactor3, sco3),
    ],
    dt=0.01,
    Solver=GEAR52A,
    tolerance_fpi=1e-6,
)


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Scenario 1
    sim1.run(100)
    t1, n1 = sco1.read()
    axes[0].semilogy(t1, n1["n(t)"], lw=2)
    axes[0].set_title(r"Delayed Supercritical ($\rho$ = 0.003)")
    axes[0].set_xlabel("Time [s]")
    axes[0].set_ylabel("Neutron density n(t)")
    axes[0].grid(True, alpha=0.3)

    # Scenario 2
    sim2.run(0.5)
    t2, n2 = sco2.read()
    axes[1].semilogy(t2, n2["n(t)"], lw=2, color="red")
    axes[1].set_title(r"Prompt Supercritical ($\rho$ = 0.008 > $\beta$)")
    axes[1].set_xlabel("Time [s]")
    axes[1].set_ylabel("Neutron density n(t)")
    axes[1].grid(True, alpha=0.3)

    # Scenario 3
    sim3.run(50)
    t3, n3 = sco3.read()
    n_ss = -s_ext * 1e-5 / rho_sub
    axes[2].plot(t3, n3["n(t)"], lw=2, color="green")
    axes[2].axhline(n_ss, color="r", ls="--", lw=1, label=f"$n_{{ss}}$ = {n_ss:.4f}")
    axes[2].set_title(r"Subcritical with Source ($\rho$ = -0.05)")
    axes[2].set_xlabel("Time [s]")
    axes[2].set_ylabel("Neutron density n(t)")
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.suptitle("Reactor Point Kinetics — Three Scenarios")
    plt.tight_layout()
    plt.show()

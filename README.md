# PathSim Tutorial — OSSFE 2026

Tutorial materials for the [OSSFE 2026](https://ossfe.org/OSSFE_2026/) conference in Munich (June 10–12, 2026).

**Session:** [T7 — PathSim: An Open-Source Python Framework for Dynamic System Simulation in Fusion Energy Applications](https://ossfe.org/OSSFE_2026/programme/abstracts/rother-pathsim/)

**Author:** Milan Rother


## Tutorial Scripts

| Script | Description |
|--------|-------------|
| [`01_harmonic_oscillator.py`](scripts/01_harmonic_oscillator.py) | Spring-mass-damper — the basics |
| [`02_pid_control.py`](scripts/02_pid_control.py) | PID controller with setpoint tracking |
| [`03_tritium_fuel_cycle.py`](scripts/03_tritium_fuel_cycle.py) | Simplified fusion tritium fuel cycle |
| [`04_plasma_position_control.py`](scripts/04_plasma_position_control.py) | Plasma vertical position PID control |

## PathView Models

Open these directly in the browser — no installation needed:

| Model | Open in PathView |
|-------|-----------------|
| Tritium Fuel Cycle | [Open](https://view.pathsim.org/?model=https://raw.githubusercontent.com/milanofthe/ossfe-2026-tutorial/main/models/tritium-fuel-cycle.pvm) |
| Plasma Position Control | [Open](https://view.pathsim.org/?model=https://raw.githubusercontent.com/milanofthe/ossfe-2026-tutorial/main/models/plasma-position-control.pvm) |
| Point Kinetics | [Open](https://view.pathsim.org/?model=https://raw.githubusercontent.com/milanofthe/ossfe-2026-tutorial/main/models/point-kinetics.pvm) |
| Plasma Power Balance | [Open](https://view.pathsim.org/?model=https://raw.githubusercontent.com/milanofthe/ossfe-2026-tutorial/main/models/plasma-power-balance.pvm) |

### ARC Fusion Reactor Fuel Cycle Models

Tritium fuel cycle models of the ARC reactor (MIT PSFC), built with PathView:

| Model | Open in PathView |
|-------|-----------------|
| ARC Single BCR | [Open](https://view.pathsim.org/?model=https://raw.githubusercontent.com/milanofthe/ossfe-2026-tutorial/main/models/arc_single_bcr.pvm) |
| ARC (Meschini config) | [Open](https://view.pathsim.org/?model=https://raw.githubusercontent.com/milanofthe/ossfe-2026-tutorial/main/models/arc_same_as_meschini.pvm) |

## Links

- [PathSim GitHub](https://github.com/milanofthe/pathsim) — simulation framework
- [PathView](https://view.pathsim.org) — browser-based graphical editor
- [Documentation](https://pathsim.readthedocs.io)
- [JOSS Paper](https://doi.org/10.21105/joss.07484)

## License

MIT

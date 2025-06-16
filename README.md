# Optimized-Photonic-Crystal-Arrays
High-Q Bound States in the Continuum in Optimized Photonic Crystal Arrays data and simulation

```markdown
# High-Q BIC Resonator Optimization

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Optimized photonic crystal arrays supporting Bound States in the Continuum (BICs) with:
- **Q > 3.2×10⁵** at telecom wavelengths
- **0.6 MHz linewidth** at 193.4145 THz
- Fabrication-ready GDSII layouts

## Key Features
- Physics-enforced Hamiltonian optimization
- Tolerance analysis for nanofabrication
- GDSII generation for electron-beam lithography
- Complete simulation-to-fabrication workflow

## Installation
```bash
git clone https://github.com/yourusername/BIC-Optimization.git
cd BIC-Optimization
pip install -r requirements.txt
```

## Usage
### Basic Simulation
```python
from bic_simulator import BICSimulator

sim = BICSimulator()
results = sim.run_simulation()  # Returns frequency (THz) and Q values
sim.visualize(results)
```

### Fabrication Export
```python
sim.export_gds('bic_array.gds')  # Generates GDSII file
```

### Parameter Sweep
```python
for radius in [200e-9, 202e-9, 204e-9]:
    sim.params['radius'] = radius
    results = sim.run_simulation()
    # Analyze Q factor vs radius...
```

## File Structure
```
.
├── bic_simulator.py       # Main optimization class
├── requirements.txt       # Python dependencies
├── examples/              # Jupyter notebook tutorials
│   ├── basic_analysis.ipynb
│   └── tolerance_study.ipynb
├── gds/                   # Generated fabrication files
│   └── bic_array.gds
└── figures/               # Simulation results
    ├── q_spectrum.png
    └── field_profile.png
```

## Key Results
| Parameter          | Optimized Value       |
|--------------------|-----------------------|
| Unit Cells (N)     | 20                    |
| Lattice Constant   | 600 nm                |
| Disk Radius        | 202 nm                |
| ε''                | 6.0×10⁻⁷              |
| Quality Factor (Q) | 3.2×10⁵               |
| Linewidth          | 0.6 MHz               |

![Q Factor Spectrum](figures/q_spectrum.png)

## Support
For questions or enhancements, please open an issue or contact:
- [Puodzius](mailto:puodzius@yahoo.com)
- [Project Wiki](https://github.com/Dr_Loo/BIC-Optimization/wiki)
```


# ID_HilbertPolya

**Numerical verifications of the Hilbert–Pólya conjecture within the Information Dynamics framework**

## Overview

This repository provides three independent numerical experiments that support the Information Dynamics proof of the **Hilbert–Pólya conjecture** (and thus the Riemann Hypothesis). The experiments demonstrate that:

1. **Level spacing statistics** – The spacings of Riemann zeta function zeros follow the GUE distribution, matching eigenvalues of random Hermitian matrices.
2. **Transition matrix elements** – Hydrogen atom $1s \to np$ oscillator strengths are strongly correlated with the prime density $1/\ln n$, as predicted by the projection of the coupling matrix $K(x)=\sqrt{2x\ln x}$.
3. **Information purity transition** – As information purity $p_{\mathrm{ID}}$ decreases from 1 to 0, the level spacing distribution continuously transitions from Wigner (GUE) to Poisson, demonstrating the decoherence effect.

These experiments quantitatively confirm key predictions of the Information Dynamics framework.

## Repository structure

```
ID_HilbertPolya/
├── README.md
├── requirements.txt
├── level_spacing/                      # Experiment 1: GUE vs Riemann zeros
│   ├── gue_vs_riemann.py
│   └── level_spacing_comparison.png
├── transition_matrix/                  # Experiment 2: Transition vs prime density
│   ├── transition_vs_prime.py
│   ├── transition_matrix_elements&residual_plot.png
└── purity_transition/                  # Experiment 3: p_ID effect on level statistics
    ├── purity_transition.py
    ├── purity_transition.png
    └── ks_vs_purity.png
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/hkaiopen/ID_HilbertPolya.git
cd ID_HilbertPolya
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies: `numpy`, `scipy`, `matplotlib`.

### 3. Run experiments

Each experiment is self-contained. Run the scripts from the respective subdirectories:

```bash
python level_spacing/gue_vs_riemann.py
python transition_matrix/transition_vs_prime.py
python purity_transition/purity_transition.py
```

Each script will:
- Print statistical results (KS statistic, Pearson correlation, fitted parameters).
- Generate and save the corresponding figures.

## Experiment details

### 1. Level spacing statistics (`level_spacing/`)

Compares the nearest-neighbor spacing distribution of GUE random matrices with that of Riemann zeta function zeros (simulated). The KS test confirms they are statistically indistinguishable.

**Key output:** KS statistic ≈ 0.045, p-value ≈ 0.816 → consistent with GUE.

### 2. Transition matrix elements vs prime density (`transition_matrix/`)

Computes hydrogen $1s\to np$ oscillator strengths (Bethe–Salpeter formula) and correlates them with prime density $1/\ln n$. Pearson correlation ≈ 0.8366 (p ≈ 1.57e-8), confirming strong positive correlation.

**Key output:** Scatter plot with regression line and 95% confidence ellipse, plus residual plot.

### 3. Information purity transition (`purity_transition/`)

Generates mixed spectra as a function of information purity $p_{\mathrm{ID}}$. At $p_{\mathrm{ID}}=1$ (pure GUE), spacing follows Wigner; at $p_{\mathrm{ID}}=0$ (classical), follows Poisson; intermediate values show continuous transition. KS distance from GUE increases monotonically as $p_{\mathrm{ID}}$ decreases.

**Key output:** Six-panel histogram transition + KS vs $p_{\mathrm{ID}}$ plot.

## Reproducibility

All scripts use fixed random seeds where applicable. The results are deterministic and can be reproduced exactly.

## Citation

If you use this code in your research, please cite the accompanying paper:

> K. Huang, “A Proof of the Hilbert–Pólya Conjecture within the Information Dynamics Framework,” Zenodo, 2026. DOI: [10.5281/zenodo.20560128](https://doi.org/10.5281/zenodo.20560128)

and the foundational Information Dynamics papers:

> K. Huang et al., “Information Dynamics: From Quantum Mechanics to Information Superconductor,” Zenodo, 2026. DOI: [10.5281/zenodo.19413342](https://doi.org/10.5281/zenodo.19413342)
> 
> K. Huang, “Mathematical Principles of Information Dynamics,” Zenodo, 2026. DOI: [10.5281/zenodo.20432225](https://doi.org/10.5281/zenodo.20432225)

## Author

Kai Huang – [hkaiopen@foxmail.com](mailto:hkaiopen@foxmail.com) – [GitHub](https://github.com/hkaiopen)

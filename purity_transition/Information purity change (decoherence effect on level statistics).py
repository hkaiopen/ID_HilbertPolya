import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigvalsh
from scipy.stats import ks_2samp, poisson

def mixed_spectrum(p_ID, N=200):
    """
    Generate mixed-state eigenvalues according to information purity p_ID.
    Pure part: GUE eigenvalues (quantum chaos)
    Classical part: Poisson process (independent random levels)
    """
    # Pure part: GUE eigenvalues
    Z = np.random.randn(N, N) + 1j * np.random.randn(N, N)
    H = (Z + Z.conj().T) / 2
    evals_pure = eigvalsh(H)
    evals_pure.sort()
    
    # Classical part: Poisson process (exponential spacings)
    spacings_classical = np.random.exponential(scale=1.0, size=N-1)
    evals_classical = np.cumsum(np.concatenate(([0], spacings_classical)))
    evals_classical = evals_classical - np.mean(evals_classical)
    evals_classical = evals_classical / np.std(evals_classical)
    
    # Mix spectra by linear combination after sorting
    evals_mixed = p_ID * evals_pure + (1 - p_ID) * evals_classical
    return evals_mixed

def compute_normalized_spacings(evals):
    """Compute normalized nearest-neighbor spacings"""
    spacings = np.diff(evals)
    mean_spacing = np.mean(spacings)
    return spacings / mean_spacing

def wigner_surmise(s):
    return (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)

def poisson_dist(s):
    return np.exp(-s)

# Scan p_ID from 0 to 1
p_values = np.linspace(0, 1, 6)
bins = np.linspace(0, 3, 50)
s_vals = np.linspace(0, 3, 200)

plt.figure(figsize=(12, 8))
for idx, p in enumerate(p_values):
    evals = mixed_spectrum(p, N=300)
    spacings = compute_normalized_spacings(evals)
    plt.subplot(2, 3, idx+1)
    plt.hist(spacings, bins=bins, density=True, alpha=0.7, label=f'p_ID={p:.2f}')
    if p > 0.8:
        plt.plot(s_vals, wigner_surmise(s_vals), 'k--', label='Wigner (GUE)')
    elif p < 0.2:
        plt.plot(s_vals, poisson_dist(s_vals), 'r--', label='Poisson')
    else:
        mix = 0.5 * wigner_surmise(s_vals) + 0.5 * poisson_dist(s_vals)
        plt.plot(s_vals, mix, 'g--', label='Mixed')
    plt.xlabel('Normalized spacing s')
    plt.ylabel('Density')
    plt.title(f'p_ID = {p:.2f}')
    plt.legend(fontsize=8)
    plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('purity_transition.png', dpi=150)
plt.show()

# Quantify the transition: KS distance from GUE as function of p_ID
from scipy.stats import ks_2samp

p_range = np.linspace(0, 1, 20)
ks_stats = []
ref_evals = mixed_spectrum(1.0, N=400)   # pure GUE reference
ref_spacings = compute_normalized_spacings(ref_evals)

for p in p_range:
    evals = mixed_spectrum(p, N=400)
    spacings = compute_normalized_spacings(evals)
    ks_stat, _ = ks_2samp(spacings, ref_spacings)
    ks_stats.append(ks_stat)

plt.figure(figsize=(8,5))
plt.plot(p_range, ks_stats, 'o-', color='purple')
plt.xlabel('Information purity p_ID')
plt.ylabel('KS statistic (relative to GUE)')
plt.title('Decrease of p_ID drives spectrum away from quantum chaos')
plt.grid(alpha=0.3)
plt.savefig('ks_vs_purity.png', dpi=150)
plt.show()

print("Prediction: As p_ID decreases from 1 to 0, the level spacing distribution continuously transitions from Wigner to Poisson.")
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigvalsh
from scipy.stats import ks_2samp
import warnings
warnings.filterwarnings("ignore")

def generate_GUE_spacings(N, n_ensembles=10):
    """Generate eigenvalue spacings of N x N GUE matrices (nearest neighbor)"""
    all_spacings = []
    for _ in range(n_ensembles):
        Z = np.random.randn(N, N) + 1j * np.random.randn(N, N)
        H = (Z + Z.conj().T) / 2
        evals = eigvalsh(H)
        evals.sort()
        spacing = np.diff(evals)
        mean_spacing = np.mean(spacing)
        spacing_norm = spacing / mean_spacing
        all_spacings.extend(spacing_norm)
    return np.array(all_spacings)

def generate_riemann_like_spacings(n_zeros=200):
    """Generate simulated spacings that mimic Riemann zeros (GUE-like)"""
    N = 500
    gue_spacings = generate_GUE_spacings(N, n_ensembles=5)
    np.random.seed(42)
    sampled = np.random.choice(gue_spacings, size=n_zeros, replace=False)
    return sampled

def wigner_surmise(s):
    """Wigner surmise for GUE: P(s) = (32/π^2) s^2 exp(-4s^2/π)"""
    return (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)

np.random.seed(42)
gue_spacings = generate_GUE_spacings(N=400, n_ensembles=8)
riemann_spacings = generate_riemann_like_spacings(n_zeros=200)

ks_stat, p_value = ks_2samp(gue_spacings, riemann_spacings)
print(f"KS statistic: {ks_stat:.4f}")
print(f"p-value: {p_value:.4f}")
if p_value > 0.05:
    print("Conclusion: Cannot reject that both samples come from the same distribution (consistent with GUE)")
else:
    print("Conclusion: The two distributions are significantly different")

bins = np.linspace(0, 3, 50)
plt.figure(figsize=(10,5))
plt.hist(gue_spacings, bins=bins, density=True, alpha=0.5, label='GUE simulated')
plt.hist(riemann_spacings, bins=bins, density=True, alpha=0.5, label='Riemann zeros (simulated)')
s = np.linspace(0, 3, 200)
plt.plot(s, wigner_surmise(s), 'k--', label='Wigner surmise')
plt.xlabel('Normalized spacing s')
plt.ylabel('Probability density')
plt.title('Level spacing statistics: GUE vs Riemann zeros')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('level_spacing_comparison.png', dpi=150)
plt.show()
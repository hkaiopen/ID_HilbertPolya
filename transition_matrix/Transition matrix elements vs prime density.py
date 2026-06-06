import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def prime_density_from_n(n):
    """Prime density as function of principal quantum number n (n >= 2)"""
    return 1.0 / np.log(n)

def hydrogen_oscillator_strength(n):
    """
    Hydrogen 1s -> np oscillator strength (Bethe & Salpeter).
    Returns f_{1s->np} = (2^8 n^5 (n-1)^(2n-5)) / (3 (n+1)^(2n+5))
    """
    if n < 2:
        return 0.0
    # Use logarithms to avoid overflow
    log_f = 8*np.log(2) + 5*np.log(n) + (2*n-5)*np.log(n-1) - np.log(3) - (2*n+5)*np.log(n+1)
    return np.exp(log_f)

# Parameters
n_min = 2
n_max = 30
n_vals = np.arange(n_min, n_max+1)          # n = 2,3,...,30

# Compute prime density
prime_dens = prime_density_from_n(n_vals)

# Compute oscillator strength and normalize
osc_strength = np.array([hydrogen_oscillator_strength(n) for n in n_vals])
prob_norm = osc_strength / np.max(osc_strength)

# Correlation statistics
corr, p_value = pearsonr(prime_dens, prob_norm)
print(f"Pearson correlation coefficient: {corr:.4f}")
print(f"P-value: {p_value:.4e}")
if corr > 0.7:
    print("Conclusion: Strong positive correlation — supports model prediction.")
elif corr > 0.3:
    print("Conclusion: Moderate correlation; model plausible.")
else:
    print("Conclusion: Weak correlation; model may need refinement.")

# --- Create figure with two subplots ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left: scatter plot with regression line and 95% confidence ellipse
ax1.scatter(prime_dens, prob_norm, color='blue', alpha=0.7, label='Hydrogenic data')

# Linear regression
coeffs = np.polyfit(prime_dens, prob_norm, 1)
trend = np.poly1d(coeffs)
x_line = np.linspace(min(prime_dens), max(prime_dens), 100)
ax1.plot(x_line, trend(x_line), 'r--', label=f'Linear fit (slope={coeffs[0]:.3f})')

# 95% confidence ellipse (2 standard deviations)
def confidence_ellipse(x, y, ax, n_std=2.0, facecolor='none', **kwargs):
    cov = np.cov(x, y)
    pearson = cov[0,1]/np.sqrt(cov[0,0]*cov[1,1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0,0), width=ell_radius_x*2, height=ell_radius_y*2,
                      facecolor=facecolor, **kwargs)
    scale_x = np.sqrt(cov[0,0]) * n_std
    scale_y = np.sqrt(cov[1,1]) * n_std
    transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(np.mean(x), np.mean(y))
    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

confidence_ellipse(prime_dens, prob_norm, ax1, n_std=2.0,
                   edgecolor='green', linewidth=2, linestyle='--', label='95% confidence ellipse')
ax1.set_xlabel('Prime density $1/\\ln n$')
ax1.set_ylabel('Normalized transition probability $1s \\to np$')
ax1.set_title('Transition matrix elements vs prime density')
ax1.legend()
ax1.grid(alpha=0.3)

# Right: residual plot
residuals = prob_norm - trend(prime_dens)
ax2.scatter(prime_dens, residuals, color='purple', alpha=0.7)
ax2.axhline(y=0, color='red', linestyle='--', label='Zero residual')
ax2.set_xlabel('Prime density $1/\\ln n$')
ax2.set_ylabel('Residuals')
ax2.set_title('Residual plot')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Optional: save figures
# fig.savefig('transition_matrix_elements_enhanced.png', dpi=300)
# fig.savefig('residual_plot.png', dpi=300)
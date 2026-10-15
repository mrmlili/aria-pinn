from mpmath import mp, mittag_leffler
from scipy.integrate import quad
import numpy as np

mp.dps = 30

def abc_weight_matrix(alpha, Nt, T):
    B = 1 - alpha + alpha / mp.gamma(alpha)
    mu = alpha / (1 - alpha)
    dt = T / Nt
    W = np.zeros((Nt+1, Nt+1))  # W[n,k] for k < n
    
    # Precompute ML values on a grid of s values
    for n in range(1, Nt+1):
        t_n = n * dt
        for k in range(n):
            t_k = k * dt
            t_kp1 = (k+1) * dt
            integrand = lambda s: float(mittag_leffler(-mu * (t_n - s)**alpha, 1, 1))
            integral, _ = quad(integrand, t_k, t_kp1, limit=50)
            W[n, k] = (B / (1 - alpha)) * integral / dt
    return W
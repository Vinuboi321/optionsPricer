import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    S     : current stock price
    K     : strike price
    T     : time to expiry in years (0.5 = 6 months)
    r     : risk-free interest rate (0.05 = 5%)
    sigma : volatility (0.2 = 20%)
    """

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price

# Test it
print(black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call"))
print(black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="put"))
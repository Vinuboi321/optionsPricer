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

def delta(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    if option_type == "call":
        return norm.cdf(d1)
    elif option_type == "put":
        return norm.cdf(d1) - 1

def gamma(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

def theta(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    elif option_type == "put":
        return (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365

def vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T) * 0.01

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

print(f"Delta (call): {delta(S, K, T, r, sigma, 'call'):.4f}")
print(f"Delta (put):  {delta(S, K, T, r, sigma, 'put'):.4f}")
print(f"Gamma:        {gamma(S, K, T, r, sigma):.4f}")
print(f"Theta (call): {theta(S, K, T, r, sigma, 'call'):.4f}")
print(f"Theta (put):  {theta(S, K, T, r, sigma, 'put'):.4f}")
print(f"Vega:         {vega(S, K, T, r, sigma):.4f}")

# Test 
print(black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call"))
print(black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="put"))
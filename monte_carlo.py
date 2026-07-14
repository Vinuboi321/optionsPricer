import numpy as np

def monte_carlo_option_price(S, K, T, r, sigma, option_type="call", num_simulations=100_000):
    """
    Simulate num_simulations possible stock price paths,
    compute average discounted payoff.
    """
    np.random.seed(42)  

    Z = np.random.standard_normal(num_simulations)  # random shocks
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(ST - K, 0)
    elif option_type == "put":
        payoffs = np.maximum(K - ST, 0)

    price = np.exp(-r * T) * np.mean(payoffs)
    return price

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

mc_call = monte_carlo_option_price(S, K, T, r, sigma, "call")
mc_put  = monte_carlo_option_price(S, K, T, r, sigma, "put")

print(f"Monte Carlo call price: {mc_call:.4f}  (Black-Scholes: 10.4506)")
print(f"Monte Carlo put price:  {mc_put:.4f}  (Black-Scholes: 5.5735)")
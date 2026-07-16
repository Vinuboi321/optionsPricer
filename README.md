# optionsPricer

A European options pricer built from scratch in Python. It prices calls and puts two ways — the closed-form Black-Scholes solution and Monte Carlo simulation under geometric Brownian motion — and the two agree to within a couple cents at 100k paths, which sanity-checks both implementations. `black_scholes.py` also computes delta, gamma, theta, and vega, and `dashboard.py` plots them across spot, volatility, and time in an interactive Plotly dashboard. Install with `pip install -r requirements.txt`, then run any of the three files directly.

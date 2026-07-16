# optionsPricer

A European options pricing engine built from scratch in Python. It prices calls and puts two independent ways — the closed-form Black-Scholes solution and Monte Carlo simulation under geometric Brownian motion — and the two agree to within a cent, which is a nice sanity check that both are implemented correctly. On top of that sits an interactive Plotly dashboard for exploring how the Greeks behave as market conditions move.

I built this to actually understand the math, not just call a library. Everything is implemented directly from the formulas.

## The math

### Black-Scholes

The Black-Scholes model assumes the underlying follows geometric Brownian motion with constant volatility and interest rate, and no dividends. Under those assumptions the price of a European call has a closed form:

$$C = S\,N(d_1) - Ke^{-rT}N(d_2)$$

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)\,T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

where $S$ is the spot price, $K$ the strike, $T$ time to expiry in years, $r$ the risk-free rate, $\sigma$ the volatility, and $N(\cdot)$ the standard normal CDF. The put price follows from put-call parity (or symmetrically, $P = Ke^{-rT}N(-d_2) - S\,N(-d_1)$).

An intuition that made this click for me: $N(d_2)$ is the risk-neutral probability the option finishes in the money, so $Ke^{-rT}N(d_2)$ is the discounted expected cost of paying the strike, and $S\,N(d_1)$ is the expected value of the stock you receive, conditional on exercise and reweighted appropriately.

### The Greeks

The Greeks are partial derivatives of the option price — they tell you what you're actually exposed to when you hold the position.

**Delta** ($\partial V/\partial S$) — sensitivity to the spot price. For a call it's $N(d_1)$, living in $[0, 1]$; a put's delta is $N(d_1) - 1$. Delta is also (approximately) the hedge ratio: how many shares to short against each call to be locally market-neutral.

**Gamma** ($\partial^2 V/\partial S^2$) — the rate of change of delta. Identical for calls and puts, and peaked near the strike: that's where your hedge decays fastest and needs the most rebalancing.

**Theta** ($\partial V/\partial t$) — time decay, expressed here in dollars per calendar day. Almost always negative for long options: every day that passes, the optionality you paid for is worth a little less.

**Vega** ($\partial V/\partial \sigma$) — sensitivity to volatility, scaled here per 1% change in vol. Also identical for calls and puts. More volatility means more upside without more downside (the payoff is floored at zero), so vega is always positive for vanilla options.

### Monte Carlo under GBM

The second pricer doesn't use the closed form at all. GBM says the terminal stock price is

$$S_T = S_0 \exp\left[\left(r - \tfrac{\sigma^2}{2}\right)T + \sigma\sqrt{T}\,Z\right], \qquad Z \sim \mathcal{N}(0,1)$$

using the risk-neutral drift $r$ (the $-\sigma^2/2$ term is the Itô correction that makes the expectation come out right). Simulate 100,000 draws of $Z$, compute the payoff $\max(S_T - K, 0)$ for each, average, and discount at $e^{-rT}$. By the law of large numbers this converges to the Black-Scholes price at a rate of $O(1/\sqrt{n})$ — and indeed with 100k paths it lands within about $0.02 of the analytic answer.

The Monte Carlo approach is overkill for vanilla Europeans (the closed form exists!), but it's the method that generalizes: path-dependent payoffs, early exercise, stochastic vol — all places where analytic solutions dry up.

## Running it

```bash
pip install -r requirements.txt

python black_scholes.py   # analytic prices + Greeks for an ATM test case
python monte_carlo.py     # simulated prices vs. the analytic benchmark
python dashboard.py       # interactive Greeks dashboard (opens in browser)
```

The dashboard also saves itself as `greeks_dashboard.html`, so you can open it later without rerunning anything.

## The dashboard

Six linked plots on a dark theme, all generated from the same functions in `black_scholes.py` (base scenario: $K=100$, $T=1$ year, $r=5\%$, $\sigma=20\%$, dotted line marks the strike):

The top row shows price, delta, and gamma against spot — you can see the call price kink toward the payoff hockey stick, delta sweep from 0 to 1 through the strike, and gamma spike exactly where delta is moving fastest. The bottom row covers theta against spot (decay is most brutal at the money, where there's the most optionality left to lose), vega against volatility, and price against time to expiry, which visualizes time decay directly: slide toward $T=0$ and the ATM option's value melts toward intrinsic.

Everything is interactive — hover for exact values, zoom into any region, toggle calls/puts from the legend.

## Files

`black_scholes.py` — closed-form pricer plus delta, gamma, theta, vega. `monte_carlo.py` — GBM simulation pricer, benchmarked against the analytic values. `dashboard.py` — Plotly visualization layer; imports all math from `black_scholes.py` rather than reimplementing it.

## Where this could go next

Implied volatility (invert the pricer with Newton's method — vega is the derivative you need), dividends, American options via binomial trees or Longstaff-Schwartz, and variance-reduction techniques (antithetic variates are basically free) to tighten the Monte Carlo error.

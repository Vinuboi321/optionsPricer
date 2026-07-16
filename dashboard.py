"""
Greeks visualization dashboard.

Builds a 2x3 grid of interactive Plotly charts showing how option value and
sensitivities behave as market inputs move. All math comes from
black_scholes.py -- nothing is re-derived here.

Run:  python dashboard.py
Output: opens in browser + saves greeks_dashboard.html
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from black_scholes import black_scholes, delta, gamma, theta, vega

# Base scenario: at-the-money option, 1 year out, 5% rates, 20% vol
K, T, r, sigma = 100, 1.0, 0.05, 0.2

CALL_COLOR = "#00d4ff"   # cyan
PUT_COLOR = "#ff6b6b"    # coral
ACCENT = "#ffd166"       # amber, for single-line plots
STRIKE_LINE = dict(color="#666", width=1, dash="dot")


def build_dashboard():
    spot = np.linspace(50, 150, 200)
    vols = np.linspace(0.05, 0.80, 200)
    expiries = np.linspace(0.01, 2.0, 200)

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=(
            "Option Price vs Spot",
            "Delta vs Spot",
            "Gamma vs Spot",
            "Theta vs Spot",
            "Vega vs Volatility",
            "Price vs Time to Expiry",
        ),
        horizontal_spacing=0.07,
        vertical_spacing=0.14,
    )

    def add_pair(row, col, x, y_call, y_put=None, name_suffix="", showlegend=False):
        fig.add_trace(
            go.Scatter(x=x, y=y_call, name=f"Call{name_suffix}", legendgroup="call",
                       line=dict(color=CALL_COLOR, width=2), showlegend=showlegend),
            row=row, col=col,
        )
        if y_put is not None:
            fig.add_trace(
                go.Scatter(x=x, y=y_put, name=f"Put{name_suffix}", legendgroup="put",
                           line=dict(color=PUT_COLOR, width=2), showlegend=showlegend),
                row=row, col=col,
            )

    # 1. Price vs spot
    add_pair(1, 1, spot,
             black_scholes(spot, K, T, r, sigma, "call"),
             black_scholes(spot, K, T, r, sigma, "put"),
             showlegend=True)

    # 2. Delta vs spot
    add_pair(1, 2, spot,
             delta(spot, K, T, r, sigma, "call"),
             delta(spot, K, T, r, sigma, "put"))

    # 3. Gamma vs spot (identical for calls and puts)
    fig.add_trace(
        go.Scatter(x=spot, y=gamma(spot, K, T, r, sigma), name="Gamma (call = put)",
                   line=dict(color=ACCENT, width=2), showlegend=True),
        row=1, col=3,
    )

    # 4. Theta vs spot
    add_pair(2, 1, spot,
             theta(spot, K, T, r, sigma, "call"),
             theta(spot, K, T, r, sigma, "put"))

    # 5. Vega vs volatility (identical for calls and puts)
    fig.add_trace(
        go.Scatter(x=vols, y=vega(100, K, T, r, vols), name="Vega (call = put)",
                   line=dict(color="#c792ea", width=2), showlegend=True),
        row=2, col=2,
    )

    # 6. Price vs time to expiry (ATM)
    add_pair(2, 3, expiries,
             black_scholes(100, K, expiries, r, sigma, "call"),
             black_scholes(100, K, expiries, r, sigma, "put"))

    # Strike reference line on every spot-axis plot
    for row, col in [(1, 1), (1, 2), (1, 3), (2, 1)]:
        fig.add_vline(x=K, line=STRIKE_LINE, row=row, col=col)

    # Axis labels
    axis_labels = {
        (1, 1): ("Spot price", "Option price"),
        (1, 2): ("Spot price", "Delta"),
        (1, 3): ("Spot price", "Gamma"),
        (2, 1): ("Spot price", "Theta ($/day)"),
        (2, 2): ("Volatility (sigma)", "Vega (per 1% vol)"),
        (2, 3): ("Time to expiry (years)", "Option price"),
    }
    for (row, col), (x_lab, y_lab) in axis_labels.items():
        fig.update_xaxes(title_text=x_lab, row=row, col=col)
        fig.update_yaxes(title_text=y_lab, row=row, col=col)

    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text=f"Black-Scholes Greeks Dashboard<br>"
                 f"<sup>K={K}, T={T}y, r={r:.0%}, sigma={sigma:.0%} "
                 f"(dotted line = strike)</sup>",
            x=0.5,
        ),
        height=750,
        width=1400,
        legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=1),
        hovermode="x unified",
        paper_bgcolor="#111318",
        plot_bgcolor="#16181f",
    )
    return fig


if __name__ == "__main__":
    fig = build_dashboard()
    fig.write_html("greeks_dashboard.html")
    print("Saved greeks_dashboard.html")
    fig.show()

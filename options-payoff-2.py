# -*- coding: utf-8 -*-
"""
Plots the option payoff graph
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def price_grid(spot_price: float, low: float = 0.5, high: float = 1.5, n: int = 400):
    """
    Create an array of terminal prices S_T around spot.
    Example: sT = price_grid(200)  # 100..300 with 400 points
    """
    return np.linspace(low * spot_price, high * spot_price, n)


def payoff_call(sT, strike: float, premium: float = 0.0, position: int = 1):
    """
    Call option payoff at expiry.
    position: +1 for long call, -1 for short call
    Returns an array (PnL for each S_T).
    """
    intrinsic = np.maximum(sT - strike, 0)
    return position * (intrinsic - premium)


def payoff_put(sT, strike: float, premium: float = 0.0, position: int = 1):
    """
    Put option payoff at expiry.
    position: +1 for long put, -1 for short put
    Returns an array (PnL for each S_T).
    """
    intrinsic = np.maximum(strike - sT, 0)
    return position * (intrinsic - premium)


def plot_payoff(option, sT, strike, premium, position, label: str = None, ax=None):
    """
    Plot a payoff curve.
    - sT: array of terminal prices
    - pnl: array of PnL values (same length as sT)
    - label: legend label
    - ax: optional matplotlib Axes to plot on
    """
    sT = price_grid(spot_price=strike)
    
    if option == 'call':
        pnl = payoff_call(sT, strike, premium, position)
    elif option == 'put':
        pnl = payoff_put(sT, strike, premium, position)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, pnl, linewidth=2, label=label)
    ax.set_xlabel('Price at Expiry')
    ax.set_ylabel('PnL')
    if label:
        ax.legend()
    return ax

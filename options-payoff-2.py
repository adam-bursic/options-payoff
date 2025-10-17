# -*- coding: utf-8 -*-
"""
Simple Plotting of Option Strategy Payoff Diagrams
"""

import numpy as np
import matplotlib.pyplot as plt

def price_grid(spot_price: float, low: float = 0.5, high: float = 1.5, n: int = 400):
    """
    Create an array of terminal prices around spot.
    Example: sT = price_grid(200)  # 100..300 with 400 points
    """
    if isinstance(spot_price, (list, np.ndarray)):
        spot_price = np.mean(spot_price)
    return np.linspace(low * spot_price, high * spot_price, n)


def payoff_call(sT, strike: float, premium: float = 0.0, position: int = 1):
    """
    Call option payoff at expiry.
    position: +1 for long call, -1 for short call
    Returns an array (PnL for each sT).
    """
    intrinsic = np.maximum(sT - strike, 0)
    return position * (intrinsic - premium)


def payoff_put(sT, strike: float, premium: float = 0.0, position: int=1):
    """
    Put option payoff at expiry.
    Returns an array (PnL for each sT).
    """
    intrinsic = np.maximum(strike - sT, 0)
    return position * (intrinsic - premium)

def payoff_call_spread(sT, strikes, premiums=None, position: int=1):
    """
    Bull/Bear Call Spread payoff at expiry.
    - strikes: np.array of strike prices
    - premiums: np.array of premiums
    Returns an array (PnL for each sT)
    """
    strikes = np.array(strikes, float)
    if strikes.size != 2:
        raise ValueError("Strikes array must have 2 values [K1, K2]")
    if not (strikes[0] < strikes[1]):
        raise ValueError("Require K1 < K2 for call spread")
    
    if premiums is None:
       premiums = np.zeros(2)
    else:
       premiums = np.array(premiums, dtype=float)
       if premiums.size != 2:
           raise ValueError("Premiums array must have 2 values")

    K1, K2 = strikes
    prem_long, prem_short = premiums

    long_call = np.maximum(sT - K1, 0) - prem_long
    short_call = np.maximum(sT - K2, 0) - prem_short
    pnl = long_call - short_call

    return position * pnl


def payoff_put_spread(sT, strikes, premiums=None, position: int=1):
    """
    Bull/Bear Put Spread payoff at expiry.
    - strikes: np.array of strike prices
    - premiums: np.array of premiums
    Returns an array (PnL for each sT)
    """
    strikes = np.array(strikes, dtype=float)
    if strikes.size != 2:
        raise ValueError("Strikes array must have 2 values [K1, K2]")
    if not (strikes[0] < strikes[1]):
        raise ValueError("Require K1 < K2 for put spread")

    if premiums is None:
        premiums = np.zeros(2)
    else:
        premiums = np.array(premiums, dtype=float)
        if premiums.size != 2:
            raise ValueError("Premiums array must have 2 values")

    K1, K2 = strikes
    prem_long, prem_short = premiums

    long_put = np.maximum(K1 - sT, 0) - prem_long
    short_put = np.maximum(K2 - sT, 0) - prem_short
    pnl = long_put - short_put

    return position * pnl


def payoff_double_bear(sT, strikes, premiums=None, position: int=1):
    """
    Double bear payoff at expiry.
    - strikes: np.array of strike prices
    - premiums: np.array of premiums
    Returns an array (PnL for each sT)
    """
    strikes = np.array(strikes, dtype=float)
    if strikes.size != 4:
        raise ValueError("Strikes array must have 4 values [K1, K2, K3, K4]")
    if not (strikes[0] > strikes[1] > strikes[2] > strikes[3]):
        raise ValueError("Require K1 > K2 > K3 > K4 for double bear")
        
    if premiums is None:
        premiums = np.zeros(4)
    else:
        premiums = np.array(premiums, dtype=float)
        if premiums.size != 4:
            raise ValueError("Premiums array must have 4 values")
    
    K1, K2, K3, K4 = strikes
    prem1, prem2, prem3, prem4 = premiums
    
    long_call = np.maximum(sT - K1, 0) - prem1
    short_call = np.maximum(sT - K2, 0) - prem2 
    long_put = np.maximum(K3 - sT, 0) - prem3
    short_put = np.maximum(K4 - sT, 0) - prem4
    pnl = (long_call - short_call) + (long_put - short_put)
    
    return position * pnl



def plot_payoff(strategy, strikes, premiums, position, label: str = None, ax=None):
    """
    Plot a payoff curve.
    - strategy: 'call', 'put', 'call_spread', 'put_spread', 'double_bear'
    - strikes: array of strike prices
    - premiums: array of premiums
    - position: volume, +long/-short
    - label: legend label
    - ax: optional matplotlib Axes to plot on
    """
    sT = price_grid(spot_price=strikes)
    
    if strategy == 'call':
        pnl = payoff_call(sT, strikes, premiums, position)
    elif strategy == 'put':
        pnl = payoff_put(sT, strikes, premiums, position)
    elif strategy == 'call_spread':
        pnl = payoff_call_spread(sT, strikes, premiums, position)
    elif strategy == 'put_spread':
        pnl = payoff_put_spread(sT, strikes, premiums, position)
    elif strategy == 'double_bear':
        pnl = payoff_double_bear(sT, strikes, premiums, position)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, pnl, linewidth=2, label=label)
    ax.set_xlabel('Price at Expiry')
    ax.set_ylabel('PnL')
    if label:
        ax.legend()
    return ax

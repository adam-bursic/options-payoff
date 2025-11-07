import pandas as pd
import QuantLib as ql

def option_calc(type, initiation, sigma, rf, K, S0, divd, DTE, market='NullCalendar'):
    """
    calculates the value and greeks of a european option in a certain market
    :param type: 'call' or 'put'
    :param initiation: date as 'YYYY-MM-DD'
    :param sigma: volatility
    :param rf: risk-free rate
    :param K: strike price
    :param S0: spot price
    :param DTE: days to expiration
    :param market: country calender, defaults to NullCalendar
    :return: ['Value', 'Delta', 'Gamma', 'Vega', 'Theta']
    """

    trade_date = ql.Date(initiation, '%Y-%m-%d')
    ql.Settings.instance().evaluationDate = trade_date
    try:
        calendar = getattr(ql, market)()
    except AttributeError:
        raise ValueError(f"Unknown market calendar: {market}")

    expiry = trade_date + DTE

    if type == 'call':
        type = ql.Option.Call
    elif type == 'put':
        type = put = ql.Option.Put
    else:
        raise ValueError(f'type has to be call or put')

    payoff = ql.PlainVanillaPayoff(type, K)
    
    exercise = ql.EuropeanExercise(expiry)
    option = ql.VanillaOption(payoff, exercise)

    spot_handle = ql.QuoteHandle(ql.SimpleQuote(S0))
    volatility_handle = ql.BlackVolTermStructureHandle(
        ql.BlackConstantVol(trade_date, calendar, ql.QuoteHandle(ql.SimpleQuote(sigma)), ql.Actual365Fixed()))
    dividend_handle = ql.YieldTermStructureHandle(
        ql.FlatForward(trade_date, ql.QuoteHandle(ql.SimpleQuote(divd)), ql.Actual365Fixed()))
    risk_free_handle = ql.YieldTermStructureHandle(
        ql.FlatForward(trade_date, ql.QuoteHandle(ql.SimpleQuote(rf)), ql.Actual365Fixed()))

    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_handle, risk_free_handle, volatility_handle)

    option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))

    price = option.NPV()
    delta = option.delta()
    gamma = option.gamma()
    vega = option.vega()
    theta = option.theta()
    
    value = price * 100
    vega = vega / 100
    theta = theta / 100

    return pd.Series(
        {"Value": value,
         "Delta": delta,
         "Gamma": gamma,
         "Vega":  vega,
         "Theta": theta
        })

from math import exp, log, sqrt
from scipy.optimize import leastsq
from scipy.stats import norm
import numpy
import operator
import pickle

cdf = norm.cdf

def black_scholes(k, s, t, put, r, v):
    d1 = (log(s/k) + (r + v**2 / 2) * t) / (v * sqrt(t))
    d2 = d1 - v * sqrt(t)
    call = s * cdf(d1) - k * exp(-r*t) * cdf(d2)

    if put:
        return k * exp(-r*t) - s + call
    return call

def black_scholes_quote(quote, r, v):
    t = quote.days_to_exp
    k = quote.strike
    s = quote.spot
    put = quote.put

    d1 = (log(s/k) + (r + v**2 / 2) * t) / (v * sqrt(t))
    d2 = d1 - v * sqrt(t)
    call = s * cdf(d1) - k * exp(-r*t) * cdf(d2)

    if put:
        return k * exp(-r*t) - s + call
    return call

def residuals(estimated_params, actual_prices, quotes):
    return map(lambda price, quote:
               price - black_scholes_quote(quote, *estimated_params),
               actual_prices, quotes)

def compute_implied(quotes, r0=log(1.0525), v0=0.1):
    p0 = [r0, v0]
    option_prices = [(quote.bid + quote.ask) / 2 for quote in quotes]
    return leastsq(residuals, p0, args=(option_prices, quotes))

if __name__ == '__main__':
    import sys
    print compute_implied(pickle.load(sys.stdin))

from math import exp, log, sqrt
from scipy.stats import norm
import numpy
import pickle

import stats

cdf = stats.cdf

def black_scholes(x, b):
    y = numpy.zeros(len(x))
    r, v = b

    for i in xrange(len(x)):
        k, s, t, put = x[i]

        sqrt_t = sqrt(t)
        k_e_r_t = k * exp(-r*t)

        d1 = (log(s/k) + (r + v**2 / 2) * t) / (v * sqrt_t)
        d2 = d1 - v * sqrt_t
        call = s * cdf(d1) - k_e_r_t * cdf(d2)

        if put:
            y[i] = k_e_r_t - s + call
        else:
            y[i] = call

    return y

def observations(quotes):
    y = numpy.array([(quote.bid + quote.ask) / 2 for quote in quotes])
    x = numpy.zeros((len(quotes), 4))
    for q in xrange(len(quotes)):
        x[q] = quotes[q].strike, quotes[q].spot, \
               quotes[q].days_to_exp, quotes[q].put

    return y, x

def compute_implied(y, x, r0=log(1.0525), v0=0.1):
    b0 = numpy.array([r0, v0])
    return stats.lm(black_scholes, y, x, b0)

def main():
    import sys

    quotes = pickle.load(sys.stdin)
    y, x = observations(quotes)
    soln = compute_implied(y, x)[0]
    errors = stats.errors(black_scholes, y, x, soln)

    print 'b:   ', soln
    print 'err: ', errors

if __name__ == '__main__':
    main()

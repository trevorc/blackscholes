#!/usr/bin/env python

import collections
from math import log
import sys
import numpy
import pickle

from _blackscholes import black_scholes
import stats

OptionQuote = collections.namedtuple('OptionQuote', [
    'symbol', 'underlying', 'put', 'strike', 'spot', 'days_to_exp',
    'bid', 'ask'])

def black_scholes_arr(x, b):
    y = numpy.zeros(len(x))
    r, vol = b

    for i in xrange(len(x)):
        k, s, t, put = x[i]
        y[i] = black_scholes(k, s, t, bool(put), r, vol)

    return y

def observations(quotes):
    y = numpy.array([(quote.bid + quote.ask) / 2 for quote in quotes])
    x = numpy.zeros((len(quotes), 4))
    for q in xrange(len(quotes)):
        x[q] = quotes[q].strike, quotes[q].spot, \
               quotes[q].days_to_exp, quotes[q].put

    return y, x

def main():
    quotes = pickle.load(sys.stdin)
    y, x = observations(quotes)
    b0 = numpy.array([log(1.0525), 0.1])
    soln = stats.lm(black_scholes_arr, y, x, b0)[0]
    errors = stats.errors(black_scholes_arr, y, x, soln)

    r, vol = soln
    print 'r:  ', r
    print 'vol:', vol
    print 'err:', errors

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import collections
import math
import sys
import time
import numpy

from _blackscholes import black_scholes
import stats

OptionQuote = collections.namedtuple('OptionQuote', [
    'symbol', 'underlying', 'put', 'strike', 'spot', 'years_to_exp',
    'price'])

def black_scholes_arr(x, b):
    y = numpy.zeros(len(x))
    r, vol = b

    for i in xrange(len(x)):
        k, s, t, put = x[i]
        y[i] = black_scholes(k, s, t, bool(put), r, vol)

    return y

def parse(f):
    for line in f:
        symbol, underlying, put, strike, spot, years_to_exp, price = \
                line.split(',')
        yield OptionQuote(symbol, underlying, bool(int(put)),
                          float(strike), float(spot), float(years_to_exp),
                          float(price))

def observations(quotes):
    y = numpy.array([quote.price for quote in quotes])
    x = numpy.zeros((len(quotes), 4))

    for q in xrange(len(quotes)):
        x[q] = quotes[q].strike, quotes[q].spot, \
               quotes[q].years_to_exp, quotes[q].put

    return y, x

def main():
    start = time.time()
    quotes = parse(sys.stdin)
    y, x = observations(filter(lambda q: q.price > 0, quotes))
    b0 = numpy.array([math.log(1.0525), 0.1])
    soln = stats.lm(black_scholes_arr, y, x, b0)[0]
    errors = stats.errors(black_scholes_arr, y, x, soln)
    runtime = time.time() - start

    r, vol = soln
    print 'Parameters\nr: %s\nvol: %s\n' % (r, vol)
    print 'Error\nrss: %s\nR^2: %s\nrmse: %s\n' % errors
    print 'processed %s quotes in %.2fs' % (len(y), runtime)

if __name__ == '__main__':
    main()

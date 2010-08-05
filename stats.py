import collections
from ctypes import c_double, cdll
import math

import scipy.optimize

libm = cdll.LoadLibrary('libm.so.6')
libm.erfc.restype = c_double
libm_erfc = libm.erfc
sqrt_2 = math.sqrt(2)

def cdf(d):
    return libm_erfc(c_double(-d/sqrt_2)) / 2.0

Errors = collections.namedtuple('Errors', ['rss', 'r_squared', 'rmse'])

def lm(f, y, x, b0, **kwargs):
    def compute_residuals(b):
        return y - f(x, b)
    return scipy.optimize.leastsq(compute_residuals, b0)

def errors(f, y, x, b):
    Y = f(x, b)
    y_mean = sum(y, 0.0) / len(y)

    rss = sum((y - Y) ** 2)
    ss_tot = sum((y - y_mean) ** 2)
    r_squared = 1 - rss / ss_tot
    rmse = math.sqrt(rss / len(y))

    return Errors(rss, r_squared, math.sqrt(rss / len(y)))

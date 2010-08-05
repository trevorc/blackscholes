import collections
import math

import scipy.optimize

Errors = collections.namedtuple('Errors', ['rss', 'r_squared', 'rmse'])

def lm(f, y, x, b0, **kwargs):
    def compute_residuals(b):
        return y - f(x, b)
    return scipy.optimize.leastsq(compute_residuals, b0, **kwargs)

def errors(f, y, x, b):
    Y = f(x, b)
    y_mean = sum(y, 0.0) / len(y)

    rss = sum((y - Y) ** 2)
    ss_tot = sum((y - y_mean) ** 2)
    r_squared = 1 - rss / ss_tot
    rmse = math.sqrt(rss / len(y))

    return Errors(rss, r_squared, math.sqrt(rss / len(y)))

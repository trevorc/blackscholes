cdef extern from 'math.h':
    double erfc(double)
    double exp(double)
    double log(double)
    double sqrt(double)

cdef double cdf(double x):
    return erfc(-x/sqrt(2)) / 2

def black_scholes(double k, double s, double t, bool put, double r,
                  double vol):
    cdef double call, d1, d2, ke_rt, sqrt_t

    sqrt_t = sqrt(t)
    ke_rt = k * exp(-r*t)

    d1 = (log(s/k) + (r + vol**2 / 2) * t) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    call = s * cdf(d1) - ke_rt * cdf(d2)

    if put:
        return ke_rt - s + call
    return call

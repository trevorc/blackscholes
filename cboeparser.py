#!/usr/bin/env python

import datetime
import operator
import pickle
import re

from blackscholes import OptionQuote

option_symbol_re = re.compile(r'(?P<exp>\d+ \w+) (?P<strike>[^ ]+) \('
                              r'(?P<sym>[^0-9]+\d\d(?P<day>\d\d)[^)]+)\)')

def parse_quotetime(s):
    return datetime.datetime.strptime(s, '%b %d %Y @ %H:%M ET')

def parse_expiration(s, day):
    dt = datetime.datetime.strptime(s, '%y %b')
    return datetime.datetime(year=dt.year, month=dt.month, day=int(day),
                             hour=17, minute=30)

def read_cboe_data(f):
    f = iter(f)
    name, _, _, _ = f.next().split(',')
    quotetime, _, under_bid, _, under_ask, _, _, _, _, _ = \
            f.next().split(',')
    f.next()

    underlying = name.split(' ', 1)[0]
    quotetime = parse_quotetime(quotetime)
    under_bid, under_ask = map(float, (under_bid, under_ask))

    while True:
        calls_strike_symbol, _, _, call_bid, call_ask, _, _, \
                puts_strike_symbol, _, _, put_bid, put_ask, _, _, _ = \
                f.next().split(',')

        calls_symbol_m = option_symbol_re.match(calls_strike_symbol)
        puts_symbol_m  = option_symbol_re.match(puts_strike_symbol)
        expiration = parse_expiration(calls_symbol_m.group('exp'),
                                      calls_symbol_m.group('day'))

        if expiration <= quotetime:
            continue
        days_to_exp = (expiration - quotetime).days / 365.0

        yield OptionQuote(calls_symbol_m.group('sym'), underlying,
                          False, float(calls_symbol_m.group('strike')),
                          (under_bid + under_ask) / 2.0, days_to_exp,
                          float(call_bid), float(call_ask))
        yield OptionQuote(puts_symbol_m.group('sym'), underlying,
                          True, float(puts_symbol_m.group('strike')),
                          (under_bid + under_ask) / 2.0, days_to_exp,
                          float(put_bid), float(put_ask))

def main():
    import sys
    pickle.dump(list(read_cboe_data(sys.stdin)), sys.stdout)

if __name__ == '__main__':
    main()

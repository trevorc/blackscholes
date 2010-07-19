import collections

OptionQuote = collections.namedtuple('OptionQuote', [
    'symbol', 'underlying', 'put', 'strike', 'spot', 'days_to_exp',
    'bid', 'ask'])

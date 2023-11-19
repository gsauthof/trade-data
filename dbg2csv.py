#!/usr/bin/env python3

import decimal
import gzip
import json
import sys

col_keys = ('messageId', 'sourceName', 'symbol', 'tickActionIndicator', 'mmtMarketMechanism', 'mmtTradingMode', 'mmtModificationInd', 'tickId', 'lastTradeTime', 'lastTrade', 'lastQty', 'currency', 'notionalAmount', 'instrumentIdCode', 'quotationType', 'distributionDateTime', 'instrumentId', 'transIdCode', 'executionVenueId', 'mmtAlgoInd')

def mainP():
    print(','.join(col_keys))
    for filename in sys.argv[1:]:
        with gzip.open(filename) as f:
            ds = json.load(f, parse_float=decimal.Decimal)
            for d in ds:
                print(','.join(str(d.get(x, '')) for x in col_keys))

def main():
    try:
        return mainP()
    except BrokenPipeError:
        return 1


if __name__ == '__main__':
    sys.exit(main())

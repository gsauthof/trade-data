#!/usr/bin/env python3

# zstd -c -d  EU_XET_posttrd_current.txt.zst | grep price | head -1  | tr ',' '\n'  | tr '{}' '\n' | grep -v '^ *$' | grep -v ':$' | sort 

import csv
import re
import sys

# company description,security_id,mic,isin,umtf,currency,tick table,operating_mic
def read_securities(filename):
    d = {}
    with open(filename, newline='') as f:
        rows = csv.DictReader(f)
        for row in rows:
            xs = (row['isin'], row['company description'], row['currency'], row['mic'], row['operating_mic'])
            d[row['security_id']] = xs
    return d


def pp_price(s):
    return s[:-5] + '.' + s[-5:]

# msgType, length, seqNo, securityId, tradeType, quantity, price, orderId,
# tradeRef, timestamp, marketMechanism, tradingMode, transactionCat,
# negotiationIndicator, crossingTrade, modificationIndicator,
# benchmarkIndicator, dividend, offBookAutomation, priceFormation,
# algoIndicator, publicationModeDeferralReason, postTradeDeferralType,
# duplicativeIndicator, v, unrestrictedAtTopOfBook
def parse(f, ref):
    ex = re.compile('[,{}]')
    d = {}
    hs = ','.join( ('timestamp', 'msgType', 'seqNo', 'securityId',
                    'isin', 'company', 'curr', 'mic', 'op_mic',
                    'tradeType', 'quantity', 'price',
                    'marketMechanism', 'tradingMode', 'transactionCat',
                    'negotiationIndicator', 'crossingTrade', 'modificationIndicator',
                    'benchmarkIndicator', 'dividend', 'offBookAutomation', 'priceFormation',
                    'algoIndicator', 'publicationModeDeferralReason', 'postTradeDeferralType',
                    'duplicativeIndicator', 'v', 'unrestrictedAtTopOfBook'
                    ) )
    print(hs)
    for line in f:
        if 'price_' not in line:
            continue
        xs = ex.split(line)
        for x in xs:
            x = x.strip()
            if not x:
                continue
            ks = x.split(':')
            if len(ks) != 2 or not ks[1]:
                continue
            k, v = ks[0].strip('"_'), ks[1].strip('"_')
            d[k] = v
        s = ','.join( (d['timestamp'], d['msgType'], d['seqNo'], d['securityId'])
                 + ref[d['securityId']]
                 + (d['tradeType'], d['quantity'], pp_price(d['price']),
                    d['marketMechanism'], d['tradingMode'], d['transactionCat'],
                    d['negotiationIndicator'], d['crossingTrade'], d['modificationIndicator'],
                    d['benchmarkIndicator'], d['dividend'], d['offBookAutomation'], d['priceFormation'],
                    d['algoIndicator'], d['publicationModeDeferralReason'], d['postTradeDeferralType'],
                    d['duplicativeIndicator'], d['v'], d['unrestrictedAtTopOfBook']
                    ) )
        print(s)
        d.clear()

def main():
    ref = read_securities(sys.argv[2])
    parse(sys.stdin, ref)


if __name__ == '__main__':
    sys.exit(main())

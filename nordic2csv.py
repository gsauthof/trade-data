#!/usr/bin/env python3


import csv
import subprocess
import sys


def main():
    filenames = sys.argv[1:]
    header = []
    writer = csv.writer(sys.stdout)
    for filename in filenames:
        with subprocess.Popen(['dcat', filename], stdout=subprocess.PIPE,
                              universal_newlines=True) as p:
            f = p.stdout
            f.readline()
            reader = csv.reader(f, delimiter=';')
            rows = iter(reader)
            row = next(rows)
            if not row:
                continue
            if header:
                if row != header:
                    raise RuntimeError(f'New header is different in {filename}: {header} vs. {row}')
            else:
                writer.writerow(row)
                header = row
            writer.writerows(rows)
    p.wait()
           

if __name__ == '__main__':
    sys.exit(main())

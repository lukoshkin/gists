#!/usr/bin/env python

import os
import re
import argparse
from pathlib import Path


# ||| ########################### |||
# ||| Change conversion rule here |||
# vvv ########################### vvv

## Square meters to Darcy
# converter = lambda match: f'{float(match)*1.01325*1e+18:.2e}'
## Darcy to square meters
# converter = lambda match: f'{float(match)*.986923*1e-18:.2e}'

def converter(num):
    num = f'{float(num)*1.01325*1e+18:.2e}'
    man, exp = num.split('e')
    exp = int(exp.replace('+', ''))
    num = man + '\cdot10^{' + str(exp) + '}'
    return repr(num).replace("'", '$')


def convert_column(infile, field_no):
    if field_no < 1:
        print('Field numbers start from 1.')
        return

    infile = Path(infile)
    tmpfile = f'/tmp/{infile.stem}.tmp'
    newfile = f'/tmp/{infile.stem}.new'

    field = '[^&]*&'
    snp = '[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
    pattern = f'\s*{field*(field_no-1)}[ ]?({snp})[ ]?.*'
    # '{{' is a way of escaping of '{' in f-strings. Unfortunately, in
    # my case, in some tables, there were numbers wrapped with curly braces.
    # pattern = f'\s*{field*(field_no-1)}[ ]?{{?({snp})}}?[ ]?.*'
    pattern = re.compile(pattern)

    with open(infile) as ifp, open(tmpfile, 'w') as ofp:
        for line in ifp:
            match = re.match(pattern, line)
            if match:
                match = match.group(1)
                repl = converter(match)
                print(f'{match} --> {repl}')
                line = re.sub(re.escape(match), repl, line, 1)
            ofp.write(line)

    os.system(f'cp {tmpfile} {newfile}')
    print('------------\n')

    return newfile


def convert_multiple_columns(infile, fields):
    outfile = infile
    for field_no in fields:
        outfile = convert_column(outfile, field_no)

    return outfile



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fields')
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    fields = list(map(int, args.fields.split(',')))
    outfile = convert_multiple_columns(args.infile, fields)
    os.system(f'cat {outfile} | xclip -selection c')

    print('Check your clipboard!')
    print('Also the results can be found here:', outfile)

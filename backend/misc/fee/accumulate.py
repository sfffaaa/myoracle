#!/usr/bin/env python3
# encoding: utf-8

import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise IOError('You should have one arguments')

    target_file = sys.argv[1]
    with open(target_file) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    lines = [line for line in lines if not line.startswith('========')]
    lines = [line for line in lines if not line.startswith('-----------------')]
    lines = [line for line in lines if line != 'name func fee count avg_fee']

    total_gas = sum([int(line.split()[2]) for line in lines])
    print('filename: {0}, total gas: {1}'.format(target_file, total_gas))

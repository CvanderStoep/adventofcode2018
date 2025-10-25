#!/usr/bin/python
"""Advent of Code 2018, Day 21, Part 2

https://adventofcode.com/2018/day/21

Given a program that runs on the CPU from day 16, figure out what number
will cause the program to execute "the most number of instructions". The
algorithm produces a repeating stream of numbers, so it has to figure out
what the last number it produces before it repeats.

The algorithm itself is very slow to execute on the pseudo-CPU, so it required
analyzing the algorithm. The semi-optimized version that still does things
more-or-less the same way takes 55 seconds. I also boiled down the algorithm
into optimized Python that does it in 4ms.

The algorithm itself is a hashing function that feeds the same number in over
and over, which eventually causes a repeating cycle.

I would imagine the puzzle varies the two constants, which are read from the
program data for these optimized versions.

See test.dat for sample data and program.dat for full data.

Author: Tim Behrendsen
"""

import re

FAST = True

fn = 'input/input21.txt'

def read_constants():
    program = []
    with open(fn, 'r') as file:
        for line in file:
            if line[0:3] != '#ip':
                op, a, b, c = re.findall(r'(....) (\d+) (\d+) (\d+)', line)[0]
                program.append((op, int(a), int(b), int(c)))

    return (program[7][1], program[11][2])

# Optimized fast version, takes about four milliseconds
def fast():
    c1, c2 = read_constants()
    seen = set()
    accum = 0

    while True:
        mult = accum | 0x10000
        accum = c1
        for byte in ( mult & 0xff, (mult >> 8) & 0xff, mult >> 16 ):
            accum = ((accum + byte) * c2) & 0xffffff

        if accum in seen:
            break
        seen.add(accum)
        last_accum = accum
        #print(f"{len(seen)}: {accum}")

    print(f"Answer: {last_accum}")

# Semi-optimized, still using instruction pointer. Takes about 55 seconds
# on my machine.
def main():
    c1, c2 = read_constants()
    regs = [0, 0, 0, 0, 0, 0]
    ip = 0
    res_counter = 0
    seen = set()

    def set_ip(n):
        nonlocal ip
        ip = n
        #print(f"    JUMP to: {n+1}")

    #ip 1
    while ip < 36:
        #print(f"{ip}: {regs}")
        if ip == 0: # seti 123 0 4
            regs[4] = 0
            set_ip(6)
            continue

        elif ip == 6: # bori 4 65536 3
            regs[3] = regs[4] | 0x10000 # 65536
            regs[4] = c1
            ip = 8
            continue

        elif ip == 8: # bani 3 255 5
            regs[5] = regs[3] & 0xff
            regs[4] += regs[5]
            regs[4] &= 0xffffff # 16777215
            regs[4] *= c2 # 65899
            regs[4] &= 0xffffff # 16777215
            if 256 > regs[3]:
                set_ip(28)
            else:
                regs[5] = 0
                set_ip(18)
            continue
        elif ip == 18: # addi 5 1 2
            regs[2] = regs[5] + 1
            regs[2] *= 256
            if regs[2] > regs[3]:
                regs[3] = regs[5]
                set_ip(8)
            else:
                regs[5] += 1
                set_ip(18)
            continue
        elif ip == 28: # eqrr 4 0 5
            res_counter += 1
            print(f"{res_counter} iteration is: {regs[4]}")
            if regs[4] in seen:
                break

            seen.add(regs[4])
            last_accum = regs[4]

            if regs[4] == regs[0]:
                break
            set_ip(6)
            continue
        else:
            print(f"BAD {ip}")
            exit(0)

        ip += 1

    print(f"Answer: {last_accum}")

if FAST:
    fast()
else:
    main()
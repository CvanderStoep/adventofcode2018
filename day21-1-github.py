#!/usr/bin/python
"""Advent of Code 2018, Day 21, Part 1

https://adventofcode.com/2018/day/21

Given a program that runs on the CPU from day 16, figure out what number
will cause the program to exit. Just intercepts the test where it does the
exit and re-injects that number.

See test.dat for sample data and program.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'test.dat'
fn = 'input/input21.txt'

class CPU:
    def __init__(self, ip_reg):
        self.regs = [ 0, 0, 0, 0, 0, 0 ]
        self.ip_reg = ip_reg
        self.program = []
        self.ip = 0
        self.op_list = {
            'addr': self.addr, 'addi': self.addi, 'mulr': self.mulr, 'muli': self.muli,
            'banr': self.banr, 'bani': self.bani, 'borr': self.borr, 'bori': self.bori,
            'setr': self.setr, 'seti': self.seti, 'gtir': self.gtir, 'gtri': self.gtri,
            'gtrr': self.gtrr, 'eqir': self.eqir, 'eqri': self.eqri, 'eqrr': self.eqrr }

    def get_reg(self, r):
        if self.ip_reg != None and self.ip_reg == r:
            return self.ip
        return self.regs[r]

    def set_reg(self, r, v):
        if self.ip_reg != None and self.ip_reg == r:
            self.ip = v
        self.regs[r] = v

    def ip(self, params):
        self.ip_reg = params[0]

    def addr(self, params):
        self.set_reg(params[2], self.get_reg(params[0]) + self.get_reg(params[1]))

    def addi(self, params):
        self.set_reg(params[2], self.get_reg(params[0]) + params[1])

    def mulr(self, params):
        self.set_reg(params[2], self.get_reg(params[0]) * self.get_reg(params[1]))

    def muli(self, params):
        self.set_reg(params[2], self.get_reg(params[0]) * params[1])

    def banr(self, params):
        self.set_reg(params[2], self.get_reg(params[0]) & self.get_reg(params[1]))

    def bani(self, params):
        self.set_reg(params[2], self.get_reg(params[0]) & params[1])

    def borr(self, params):
        self.set_reg(params[2], self.get_reg(params[0]) | self.get_reg(params[1]))

    def bori(self, params):
        self.set_reg(params[2], self.get_reg(params[0]) | params[1])

    def setr(self, params):
        self.set_reg(params[2], self.get_reg(params[0]))

    def seti(self, params):
        self.set_reg(params[2], params[0])

    def gtir(self, params):
        self.set_reg(params[2], 1 if params[0] > self.get_reg(params[1]) else 0)

    def gtri(self, params):
        self.set_reg(params[2], 1 if self.get_reg(params[0]) > params[1] else 0)

    def gtrr(self, params):
        self.set_reg(params[2], 1 if self.get_reg(params[0]) > self.get_reg(params[1]) else 0)

    def eqir(self, params):
        self.set_reg(params[2], 1 if params[0] == self.get_reg(params[1]) else 0)

    def eqri(self, params):
        self.set_reg(params[2], 1 if self.get_reg(params[0]) == params[1] else 0)

    def eqrr(self, params):
        self.set_reg(params[2], 1 if self.get_reg(params[0]) == self.get_reg(params[1]) else 0)

    def load(self, program):
        self.program = program

    def run(self, reg0, get_mode):
        self.ip = 0
        self.regs = [ reg0, 0, 0, 0, 0, 0 ]
        counter = 0
        while self.ip < len(self.program):
            counter += 1
            inst = self.program[self.ip]
            self.op_list[inst[0]](inst[1:4])

            # Intercept test if we're in that mode
            if get_mode and inst == ('eqrr', 4, 0, 5):
                return self.regs[4]

            self.ip += 1
            self.regs[self.ip_reg] = self.ip

        return 0

def main():
    program = []
    with open(fn, 'r') as file:
        for line in file:
            if line[0:3] == '#ip':
                ip_reg = int(line[4])
                continue
            op, a, b, c = re.findall(r'(....) (\d+) (\d+) (\d+)', line)[0]
            program.append((op, int(a), int(b), int(c)))

    cpu = CPU(ip_reg)
    cpu.load(program)

    # First run and intercept testing number
    n = cpu.run(0, True)

    # Re-inject testing number so it exits
    cpu.run(n, False)

    return cpu.regs[0]

answer = main()
print(f"Answer is {answer}")
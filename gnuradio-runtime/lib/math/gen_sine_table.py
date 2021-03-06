#!/usr/bin/env python
#
# Copyright 2004 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#

from __future__ import unicode_literals
import math
import sys

def wrap (x):
    if x >= 2**31:
        return x - 2**32
    return x

def gen_approx_table (f, nentries, min_x, max_x):
    """return a list of nentries containing tuples of the form:
    (m, c, abs_error).  min_x and max_x specify the domain
    of the table.
    """
    r = []
    incx = float (max_x - min_x) / nentries
    for i in range (nentries):
        a = (i * incx) + min_x
        b = ((i + 1) * incx) + min_x
        m = (f(b)-f(a)) / (b-a)
        c = (3.0*a+b)*(f(a)-f(b))/(4.0*(b-a)) + (f((a+b)/2.0) + f(a))/2.0
        abs_error = c+m*a-f(a)
        r.append ((m, c, abs_error))
    return r

def scaled_sine (x):
    return math.sin (x * math.pi / 2**31)

def gen_sine_table ():
    nbits = 10
    nentries = 2**nbits

    # min_x = -2**31
    # max_x =  2**31-1
    min_x = 0
    max_x = 2**32-1
    t = gen_approx_table (scaled_sine, nentries, min_x, max_x)

    max_error = 0
    for e in t:
        max_error = max (max_error, abs (e[2]))

    # sys.stdout.write ('static const int WORDBITS = 32;\n')
    # sys.stdout.write ('static const int NBITS = %d;\n' % (nbits,))

    sys.stdout.write ('  // max_error = %22.15e\n' % (max_error,))

    # sys.stdout.write ('static const double sine_table[%d][2] = {\n'% (nentries,))

    for e in t:
        sys.stdout.write ('  { %22.15e, %22.15e },\n' % (2.0 * e[0], e[1]))

    # sys.stdout.write ('};\n')

if __name__ == '__main__':
    gen_sine_table ()

#!/bin/env python3
# uDMX.py - Anyma (and clones) uDMX interface utility
# Copyright (C) 2016  Dave Hocker (email: AtHomeX10@gmail.com)
# Copyright (C) 2022  Ken Shibata <+@nyiyui.ca> (modifications made from uDMX.py)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#
# This utility is based on the C++ uDMX utility written by Markus Baertschi.
# See https://github.com/markusb/uDMX-linux.git for more on this good work.
# In particular, this program reads the same format rc file: ~/.uDMXrc
# It responds to the same commands and inputs.
#
# This program is limited to controlling one uDMX, namely the first one
# it finds with the correct vendor ID and product ID.
#

import sys
import usb
from pyudmx import pyudmx


if __name__ == "__main__":
    import argparse

    # Set up command line parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Produce verbose output", action="store_true")
    args = parser.parse_args()

    verbose = args.verbose

    # Open the uDMX USB device
    dev = pyudmx.uDMXDevice()
    dev.open()
    with dev:
        for line in sys.stdin:
            raw_tokens = list(map(int, line.split()))
            ch, *tokens = raw_tokens
            if verbose:
                print(f"sending ch {ch} tokens {tokens}", f=sys.stderr)
            if len(tokens) == 1:
                n = dev.send_single_value(ch, tokens[0])
            else:
                n = dev.send_multi_value(ch, tokens)
            if n != len(tokens):
                print(f"failed to send all ({len(raw_tokens)}) raw tokens ({n} raw tokens sent)", f=sys.stderr)
            else:
                print(f"sent {n} raw tokens: {raw_tokens}", f=sys.stderr)

#!/usr/bin/env python3

import subprocess, os, sys

fig_width = sys.argv[1] if len(sys.argv) > 1 else '7'

traceses = ["MMWAVESINR CWND", "MMWAVESINR RTT", "MMWAVESINR DATA", "RTT DATA", "RTT CWND", "DATA RTT CWND", "MMWAVESINR CWND RTT DATA"]

for traces in traceses:
    subprocess.call('plot.py --trace {} --figsize {},4 --data-wndw 0.1'.format(traces, fig_width), shell=True, cwd=os.getcwd())
import subprocess

traces = ['CWND', 'RCWND', 'RTT', 'DATA', 'LTESINR', 'MMWAVESINR']

for trace in traces:
    subprocess.call('python3 plot.py 1 {}'.format(trace), shell=True)
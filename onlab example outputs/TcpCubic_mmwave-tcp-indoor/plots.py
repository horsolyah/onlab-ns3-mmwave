import subprocess

traces = ['CWND', 'RCWND', 'RTT']
nodeses = ['', '1 3 5', '2 4 6']

for trace in traces:
    for nodes in nodeses:
        subprocess.call('python3 plot.py {} {}'.format(nodes, trace), shell=True)
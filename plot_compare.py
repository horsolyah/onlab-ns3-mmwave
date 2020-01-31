#!/usr/bin/env python3

"""
Plots traces of different/separate executions.
Filename requirements:
e.g. TcpBbr-1500000-1400-5-1-1-TCP-DATA.txt
     TcpBbr-1500000-1400-5-2-2-TCP-DATA.txt
For each data type, a lighter and a darker shade of a color will be set using attr_specific_dict.   
"""

import os, sys, re
import argparse
import matplotlib.style as mplstyle
#mplstyle.use('fast')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

parser = argparse.ArgumentParser()
parser.add_argument("--traces", "-t", default='DATA', nargs='?', help="Select data trace to plot.", choices=['CWND', 'RCWND', 'RTT', 'DATA', 'MMWAVESINR', 'LTESINR'])
parser.add_argument("--nodes", "-n", default=['1','2'], nargs='*', help="Select which nodes' trace files should be plotted.", choices=['1', '2', '3', '4', '5', '6'])
parser.add_argument("--data-wndw", default='0.05', nargs='?', help="Resolution of x axis (tick size) in seconds.")
parser.add_argument("--figsize", default='5,4', nargs='?', help="Figure size in inches delimited by a comma e.g. 11,4")
args = parser.parse_args()

#protocol = 'TcpWestwood'
protocol = 'TcpBbr'
#protocol = 'TcpCubic'
buffer_size = '1500000'
packet_size = '1400'
p2pdelay = '5'
nodeNum = 2
filename_base = '-'.join([protocol, buffer_size, packet_size, p2pdelay])
#colors = 'bgrcmyk'
colors = 'brcmgyk'
labels_new = ['CUBIC', 'BBR']

data_wndw = float(args.data_wndw)

def value_to_plot(trace):
    if trace in ['DATA']:
        return 1
    if trace in ['CWND', 'RCWND', 'RTT']:
        return 2
    if trace in ['MMWAVESINR', 'LTESINR']:
        return 3

def data_trace(x_vals, y_vals):
    wndw = data_wndw
    wndw_start = 0.0
    wndw_end = wndw_start + wndw
    multiplier = 1/wndw

    wndw_cnt = 0
    packets_list = [0]   # element: sum of the size of packets rcvd in wndw (e.g. 0.1 s) in bits    e.g. [20000, 26000, 34000, 42000] need to be multiplied by multiplier!

    # iterate over lines in trace file
    for i in range(len(x_vals)):
        packet_arrive_time = x_vals[i]
        packet_size = y_vals[i] * 8    # in bits

        # count how many packets fit into given window (tick)
        if packet_arrive_time >= wndw_start and packet_arrive_time < wndw_end:
            packets_list[wndw_cnt] += packet_size
        else:
            wndw_cnt += 1
            packets_list.append(0)
            wndw_start = wndw_end
            wndw_end = wndw_end + wndw

    x_vals, y_vals = [], []

    # iterate over quantitized windows (ticks)
    for i in range(len(packets_list)):
        x_val = i * wndw

        bitpers = packets_list[i] * multiplier
        kbitpers = bitpers / 1000
        mbitpers = kbitpers / 1000

        y_val = mbitpers

        x_vals.append(float(x_val))
        y_vals.append(int(y_val))

    return (x_vals, y_vals)
    
def plot_trace_file(nodes=None, trace=''):
    # nodes: only plot specified nodes' trace data (list)
    # trace: [CWND, RCWND, RTT]

    figsize = tuple(map(lambda n: int(n), args.figsize.split(',')))
    figure = plt.figure(figsize=figsize)

    if not nodes: 
        nodes = ['1', '2', '3', '4', '5', '6']
        output_filename = trace + '.png'
    else:
        output_filename = '-'.join(['-'.join(nodes), trace + '.png'])

    if trace == 'MMWAVESINR':
        trace_filename = 'MmWaveSinrTime.txt'
        output_filename = 'MmWaveSinrTime.png'
    if trace == 'LTESINR':
        trace_filename = 'LteSinrTime.txt'
        output_filename = 'LteSinrTime.png'
    
    for i in nodes:
        if trace in ['CWND', 'RCWND', 'RTT', 'DATA']:   
            trace_filename = '-'.join([filename_base, i, i, 'TCP', trace + '.txt'])

        plot_style = 's' if trace == 'RCWND' else '-'

        x_vals, y_vals = [], []

        with open(trace_filename, 'r') as f:
            print("Opening ", trace_filename)
            for line in f:
                #time, old, new = re.match('([0-9\.]*)\W*([0-9\.]*)\W*([0-9\.]*)\W*')
                linedata = re.findall('([0-9\.]*)\W*', line)

                if trace == 'MMWAVESINR':
                    if linedata[1] != str(i):	# only gather current node's data
                        continue

                x_val, y_val = linedata[0], linedata[value_to_plot(trace)]                    

                if trace == 'CWND' or trace == 'RCWND':     # cwnd size to packets
                    y_val = str(int(int(y_val) / int(packet_size)))

                if '.' in x_val: 
                    x_vals.append(float(x_val))
                else:
                    x_vals.append(int(x_val))
                if '.' in y_val: 
                    y_vals.append(float(y_val))
                else:
                    y_vals.append(int(y_val))

        if trace == 'DATA': 
            (x_vals, y_vals) = data_trace(x_vals, y_vals)
        

        attr_specific_dict = {
            'DATA': ['red', 'maroon'],
            'RTT': ['limegreen', 'darkgreen'],
            'CWND': ['darkorange', 'darkgoldenrod'],
            'MMWAVESINR': ['b', 'b']
        }

        attr_specific_color = attr_specific_dict[trace][int(i)-1]
        print(attr_specific_color)


        # missing plot_style -
        plt.plot(x_vals, y_vals, attr_specific_color, linestyle='-', linewidth=0.5, antialiased=False, label=labels_new[int(i)-1])
        #used before last minute coloring #plt.plot(x_vals, y_vals, colors[int(i)-1]+plot_style, linewidth=0.5, antialiased=False, label=labels_new[int(i)-1])
        #plt.plot(x_vals, y_vals, colors[int(i)-1], linestyle='s', markersize=2, linewidth=0.3, antialiased=False, label='Node '+i)
        
        plt.xlabel('time (s)')
        if trace == 'CWND' or trace == 'RCWND':
            plt.ylabel('CWND size (packets)')
        if trace == 'RTT':
            plt.ylabel('RTT (s)')
        if trace == 'DATA': 
            plt.ylabel('Throughput (Mb/s)')
        if trace == 'MMWAVESINR':
            plt.ylabel('SINR (dB)')
        if trace == 'LTESINR':
            plt.ylabel('SINR')
        #plt.axis('tight')
        '''if len(nodes) == 1:
            plt.title('Node {} {}'.format(nodes[0], trace))
        elif len(nodes) == 6:
            plt.title('All nodes {}'.format(trace))
        elif len(nodes) > 1:
            plt.title('Nodes {} {}'.format(', '.join(nodes), trace))
        else:
            plt.title('Node 1-6 {}'.format(trace))
        if trace == 'DATA': 
            plt.suptitle('Data throughput')
            plt.title('interval = ' + str(data_wndw) + ' s')'''

    ax = plt.axes()
    #ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    #ax.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_major_locator(plt.AutoLocator())
    ax.yaxis.set_major_locator(plt.AutoLocator())
    ax.legend()
    ax.axvspan(0, 2, facecolor='lightgray', alpha=0.5, label="NLOS")
    ax.axvspan(4, 8, facecolor='lightgray', alpha=0.5, label="NLOS")
    ax.axvspan(10, 12, facecolor='lightgray', alpha=0.5, label="NLOS")

    #plt.show()
    if not os.path.isdir('png'): os.makedirs('png')
    plt.savefig('./png/' + output_filename, bbox_inches='tight')
    #plt.savefig('./png/' + output_filename)

plot_trace_file(nodes=args.nodes, trace=args.traces)

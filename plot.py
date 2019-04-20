import os, sys, re, math
import argparse
import matplotlib.style as mplstyle
mplstyle.use('fast')
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot

parser = argparse.ArgumentParser()
parser.add_argument("--traces", "-t", default=['DATA'], nargs='*', help="", choices=['CWND', 'RCWND', 'RTT', 'DATA', 'MMWAVESINR', 'LTESINR'])
parser.add_argument("--nodes", "-n", default=['1'], nargs='*', help="", choices=['1', '2', '3', '4', '5', '6'])
parser.add_argument("--data-wndw", default='0.1', nargs='?', help="")
args = parser.parse_args()

filename_regex = '(Tcp[\w]*)-([\d]*)-([\d]*)-([\d]*)-([\d]*)-([\w]*)-([\w]*).txt'
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(f)]
for filename in files:
    match = re.match(filename_regex, filename)
    if match:
        protocol = match[1]
        buffer_size = match[2]
        packet_size = match[3]
        p2pdelay = match[4]

'''
#protocol = 'TcpWestwood'
protocol = 'TcpVegas'
#protocol = 'TcpCubic'
#protocol = 'TcpNewReno'
#protocol = 'TcpHighSpeed'
buffer_size = '1500000'
packet_size = '1400'
#p2pdelay = '0'
p2pdelay = '18'
'''
nodeNum = 6
filename_base = '-'.join([protocol, buffer_size, packet_size, p2pdelay])
#colors = 'bgrcmyk'
colors = 'brcmgyk'

host = host_subplot(111, axes_class=AA.Axes)
y_plots = []
multiplot_cnt = 0   # post-increment

data_wndw = float(args.data_wndw)
output_filename = ''

def value_to_plot(trace):
    if trace in ['DATA']:
        return 1
    if trace in ['CWND', 'RCWND', 'RTT']:
        return 2
    if trace in ['MMWAVESINR', 'LTESINR']:
        return 3

def get_y_lims(y_vals, trace):
    # should axes start from 0? or min(vals)? percentage padding?
    if trace == 'RTT':
        lims = min(y_vals), max(y_vals)
    else:
        lims = math.floor(min(y_vals)), math.ceil(max(y_vals))
    return lims

def get_label(trace):
    if trace == 'CWND' or trace == 'RCWND':
        return 'CWND size (packets)'
    if trace == 'RTT':
        return 'RTT (s)'
    if trace == 'DATA': 
        return 'Throughput (Mb/s)'  # MB? Mb?????????
    if trace == 'MMWAVESINR':
        return 'SINR (dB)'
    if trace == 'LTESINR':
        return 'SINR'

def new_y_axis_plot(x_vals, y_vals, trace):
    if multiplot_cnt == 0:
        PLOT = host
        LOCATION = 'left'
    else:
        PLOT = host.twinx()
        if multiplot_cnt == 1:
            LOCATION = 'right'
        else:
            LOCATION = 'right' if multiplot_cnt % 2 == 0 else 'left'
            OFFSET = (60, 0) if multiplot_cnt % 2 == 0 else (-60, 0)

        if multiplot_cnt >= 2:
            new_fixed_axis = PLOT.get_grid_helper().new_fixed_axis
            PLOT.axis[LOCATION] = new_fixed_axis(loc=LOCATION, axes=PLOT, offset=OFFSET)
            PLOT.axis[LOCATION].toggle(all=True)

    PLOT.set_ylabel(get_label(trace))
    PLOT.set_ylim(get_y_lims(y_vals, trace))

    p1, = PLOT.plot(x_vals, y_vals, label=get_label(trace))    # plot call

    PLOT.axis[LOCATION].toggle(all=True)
    PLOT.axis[LOCATION].label.set_color(p1.get_color())
    PLOT.axis[LOCATION].line.set_color(p1.get_color())
    PLOT.axis[LOCATION].major_ticks.set_color(p1.get_color())
    PLOT.axis[LOCATION].major_ticklabels.set_color(p1.get_color())

def data_trace(x_vals):
    #wndw = 0.1
    wndw = data_wndw
    wndw_start = 0.0
    wndw_end = wndw_start + wndw
    multiplier = 1/wndw

    wndw_cnt = 0
    packet_cnt = 0
    packets_list = [0]   # element: n of packets rcvd in 0.1s
    for packet_arrive_time in x_vals:
        if packet_arrive_time > wndw_start and packet_arrive_time < wndw_end:
            packets_list[wndw_cnt] += 1
        else:
            wndw_cnt += 1
            packets_list.append(0)
            wndw_start = wndw_end
            wndw_end = wndw_end + wndw

    x_vals, y_vals = [], []

    for i in range(len(packets_list)):
        x_val = i * wndw

        packetper100ms = packets_list[i]
        #print(packetper100ms)
        packetpers = packetper100ms * multiplier
        #print('  ' + str(packetpers))
        bytepers = packetpers * int(packet_size)
        kbytepers = bytepers / 1000
        #print('  ' + str(kbytepers) + ' KB/s')
        mbytepers = kbytepers / 1000
        #print('  ' + str(mbytepers) + ' MB/s')

        y_val = mbytepers

        x_vals.append(float(x_val))
        y_vals.append(int(y_val))

    return (x_vals, y_vals)

def plot_trace_file(nodes=None, trace=''):
    # nodes: only plot specified nodes' trace data (list)
    # trace: ['CWND', 'RCWND', 'RTT', 'DATA', 'MMWAVESINR', 'LTESINR']

    global multiplot_cnt, output_filename

    if not nodes: 
        nodes = ['1']
        output_filename += trace # TODO
    else:
        output_filename += '-'.join(['-'.join(nodes), trace]) # TODO

    if trace == 'MMWAVESINR':
        trace_filename = 'MmWaveSinrTime.txt'
    if trace == 'LTESINR':
        trace_filename = 'LteSinrTime.txt'
    
    for i in nodes:
        if trace in ['CWND', 'RCWND', 'RTT', 'DATA']:   
            trace_filename = '-'.join([filename_base, i, 'TCP', trace + '.txt'])

        plot_style = 's' if trace == 'RCWND' else '-'

        x_vals, y_vals = [], []

        with open(trace_filename, 'r') as f:
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
            (x_vals, y_vals) = data_trace(x_vals)

        #color_index = int(i)-1
        # color_index = (multiplot_cnt + int(i)-1) % len(colors)    # todo test
        color_index = multiplot_cnt
        ### this was used ##plt.plot(x_vals, y_vals, colors[color_index]+plot_style, linewidth=0.5, antialiased=False, label='Node '+i+' '+trace)
        #plt.plot(x_vals, y_vals, colors[int(i)-1], linestyle='s', markersize=2, linewidth=0.3, antialiased=False, label='Node '+i)

        
        plt.subplots_adjust(right=0.75)

        new_y_axis_plot(x_vals, y_vals, trace)
        
        host.set_xlabel("Time (s)")
        host.set_xlim(math.floor(min(x_vals)), math.ceil(max(x_vals)))
        host.legend()
        
        #plt.axis('tight')
        '''
        if len(nodes) == 1:
            plt.title('Node {} {}'.format(nodes[0], trace))
        elif len(nodes) == 6:
            plt.title('All nodes {}'.format(trace))
        elif len(nodes) > 1:
            plt.title('Nodes {} {}'.format(', '.join(nodes), trace))
        else:
            plt.title('Node 1-6 {}'.format(trace))
        if trace == 'DATA': 
            plt.suptitle('Data throughput')
            plt.title('interval = ' + str(data_wndw) + ' s')
        '''

    multiplot_cnt += 1

def multiplot_trace_files(nodes=None, traces=None):
    #2plt.figure(figsize=(11,4))

    for trace in traces:
        if trace != traces[0] and trace != traces[-1]: 
            global output_filename
            output_filename += '_'
        plot_trace_file(nodes=nodes, trace=trace)

multiplot_trace_files(nodes=args.nodes, traces=args.traces)

if not os.path.isdir('png'): os.makedirs('png')
plt.draw()
#plt.show()
#plt.savefig('./png/' + output_filename, bbox_inches='tight')
plt.savefig('./png/' + output_filename + '.png')



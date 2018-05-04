import os, sys, re
import matplotlib.style as mplstyle
mplstyle.use('fast')
import matplotlib.pyplot as plt

protocol = 'TcpVegas'
#protocol = 'TcpHighSpeed'
buffer_size = '1500000'
packet_size = '1400'
p2pdelay = '0'
nodeNum = 6
filename_base = '-'.join([protocol, buffer_size, packet_size, p2pdelay])
#colors = 'bgrcmyk'
colors = 'brcmgyk'

def plot_trace_file_3cols(nodes=None, trace=''):
    # nodes: only plot specified nodes' trace data (list)
    # trace: [CWND, RCWND, RTT]

    if not nodes: 
        nodes = ['1', '2', '3', '4', '5', '6']
        output_filename = trace + '.png'
    else:
        output_filename = '-'.join(['-'.join(nodes), trace + '.png'])
    
    for i in nodes:
        trace_filename = '-'.join([filename_base, i, 'TCP', trace + '.txt'])
        plot_style = 's' if trace == 'RCWND' else '-'

        x_vals, y_vals = [], []

        with open(trace_filename, 'r') as f:
            for line in f:
                #time, old, new = re.match('([0-9\.]*)\W*([0-9\.]*)\W*([0-9\.]*)\W*')
                linedata = re.findall('([0-9\.]*)\W*', line)
                x_val, y_val = linedata[0], linedata[2]

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

        plt.plot(x_vals, y_vals, colors[int(i)-1]+plot_style, linewidth=0.5, antialiased=False, label='Node '+i)
        #plt.plot(x_vals, y_vals, colors[int(i)-1], linestyle='s', markersize=2, linewidth=0.3, antialiased=False, label='Node '+i)
        
        plt.xlabel('time (s)')
        if trace == 'CWND' or trace == 'RCWND':
            plt.ylabel('CWND size (packets)')
        if trace == 'RTT':
            plt.ylabel('RTT (s)')
        #plt.axis('tight')
        if len(nodes) == 1:
            plt.title('Node {} {}'.format(nodes[0], trace))
        elif len(nodes) == 6:
            plt.title('All nodes {}'.format(trace))
        elif len(nodes) > 1:
            plt.title('Nodes {} {}'.format(', '.join(nodes), trace))
        else:
            plt.title('Node 1-6 {}'.format(trace))

    ax = plt.axes()
    #ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    #ax.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_major_locator(plt.AutoLocator())
    ax.yaxis.set_major_locator(plt.AutoLocator())
    ax.legend()

    #plt.show()
    plt.savefig('./png/' + output_filename, bbox_inches='tight')

if not os.path.isdir('png'): os.makedirs('png')
if len(sys.argv) == 2:
    if sys.argv[1] not in ['CWND', 'RCWND', 'RTT']: 
        print('Available arguments: "CWND", "RCWND", "RTT"')
        exit(0)
    plot_trace_file_3cols(trace=sys.argv[1])
elif len(sys.argv) == 3:
    plot_trace_file_3cols(nodes=[sys.argv[1]], trace=sys.argv[2])
elif len(sys.argv) > 3:
    plot_trace_file_3cols(nodes=sys.argv[1:-1], trace=sys.argv[-1])
else:
    plot_trace_file_3cols(nodes=[1], trace='RTT')



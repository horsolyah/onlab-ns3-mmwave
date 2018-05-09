import os, sys, re
import matplotlib.style as mplstyle
mplstyle.use('fast')
import matplotlib.pyplot as plt

protocol = 'TcpVegas'
#protocol = 'TcpCubic'
#protocol = 'TcpNewReno'
#protocol = 'TcpHighSpeed'
buffer_size = '1500000'
packet_size = '1400'
#p2pdelay = '0'
p2pdelay = '18'
nodeNum = 6
filename_base = '-'.join([protocol, buffer_size, packet_size, p2pdelay])
#colors = 'bgrcmyk'
colors = 'brcmgyk'

data_wndw = 0.1

def value_to_plot(trace):
    if trace in ['DATA']:
        return 1
    if trace in ['CWND', 'RCWND', 'RTT']:
        return 2
    if trace in ['MMWAVESINR', 'LTESINR']:
        return 3

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
    # trace: [CWND, RCWND, RTT]

    

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

        plt.figure(figsize=(11,4))
        plt.plot(x_vals, y_vals, colors[int(i)-1]+plot_style, linewidth=0.5, antialiased=False, label='Node '+i)
        #plt.plot(x_vals, y_vals, colors[int(i)-1], linestyle='s', markersize=2, linewidth=0.3, antialiased=False, label='Node '+i)
        
        plt.xlabel('time (s)')
        if trace == 'CWND' or trace == 'RCWND':
            plt.ylabel('CWND size (packets)')
        if trace == 'RTT':
            plt.ylabel('RTT (s)')
        if trace == 'DATA': 
            plt.ylabel('Throughput (MB/s)')
        if trace == 'MMWAVESINR':
            plt.ylabel('SINR (dB)')
        if trace == 'LTESINR':
            plt.ylabel('SINR')
        #plt.axis('tight')
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

    ax = plt.axes()
    #ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    #ax.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_major_locator(plt.AutoLocator())
    ax.yaxis.set_major_locator(plt.AutoLocator())
    ax.legend()

    #plt.show()
    #plt.savefig('./png/' + output_filename, bbox_inches='tight')
    plt.savefig('./png/' + output_filename)

if not os.path.isdir('png'): os.makedirs('png')
if len(sys.argv) == 2:
    if sys.argv[1] not in ['CWND', 'RCWND', 'RTT', 'DATA', 'MMWAVESINR', 'LTESINR']: 
        print('Available arguments: CWND, RCWND, RTT, DATA, MMWAVESINR, LTESINR')
        exit(0)
    plot_trace_file(trace=sys.argv[1])
elif len(sys.argv) == 3:
    plot_trace_file(nodes=[sys.argv[1]], trace=sys.argv[2])
elif len(sys.argv) > 3:
    plot_trace_file(nodes=sys.argv[1:-1], trace=sys.argv[-1])
else:
    print('Else.')



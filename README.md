## 5G network simulation experiments using the ns3-mmwave module
##### Code repository for my ns-3 mobile network simulation coursework, created for a Laboratory course at Budapest University of Technology and Economics.

![]()

![Map1](https://i.imgur.com/X9vuW7J.png)   ![Test1](https://i.imgur.com/vOAnmEz.png)


![Map2](https://i.imgur.com/w8B78OF.png) ![Test2](https://raw.githubusercontent.com/levesduzw/onlab-ns3-mmwave/master/szakdolgozat%20example%20outputs/plot%20colored%20axes/2_bbr.png)

![Wireshark Window Scaling](https://i.imgur.com/HP29Dwc.png) 

## Summary

Millimeter-wave is an undeveloped band of spectrum, planned to be used for high-speed communication in 5G mobile networks. 

Millimeter-wave data speeds dramatically decrease when the line of sight (LOS) between a UE and a base station is blocked by any objects (non-LOS scenario).

Communication using the TCP protocol can use one of many network _Congestion Avoidance_ algorithms. TCP wasn't designed with wireless communication in mind, so the protocol might mistake the mentioned dramatic speed drops as congestion on the link.


The main task was to explore the behavior of TCP's most used Congestion Avoidance algorithms, and to observe the effects of their usage in simulated mmWave mobility scenarios (involving LOS-NLOS transitions).

## Details
Dependencies:
- [ns-3 Network Simulator 3.27 + mmwave module v1.2 + TCP BBR implementation](https://github.com/levesduzw/szakdolgozat-SETUP-ns3-mmwave-tcpbbr)
- Python 3.6, matplotlib, tkinter (custom plotting script)

Custom test definition files ('...') are used for the simulation, involving one mmWave base station, one piece of User Equipment, and some "buildings". The UE's movement direction and speed are specified here, as well as the congestion avoidance algorithm to be used.

After a simulation in ns-3 is completed, the plotting script parses the trace files (txt, pcap). 

It then generates several plots from the data (Round-trip time, Congestion Window size, SINR). 

Other plots can be acquired from Wireshark manually (Throughput, Duplicate ACKs). 

By observing these plots, it's possible to identify the effects of
- the LOS-NLOS transitions
- the currently used CA algorithm

on the simulated transmission speed, among other metrics.



![TcpNewReno](https://i.imgur.com/DyjG3HF.png)

![TcpVegas](https://i.imgur.com/hayaEia.png)

## Etc

[__Presentation slides__](https://drive.google.com/file/d/1dY-uq6KDm_-kYY2W4T8BOVpMgbjO0lFM/view)

[__Written summary__](https://drive.google.com/file/d/1MmeWTPB4YD4IQd4W8dZWFICiiUP5qGoL/view?usp=sharing)




[Summary of official example script mmwave-tcp-indoor.cc](https://docs.google.com/document/d/1E7V21YlyQi88-cIJIRR27EwXFH24dsR1kpfJ2qRV8Lw/edit?usp=sharing)

[Scenarios](https://docs.google.com/document/d/1GB0Hwlg4CwLH5kQfJOYqBkfU2C4I246gBOQymoSd1dY/edit?usp=sharing)

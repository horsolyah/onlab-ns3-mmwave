## 5G hálózat szimulációs vizsgálata az ns-3 mmWave modul használatával
##### Code repository for my ns-3 mobile network simulation coursework, created for a Laboratory course at Budapest University of Technology and Economics.

![Scenario1](https://i.imgur.com/bn7DiyI.png) ![Scenario2](https://i.imgur.com/p6ieC4L.png)

## Summary

Millimeter-wave is an undeveloped band of spectrum, planned to be used for high-speed communication in 5G mobile networks. 

Millimeter-wave data speeds dramatically decrease when the line of sight (between a UE and a base station) is blocked by any objects (non-LOS scenario).

Communication using the TCP protocol can use one of many network congestion-avoidance algorithms. TCP wasn't designed with wireless communication in mind, so the protocol might mistake the mentioned dramatic speed drops as congestion on the link.


The main task was to explore the behavior of TCP's most used Congestion Avoidance algorithms, and to observe the effects of their usage in simulated mmWave mobility scenarios (involving LOS-NLOS transitions).

## Details

Dependencies:
- [ns-3 Network Simulator](https://www.nsnam.org/ns-3-28/download/)
- [ns-3 mmWave module](https://github.com/nyuwireless-unipd/ns3-mmwave)
- Python 3.6, matplotlib (custom plotting scripts)

[Summary of example script mmwave-tcp-indoor.cc](https://docs.google.com/document/d/1E7V21YlyQi88-cIJIRR27EwXFH24dsR1kpfJ2qRV8Lw/edit?usp=sharing)

[Scenarios](https://docs.google.com/document/d/1GB0Hwlg4CwLH5kQfJOYqBkfU2C4I246gBOQymoSd1dY/edit?usp=sharing)


#include "ns3/point-to-point-module.h"
#include "ns3/mmwave-helper.h"
#include "ns3/epc-helper.h"
#include "ns3/mmwave-point-to-point-epc-helper.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"
#include "ns3/point-to-point-helper.h"
#include "ns3/config-store.h"
#include <ns3/buildings-helper.h>
#include <ns3/buildings-module.h>
#include <ns3/packet.h>
#include <ns3/tag.h>

using namespace ns3;

/**
 * A script to simulate the DOWNLINK TCP data over mmWave links
 * with the mmWave devices and the LTE EPC.
 */
NS_LOG_COMPONENT_DEFINE ("mmWaveTCP_NLOS");

static void
CwndChange (Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd)
{
	*stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << oldCwnd << "\t" << newCwnd << std::endl;
}

static void
RttChange (Ptr<OutputStreamWrapper> stream, Time oldRtt, Time newRtt)
{
	*stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << oldRtt.GetSeconds () << "\t" << newRtt.GetSeconds () << std::endl;
}

static void
StateChange (Ptr<OutputStreamWrapper> stream, TcpSocket::TcpStates_t oldState, TcpSocket::TcpStates_t newState)
{
	std::cout << "(t=" << Simulator::Now ().GetSeconds () << ") " << "TCP State changed from " << oldState << " to " << newState << std::endl;
	*stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << oldState << "\t" << newState << std::endl;
}

static void
CongStateChange (Ptr<OutputStreamWrapper> stream, TcpSocketState::TcpCongState_t oldState, TcpSocketState::TcpCongState_t newState)
{
	std::cout << "(t=" << Simulator::Now ().GetSeconds () << ") " << "TCP CongState changed from " << oldState << " to " << newState << std::endl;
	*stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << oldState << "\t" << newState << std::endl;
}

static void Rx (Ptr<OutputStreamWrapper> stream, Ptr<const Packet> packet, const Address &from)
{
	*stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << packet->GetSize()<< std::endl;
}

/*static void Sstresh (Ptr<OutputStreamWrapper> stream, uint32_t oldSstresh, uint32_t newSstresh)
{
	*stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << oldSstresh << "\t" << newSstresh << std::endl;
}*/

void
ChangeSpeed(Ptr<Node>  n, Vector speed)
{
	n->GetObject<ConstantVelocityMobilityModel> ()->SetVelocity (speed);
}

void ue_move (Ptr<ConstantVelocityMobilityModel> m, Vector velocity_vector)
{
	m->SetVelocity (velocity_vector); 
	Vector pos = m->GetPosition ();
	std::cout << "(t=" << Simulator::Now ().GetSeconds () << ") " << "Moving from x=" << pos.x << ", y=" << pos.y << "    with velocity x=" << velocity_vector.x << ", y=" << velocity_vector.y << std::endl;
}

void ue_pos (Ptr<ConstantVelocityMobilityModel> m, Vector velocity_vector)
{
	Vector pos = m->GetPosition ();
	std::cout << "(t=" << Simulator::Now ().GetSeconds () << ") " << "UE is at x=" << pos.x << ", y=" << pos.y << "    with velocity x=" << velocity_vector.x << ", y=" << velocity_vector.y  << std::endl;
}


static void
Traces(uint16_t nodeNum, uint16_t remotehostNum, std::string protocol)
{
	AsciiTraceHelper asciiTraceHelper;

	std::ostringstream pathCW;
	pathCW<<"/NodeList/"<<nodeNum+2<<"/$ns3::TcpL4Protocol/SocketList/"<<remotehostNum<<"/CongestionWindow";
	std::ostringstream fileCW;
	fileCW<<protocol<<"-"<<nodeNum+1<<"-"<<remotehostNum<<"-TCP-CWND.txt";

	std::ostringstream pathRTT;
	pathRTT<<"/NodeList/"<<nodeNum+2<<"/$ns3::TcpL4Protocol/SocketList/"<<remotehostNum<<"/RTT";
	std::ostringstream fileRTT;
	fileRTT<<protocol<<"-"<<nodeNum+1<<"-"<<remotehostNum<<"-TCP-RTT.txt";

	std::ostringstream pathRCWnd;
	pathRCWnd<<"/NodeList/"<<nodeNum+2<<"/$ns3::TcpL4Protocol/SocketList/"<<remotehostNum<<"/RWND";
	std::ostringstream fileRCWnd;
	fileRCWnd<<protocol<<"-"<<nodeNum+1<<"-"<<remotehostNum<<"-TCP-RCWND.txt";

	std::ostringstream pathSTATE;
	pathSTATE<<"/NodeList/"<<nodeNum+2<<"/$ns3::TcpL4Protocol/SocketList/"<<remotehostNum<<"/State";
	std::ostringstream fileSTATE;
	fileSTATE<<protocol<<"-"<<nodeNum+1<<"-"<<remotehostNum<<"-TCP-STATE.txt";

	std::ostringstream pathCONGSTATE;
	pathCONGSTATE<<"/NodeList/"<<nodeNum+2<<"/$ns3::TcpL4Protocol/SocketList/"<<remotehostNum<<"/CongState";
	std::ostringstream fileCONGSTATE;
	fileCONGSTATE<<protocol<<"-"<<nodeNum+1<<"-"<<remotehostNum<<"-TCP-CONGSTATE.txt";

	Ptr<OutputStreamWrapper> stream1 = asciiTraceHelper.CreateFileStream (fileCW.str ().c_str ());
	Config::ConnectWithoutContext (pathCW.str ().c_str (), MakeBoundCallback(&CwndChange, stream1));

	Ptr<OutputStreamWrapper> stream2 = asciiTraceHelper.CreateFileStream (fileRTT.str ().c_str ());
	Config::ConnectWithoutContext (pathRTT.str ().c_str (), MakeBoundCallback(&RttChange, stream2));

	Ptr<OutputStreamWrapper> stream4 = asciiTraceHelper.CreateFileStream (fileRCWnd.str ().c_str ());
	Config::ConnectWithoutContext (pathRCWnd.str ().c_str (), MakeBoundCallback(&CwndChange, stream4));

	Ptr<OutputStreamWrapper> stream5 = asciiTraceHelper.CreateFileStream (fileSTATE.str ().c_str ());
	Config::ConnectWithoutContext (pathSTATE.str ().c_str (), MakeBoundCallback(&StateChange, stream5));

	Ptr<OutputStreamWrapper> stream6 = asciiTraceHelper.CreateFileStream (fileCONGSTATE.str ().c_str ());
	Config::ConnectWithoutContext (pathCONGSTATE.str ().c_str (), MakeBoundCallback(&CongStateChange, stream6));

}

static void set_protocol(std::string protocol) 
{
    if(protocol == "TcpNewReno")
	{
	Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpNewReno::GetTypeId ()));
	}
	else if (protocol == "TcpVegas")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpVegas::GetTypeId ()));
	}
	else if (protocol == "TcpLedbat")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpLedbat::GetTypeId ()));

	}
	else if (protocol == "TcpHighSpeed")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpHighSpeed::GetTypeId ()));

	}
	else if (protocol == "TcpCubic")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpCubic::GetTypeId ()));

	}
	else if (protocol == "TcpIllinois")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpIllinois::GetTypeId ()));

	}
	else if (protocol == "TcpHybla")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpHybla::GetTypeId ()));

	}
	else if (protocol == "TcpVeno")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpVeno::GetTypeId ()));

	}
	else if (protocol == "TcpWestwood")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpWestwood::GetTypeId ()));

	}
	else if (protocol == "TcpYeah")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpYeah::GetTypeId ()));

	}
	else if (protocol == "TcpBbr")
	{
		Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpBbr::GetTypeId ()));

	}
	else
	{
		std::cout<<protocol<<" Unkown protocol.\n";
	}
}

int
main (int argc, char *argv[])
{   

	Box building_box_1 = Box (37.5,50, 16.66,29.16, 0,50);
	Box building_box_2 = Box (37.5,50, -6.25,6.25, 0,50); 
	Box building_box_3 = Box (37.5,50, -29.16,-16.66, 0,50); 
	Vector UE_start_pos = Vector (75, -37.5, 1.5);
	Vector UE_velocity_vector = Vector (0.0, 6.25, 0.0);	// 50 / 8 = 6.25
	
	// LogComponentEnable("TcpCongestionOps", LOG_LEVEL_INFO);
	// LogComponentEnable("TcpSocketBase", LOG_LEVEL_INFO);

	uint16_t nodeNum = 1;
	double simStopTime = 3.51;
	bool harqEnabled = true;
	bool rlcAmEnabled = true;
	std::string protocol = "TcpBbr";
	//int bufferSize = 1000 *1000 * 3.5 * 0.4;
	int bufferSize = 1000 *1000 * 1.5;
	int packetSize = 1400;
	int p2pDelay = 9;
	// This 3GPP channel model example only demonstrate the pathloss model. The fast fading model is still in developing.

	// The available channel scenarios are 'RMa', 'UMa', 'UMi-StreetCanyon', 'InH-OfficeMixed', 'InH-OfficeOpen', 'InH-ShoppingMall'
	std::string scenario = "UMa";
	std::string condition = "a";

	CommandLine cmd;
//	cmd.AddValue("numEnb", "Number of eNBs", numEnb);
//	cmd.AddValue("numUe", "Number of UEs per eNB", numUe);
	cmd.AddValue("simTime", "Total duration of the simulation [s])", simStopTime);
//	cmd.AddValue("interPacketInterval", "Inter-packet interval [us])", interPacketInterval);
	cmd.AddValue("harq", "Enable Hybrid ARQ", harqEnabled);
	cmd.AddValue("rlcAm", "Enable RLC-AM", rlcAmEnabled);
	cmd.AddValue("protocol", "TCP protocol", protocol);
	cmd.AddValue("bufferSize", "buffer size", bufferSize);
	cmd.AddValue("packetSize", "packet size", packetSize);
	cmd.AddValue("p2pDelay","delay between server and PGW", p2pDelay);
	cmd.Parse(argc, argv);

	//Config::SetDefault ("ns3::TcpSocket::SegmentSize", UintegerValue (65535));
	Config::SetDefault ("ns3::TcpSocketBase::MinRto", TimeValue (MilliSeconds (200)));
	Config::SetDefault ("ns3::Ipv4L3Protocol::FragmentExpirationTimeout", TimeValue (Seconds (1)));
	Config::SetDefault ("ns3::TcpSocket::SegmentSize", UintegerValue (packetSize));
	Config::SetDefault ("ns3::TcpSocket::DelAckCount", UintegerValue (1));

	Config::SetDefault ("ns3::TcpSocket::SndBufSize", UintegerValue (131072*400));
	Config::SetDefault ("ns3::TcpSocket::RcvBufSize", UintegerValue (131072*400));


	Config::SetDefault ("ns3::MmWaveHelper::RlcAmEnabled", BooleanValue(rlcAmEnabled));
	Config::SetDefault ("ns3::MmWaveHelper::HarqEnabled", BooleanValue(harqEnabled));
	Config::SetDefault ("ns3::MmWaveFlexTtiMacScheduler::HarqEnabled", BooleanValue(true));
	Config::SetDefault ("ns3::MmWaveFlexTtiMaxWeightMacScheduler::HarqEnabled", BooleanValue(true));
	Config::SetDefault ("ns3::MmWaveFlexTtiMacScheduler::HarqEnabled", BooleanValue(true));
	Config::SetDefault ("ns3::LteRlcAm::PollRetransmitTimer", TimeValue(MilliSeconds(2.0)));
	Config::SetDefault ("ns3::LteRlcAm::ReorderingTimer", TimeValue(MilliSeconds(1.0)));
	Config::SetDefault ("ns3::LteRlcAm::StatusProhibitTimer", TimeValue(MilliSeconds(1.0)));
	Config::SetDefault ("ns3::LteRlcAm::ReportBufferStatusTimer", TimeValue(MilliSeconds(2.0)));
	Config::SetDefault ("ns3::LteRlcAm::MaxTxBufferSize", UintegerValue (bufferSize));
	Config::SetDefault ("ns3::LteRlcAm::EnableAQM", BooleanValue(true));
	Config::SetDefault ("ns3::QueueBase::MaxPackets", UintegerValue (100*1000));

	Config::SetDefault ("ns3::CoDelQueueDisc::Mode", StringValue ("QUEUE_DISC_MODE_PACKETS"));
	Config::SetDefault ("ns3::CoDelQueueDisc::MaxPackets", UintegerValue (50000));
	//Config::SetDefault ("ns3::CoDelQueue::Interval", StringValue ("500ms"));
	//Config::SetDefault ("ns3::CoDelQueue::Target", StringValue ("50ms"));

	//Config::SetDefault ("ns3::LteEnbRrc::SecondaryCellHandoverMode", EnumValue(LteEnbRrc::FIXED_TTT));

	
	Config::SetDefault ("ns3::TcpVegas::Alpha", UintegerValue (20));
	Config::SetDefault ("ns3::TcpVegas::Beta", UintegerValue (40));
	Config::SetDefault ("ns3::TcpVegas::Gamma", UintegerValue (2));



	Config::SetDefault ("ns3::MmWave3gppPropagationLossModel::ChannelCondition", StringValue(condition));
	Config::SetDefault ("ns3::MmWave3gppPropagationLossModel::Scenario", StringValue(scenario));
	Config::SetDefault ("ns3::MmWave3gppPropagationLossModel::OptionalNlos", BooleanValue(false));
	Config::SetDefault ("ns3::MmWave3gppPropagationLossModel::Shadowing", BooleanValue(true)); // enable or disable the shadowing effect
	Config::SetDefault ("ns3::MmWave3gppPropagationLossModel::InCar", BooleanValue(false)); // enable or disable the shadowing effect



	Config::SetDefault ("ns3::MmWave3gppChannel::UpdatePeriod", TimeValue (MilliSeconds (100))); // Set channel update period, 0 stands for no update.
	Config::SetDefault ("ns3::MmWave3gppChannel::CellScan", BooleanValue(false)); // Set true to use cell scanning method, false to use the default power method.
	Config::SetDefault ("ns3::MmWave3gppChannel::Blockage", BooleanValue(true)); // use blockage or not
	Config::SetDefault ("ns3::MmWave3gppChannel::PortraitMode", BooleanValue(true)); // use blockage model with UT in portrait mode
	Config::SetDefault ("ns3::MmWave3gppChannel::NumNonselfBlocking", IntegerValue(4)); // number of non-self blocking obstacles
	Config::SetDefault ("ns3::MmWave3gppChannel::BlockerSpeed", DoubleValue(1)); // speed of non-self blocking obstacles

	Config::SetDefault ("ns3::MmWavePhyMacCommon::NumHarqProcess", UintegerValue(100));

	Config::SetDefault ("ns3::MmWaveSpectrumPhy::FileName", StringValue(protocol+"-"+std::to_string(bufferSize)+"-"+std::to_string(packetSize)+"-"+std::to_string(p2pDelay)));

  	Config::SetDefault ("ns3::LteEnbRrc::OutageThreshold", DoubleValue (-50));


	double hBS = 0; //base station antenna height in meters;
	double hUT = 0; //user antenna height in meters;
	if(scenario.compare("RMa")==0)
	{
		hBS = 35;
		hUT = 1.5;
	}
	else if(scenario.compare("UMa")==0)
	{
		hBS = 25;
		hUT = 1.5;
	}
	else if (scenario.compare("UMi-StreetCanyon")==0)
	{
		hBS = 10;
		hUT = 1.5;
	}
	else if (scenario.compare("InH-OfficeMixed")==0 || scenario.compare("InH-OfficeOpen")==0 || scenario.compare("InH-ShoppingMall")==0)
	{
		hBS = 3;
		hUT = 1;
	}
	else
	{
		std::cout<<"Unkown scenario.\n";
		return 1;
	}


	Ptr<MmWaveHelper> mmwaveHelper = CreateObject<MmWaveHelper> ();

	mmwaveHelper->SetAttribute ("PathlossModel", StringValue ("ns3::MmWave3gppBuildingsPropagationLossModel"));
	mmwaveHelper->SetAttribute ("ChannelModel", StringValue ("ns3::MmWave3gppChannel"));

	mmwaveHelper->Initialize();
	mmwaveHelper->SetHarqEnabled(true);

	Ptr<MmWavePointToPointEpcHelper>  epcHelper = CreateObject<MmWavePointToPointEpcHelper> ();
	mmwaveHelper->SetEpcHelper (epcHelper);

	Ptr<Node> pgw = epcHelper->GetPgwNode ();


	// Create two RemoteHost objects
	NodeContainer remoteHostContainer;
	remoteHostContainer.Create (2);

	// Create internet router
	NodeContainer routerContainer;
	routerContainer.Create (1);

	InternetStackHelper internet;
	internet.Install (remoteHostContainer);
	internet.Install (routerContainer);

	
	Ipv4StaticRoutingHelper ipv4RoutingHelper;
	Ipv4InterfaceContainer internetIpIfaces;

	PointToPointHelper internetp2ph;
	internetp2ph.SetDeviceAttribute ("DataRate", DataRateValue (DataRate ("10Gb/s")));
	internetp2ph.SetDeviceAttribute ("Mtu", UintegerValue (1500));
	internetp2ph.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (2)));

	PointToPointHelper bottleneckp2ph;
	bottleneckp2ph.SetDeviceAttribute ("DataRate", DataRateValue (DataRate ("10Mb/s")));
	bottleneckp2ph.SetDeviceAttribute ("Mtu", UintegerValue (1500));
	bottleneckp2ph.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (7)));

	//  [remoteHost1]
	//                >---  [router]  --(bottleneck link)--  [pgw]
	//  [remoteHost2]
	//

	NetDeviceContainer bottleneckLink = bottleneckp2ph.Install (pgw, routerContainer.Get (0));
	Ipv4AddressHelper ipv4h;
	ipv4h.SetBase ("100.1.0.0", "255.255.0.0");
	internetIpIfaces = ipv4h.Assign (bottleneckLink);
	// interface 0 is localhost, 1 is the p2p device
	Ptr<Ipv4StaticRouting> routerStaticRouting = ipv4RoutingHelper.GetStaticRouting (routerContainer.Get (0)->GetObject<Ipv4> ());
	routerStaticRouting->AddNetworkRouteTo (Ipv4Address ("7.0.0.0"), Ipv4Mask ("255.255.0.0"), 1);	// if 2: acks retransmissions visible
	routerStaticRouting->AddNetworkRouteTo (Ipv4Address ("0.1.0.0"), Ipv4Mask ("255.255.0.0"), 2);
	routerStaticRouting->AddNetworkRouteTo (Ipv4Address ("1.1.0.0"), Ipv4Mask ("255.255.0.0"), 3);
	//routerStaticRouting->AddNetworkRouteTo (Ipv4Address ("100.1.0.0"), Ipv4Mask ("255.255.0.0"), 2);

	Ptr<Ipv4StaticRouting> pgwStaticRouting = ipv4RoutingHelper.GetStaticRouting (pgw->GetObject<Ipv4> ());
	pgwStaticRouting->AddNetworkRouteTo (Ipv4Address ("7.0.0.0"), Ipv4Mask ("255.255.0.0"), 1);	// if 1: forward packet to 7.0.0.0   if 2: acks retransmissions visible
	pgwStaticRouting->AddNetworkRouteTo (Ipv4Address ("0.1.0.0"), Ipv4Mask ("255.255.0.0"), 2); // if 2: seems ok, fails at router!
	pgwStaticRouting->AddNetworkRouteTo (Ipv4Address ("1.1.0.0"), Ipv4Mask ("255.255.0.0"), 2);

	for (uint16_t i = 0; i < 2; i++)
	{
 		if (i == 0) {
			set_protocol ("TcpBbr");	// primary sender is always TCP BBR
		} 
		else {
			set_protocol ("TcpBbr");	// secondary sender
			//set_protocol (protocol);	// secondary sender
		}

		Ptr<Node> remoteHost = remoteHostContainer.Get (i);
		NetDeviceContainer internetDevices = internetp2ph.Install (routerContainer.Get (0), remoteHost);	// pgw was here

		Ipv4AddressHelper ipv4h;
		std::ostringstream subnet;
		subnet<<i<<".1.0.0";
		ipv4h.SetBase (subnet.str ().c_str (), "255.255.0.0");
		internetIpIfaces = ipv4h.Assign (internetDevices);
		// interface 0 is localhost, 1 is the p2p device
		Ptr<Ipv4StaticRouting> remoteHostStaticRouting = ipv4RoutingHelper.GetStaticRouting (remoteHost->GetObject<Ipv4> ());
		remoteHostStaticRouting->AddNetworkRouteTo (Ipv4Address ("100.1.0.0"), Ipv4Mask ("255.255.0.0"), 1);
		Ptr<Ipv4StaticRouting> remoteHostStaticRouting2 = ipv4RoutingHelper.GetStaticRouting (remoteHost->GetObject<Ipv4> ());
		remoteHostStaticRouting2->AddNetworkRouteTo (Ipv4Address ("7.0.0.0"), Ipv4Mask ("255.255.0.0"), 1);

		//internetp2ph.EnablePcapAll("mmwave-sgi-capture");
		std::cout << "GetId(): " << remoteHost->GetId () << std::endl;
		internetp2ph.EnablePcap ("netdevice", remoteHost->GetId (), 1);
	}

	Ptr < Building > building1;
	building1 = Create<Building> ();
	building1->SetBoundaries (building_box_1);
	building1->SetNFloors (1);
	building1->SetNRoomsX (1);
	building1->SetNRoomsY (1);

	Ptr < Building > building2;
	building2 = Create<Building> ();
	building2->SetBoundaries (building_box_2);
	building2->SetNFloors (1);
	building2->SetNRoomsX (1);
	building2->SetNRoomsY (1);
	
	Ptr < Building > building3;
	building3 = Create<Building> ();
	building3->SetBoundaries (building_box_3);
	building3->SetNFloors (1);
	building3->SetNRoomsX (1);
	building3->SetNRoomsY (1);

	NodeContainer ueNodes;
	NodeContainer mmWaveEnbNodes;
	NodeContainer lteEnbNodes;
	NodeContainer allEnbNodes;
	mmWaveEnbNodes.Create(1);
	lteEnbNodes.Create(1);
	ueNodes.Create(nodeNum);
	allEnbNodes.Add(lteEnbNodes);
	allEnbNodes.Add(mmWaveEnbNodes);

	Ptr<ListPositionAllocator> enbPositionAlloc = CreateObject<ListPositionAllocator> ();
	enbPositionAlloc->Add (Vector (0.0, 0.0, hBS));

	MobilityHelper enbmobility;
	enbmobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
	enbmobility.SetPositionAllocator(enbPositionAlloc);
	enbmobility.Install (allEnbNodes);
	BuildingsHelper::Install (allEnbNodes);

	MobilityHelper uemobility;
	uemobility.SetMobilityModel ("ns3::ConstantVelocityMobilityModel");   
	Ptr<ListPositionAllocator> uePositionAlloc = CreateObject<ListPositionAllocator> ();
	//uePositionAlloc->Add (Vector (75.0, -30.0, hUT));
	UE_start_pos.z = hUT;
	uePositionAlloc->Add (UE_start_pos);
	uemobility.SetPositionAllocator (uePositionAlloc);
	uemobility.Install (ueNodes.Get (0));

	Ptr<ConstantVelocityMobilityModel> mob = ueNodes.Get (0)->GetObject<ConstantVelocityMobilityModel>();
	// uemobility->SetVelocity("Velocity", Vector3DValue (Vector(0.0, 20.0, 0.0)) );
	//mob->SetVelocity( UE_velocity_vector);   // direction and velocity of UE in m/s
	mob->SetVelocity (Vector (0, 0, 0));   // initially stationary
	Vector pos = mob->GetPosition ();
	std::cout << "Starting position: x=" << pos.x << ", y=" << pos.y << std::endl;

	BuildingsHelper::Install (ueNodes);

	// Install LTE Devices to the nodes
	NetDeviceContainer lteEnbDevs = mmwaveHelper->InstallLteEnbDevice (lteEnbNodes);
	NetDeviceContainer mmWaveEnbDevs = mmwaveHelper->InstallEnbDevice (mmWaveEnbNodes);
	NetDeviceContainer mcUeDevs;

	mcUeDevs = mmwaveHelper->InstallMcUeDevice (ueNodes);

	// Install the IP stack on the UEs
	// Assign IP address to UEs, and install applications
	internet.Install (ueNodes);
	Ipv4InterfaceContainer ueIpIface;
	ueIpIface = epcHelper->AssignUeIpv4Address (NetDeviceContainer (mcUeDevs));

	mmwaveHelper->AddX2Interface (lteEnbNodes, mmWaveEnbNodes);
	mmwaveHelper->AttachToClosestEnb (mcUeDevs, mmWaveEnbDevs, lteEnbDevs);
	mmwaveHelper->EnableTraces();

	ApplicationContainer sourceApps;
	ApplicationContainer sinkApps;
	uint16_t sinkPort = 20000;

	for (uint16_t i = 0; i < 2; i++)
	{
		// Set the default gateway for the UE
		Ptr<Node> ueNode = ueNodes.Get (0);
		Ptr<Ipv4StaticRouting> ueStaticRouting = ipv4RoutingHelper.GetStaticRouting (ueNode->GetObject<Ipv4> ());
		ueStaticRouting->SetDefaultRoute (epcHelper->GetUeDefaultGatewayAddress (), 1);

		// Install and start applications on UEs and remote host
		PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));
		sinkApps.Add (packetSinkHelper.Install (ueNodes.Get (0)));

		BulkSendHelper ftp ("ns3::TcpSocketFactory", InetSocketAddress (ueIpIface.GetAddress (0), sinkPort));
		sourceApps.Add (ftp.Install (remoteHostContainer.Get (i)));

		std::ostringstream fileName;
		fileName<<protocol+"-"+std::to_string(bufferSize)+"-"+std::to_string(packetSize)+"-"+std::to_string(p2pDelay)<<"-1-"<<i<<"-TCP-DATA.txt";	// nodenum fixed

		AsciiTraceHelper asciiTraceHelper;

		Ptr<OutputStreamWrapper> stream = asciiTraceHelper.CreateFileStream (fileName.str ().c_str ());
		sinkApps.Get(i)->TraceConnectWithoutContext("Rx",MakeBoundCallback (&Rx, stream));
		sourceApps.Get(i)->SetStartTime(Seconds (0.1+0.01*i));
		Simulator::Schedule (Seconds (0.1001+0.01*i), &Traces, 0, i, protocol+"-"+std::to_string(bufferSize)+"-"+std::to_string(packetSize)+"-"+std::to_string(p2pDelay));
		sourceApps.Get(i)->SetStopTime (Seconds (simStopTime));

		sinkPort++;
	}

	sinkApps.Start (Seconds (0.));
	sinkApps.Stop (Seconds (simStopTime));
	//sourceAppsUL.Start (Seconds (0.1));
	//sourceApps.Stop (Seconds (simStopTime));

	//internetp2ph.EnablePcapAll("mmwave-sgi-capture");
	//bottleneckp2ph.EnablePcapAll("mmwave-sgi-capture_bottleneck");
	BuildingsHelper::MakeMobilityModelConsistent ();

	Config::Set ("/NodeList/*/DeviceList/*/TxQueue/MaxPackets", UintegerValue (1000*1000));
	Config::Set ("/NodeList/*/DeviceList/*/TxQueue/MaxBytes", UintegerValue (1500*1000*1000));

	Simulator::Schedule (Seconds(0), &ue_move, mob, UE_velocity_vector);
	for (int i=0; i<simStopTime; i++) {
		Simulator::Schedule (Seconds(i), &ue_pos, mob, UE_velocity_vector);
	}
	Simulator::Stop (Seconds (simStopTime));
	Simulator::Run ();
	Simulator::Destroy ();

	return 0;

}


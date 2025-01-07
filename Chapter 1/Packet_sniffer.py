#this is an external example as it show how to sniff a network in windows system

'''
This Python script creates a raw socket to capture network packets.
Raw sockets allow access to lower-level networking details, typically used for packet sniffing or network diagnostics.
socket.AF_INET: Specifies IPv4 addressing.
socket.SOCK_RAW: Creates a raw socket to access packet-level data.
socket.IPPROTO_IP: Indicates capturing all IP packets.

Note: Raw sockets require administrative/root privileges.

socket.IP_HDRINCL: Ensures that captured packets include the IP headers, which contain metadata like source/destination IP, packet length, and protocols.
socket.SIO_RCVALL: Enables "promiscuous mode" to capture all packets on the network, not just those addressed to the local machine.
Note: Promiscuous mode might not be supported on all systems.
recvfrom(65565): Receives a packet up to 65,565 bytes in size.
The largest possible IPv4 packet size is 65,535 bytes (header + payload).
'''

import socket

#get Host's Ip address
HOST = socket.gethostbyname(socket.gethostname())

#create Raw socket
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

#bind the socket to host and port, port=0 indicate any available port
s.bind((HOST, 0))

#incloud IP header
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#enable promiscuous mode
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

#reveice packet
print(s.recvfrom(65535))

#disable promiscuous mode
#Turns off promiscuous mode after capturing all packet to avoid network issue or detection by IDS
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

'''

Note: if you want to execute the code you need to exit the app and change the property of the app you use, 
and enable "run as administrative privilege" then enter and execute it. 
it is recommended that you disable the administrative privilege once you have done.
'''
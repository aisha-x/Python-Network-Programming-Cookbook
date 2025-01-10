#Listing 1.3 ipv4 conversion
#!/usr/bin/env python
# Python Network Programming Cookbook,Second Edition -- Chapter - 1

import socket
from binascii import hexlify
from netaddr import IPAddress

#Convert an IP address from 32-bit packed binary format to string format
#help(socket.inet_ntoa)

#Convert an IP address in string format (123.45.67.89) to the 32-bit packed
#binary format used in low-level network functions.
#help(socket.inet_aton)

def ip4_addr_convertion():

    for ip_addr in ['127.0.0.1', '192.168.1.0']:

        packed_ip = socket.inet_aton(ip_addr) #convert ip string to its binary format
        unpacked_ip = socket.inet_ntoa(packed_ip) #convert binary format to string ip
        print(f"This ip address : {unpacked_ip}, represent the binary data in a hexadecimal format as : {hexlify(packed_ip)} ")


        print("-"*20)
        ip = IPAddress(ip_addr)
        print(f"This ipv4 address: {unpacked_ip}, represent in binay format as: {ip.bits()}")


ip4_addr_convertion()

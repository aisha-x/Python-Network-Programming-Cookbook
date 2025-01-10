#Lisiting 1.12 show how to write a simple SNTP client
#SNTP= simple network time protocol, it is a simple version of NTP
#!/usr/bin/env python
#Python Network Programming Cookbook,Second Edition - - Chapter - 1

import socket
from time import ctime
import struct


NTP_SER = '0.uk.pool.ntp.org'
TIME1970 =2208988800

def print_current_time_using_snmp():

    #initiate socket, ntp use udp connection
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #\x1b: Indicates the NTP mode and version in the first byte (the rest are padding bytes).
    data = '\x1b' + 47 * '\0' #Fills the rest of the packet with zeros (total 48 bytes).
    s.sendto(data.encode('utf-8'), (NTP_SER, 123))

    #Receive Response
    data, addr = s.recvfrom(1024)#buffer size
    #if there is data
    if data:
        print(f"Response Received from: {addr}")

    #unpack ntp response
    time = struct.unpack('!12I', data)[10]
    #Subtracts TIME1970 (the offset) to convert the timestamp from NTP epoch to Unix epoch.
    time -= TIME1970

    #print time
    print(f"\t converted time: {ctime(time)}")


print_current_time_using_snmp()

#Listing 1.11 show how to synchronize time with remote machine using ntp protocol
#ntp = Network time protocol, we will write client program to connecte to the remote machine using ntp protocol
# !/usr/bin/env python
#Python Network Programming Cookbook,Second Edition - - Chapter - 1

from time import ctime
import ntplib

def print_current_time():

    ntp_client = ntplib.NTPClient()
    #send request to remote server
    response = ntp_client.request('pool.ntp.org')
    print(f"Current time: {ctime(response.tx_time)}")
    #print(help(ctime))

print_current_time()

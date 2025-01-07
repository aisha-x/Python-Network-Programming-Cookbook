#Listing 1.6 Show socket timeout as follow
#!/usr/bin/env python
#Python Network Programming Cookbook, Second Edition -- Chapter - 1

import socket

def test_socket_time():

    #first make a socket instance
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Default Socket timeout: {s.gettimeout()}")
    print(f"Current socket Timeout: {s.settimeout(100)}")

test_socket_time()
#Listing 1.4 finding service name
#!/usr/bin/env python
#Python Network Programming Cookbook, Second Edition -- Chapter - 1

import socket

def finding_service_name():


    port_number = [80, 25, 69, 53, 443, 67]
    #use try to handle error in getservbyport function

    for port in port_number:
        try:
            tcp_serv = socket.getservbyport(port, 'tcp')
            print(f"TCP conn: Port number: {port} => {tcp_serv}")

        #OSError is raised, which is caught to avoid the program from breaking.
        except OSError:
            tcp_serv = None

        try:
            udp_serv = socket.getservbyport(port, 'udp')
            print(f"UPD conn: Port number: {port} => {udp_serv}")
        except OSError:
            udp_serv = None




finding_service_name()
#Listing 1.9 show how the socket changes to blocking and unblocking mood
#!/usr/bin/env python
#Python Network Programming Cookbook, Second Edition -- Chapter - 1

import socket

def test_socket_mode():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #setblocking(1) => blocking mode
    #setblocking(0) => nonblocking mode

    s.setblocking(1)
    s.settimeout(0.5)
    s.bind(('127.0.0.1', 0))

    socket_addr = s.getsockname()
    print("Trivial server runs on %s" % str(socket_addr))

    while (1):
        s.listen(1)

test_socket_mode()
'''
getsockname(...) method of socket.socket instance
    getsockname() -> address info

    Return the address of the local endpoint. The format depends on the
    address family. For IPv4 sockets, the address info is a pair
    (hostaddr, port). For IPv6 sockets, the address info is a 4-tuple
    (hostaddr, port, flowinfo, scope_id).
'''
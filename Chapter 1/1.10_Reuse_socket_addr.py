#Lisiting 1.10 show how to reuse socket address
#!/usr/bin/env python
#Python Network Programming Cookbook, Second Edition -- Chapter - 1

import socket

def reuse_socket_addr():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    old_state = s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print("Old state of reusing the socket address: %d " % old_state)
    set_opt = s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    new_state = s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print("New state of reusing the socket address: %d" % new_state)

    host = '127.0.0.1'
    local_port = 8282
    s.bind((host, local_port))
    s.listen(1)
    print(f"Host {host} Listening on port:{local_port} ")

    #accept connection
    while True:
        try:
            conn, addr = s.accept()
            print(f"Connected from {conn} by: {addr}")
        except KeyboardInterrupt:
            break
        except socket.error as msg:
            print("Error in socket connection %s " % msg)


reuse_socket_addr()
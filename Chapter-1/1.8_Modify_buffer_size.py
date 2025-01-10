#Listing 1.8 modify buffer size
#!/usr/bin/env python
#Python Network Programming Cookbook, Second Edition -- Chapter - 1

'''

What the Code Does
1- Creates a TCP socket.
2- Retrieves the initial send buffer size.
3- Disables the Nagle algorithm for low-latency communication.
4- Sets the send and receive buffer sizes to 4096 bytes.
5- Verifies the updated send buffer size.
Key Takeaways:
- SO_SNDBUF and SO_RCVBUF: Control the sizes of the send and receive buffers.
- Performance Tuning: Choose buffer sizes appropriate for your application's data flow and network characteristics.
- Nagle Algorithm (TCP_NODELAY): Disable for immediate data transmission when small packets are critical

getsockopt fetches the current size of the send buffer (SO_SNDBUF) at the socket level (SOL_SOCKET).
The buffer size determines how much data can be stored in the buffer before being sent over the network.
---
setsocketopt(): Disables the Nagle algorithm, which groups small packets into larger ones to reduce overhead.
Disabling it ensures data is sent immediately, useful for low-latency applications.
'''

import socket

SEND_BUF_SIZE = 4096
RECE_BUF_SIZE = 4096

def change_buffer_size():


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #get the size of the socket's send buffer
    buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print("Buffer size [before]: %d " % buf_size)

    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY,1)

    #setting new buffer sizes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECE_BUF_SIZE)

    #verify new buffer size
    #SOL= socket level, SO= socket option
    buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print("Buffer Size [After]: %d" % buf_size)

change_buffer_size()

#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 3
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications

import argparse

LOCAL_SERVER_HOST = 'localhost'
REMOTE_SERVER_HOST ='www.google.com'
BUFSIZE = 4096

# NOTE:
# asyncore is deprecated in Python 3.6+ and removed completely in Python 3.12
# The recommended replacement is asyncio which I wrote in 3.1-port_forwarding2

import asyncore
import socket

class PortForwarder(asyncore.dispatcher):
    """listen for incoming connections on a local port and set up
    a forwarding mechanism to the remote destination  """

    def __init__(self, ip,port, remoteip, remoteport, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
        print("Connected to: ", addr)
        Sender(Receiver(conn), self.remoteip, self.remoteport)

class Receiver(asyncore.dispatcher):
    """Handle incoming traffic from the local client and sent
    it to the Server (which talk to the remote server)"""
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.from_remote_buffer='' # data coming from client, going to the remote
        self.to_remote_buffer=''   # data coming from the remote via Sender, going to the client
        self.sender=None           # a reference to the Sender instance

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(BUFSIZE)
        self.from_remote_buffer += read

    def writable(self):
        """Check if there is data to send to the remote server"""
        return (len(self.from_remote_buffer ) > 0)

    def handle_write(self):
        """send data coming from remote back to the client"""
        send = self.send(self.to_remote_buffer)
        self.to_remote_buffer = self.to_remote_buffer[send:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()

class Sender(asyncore.dispatcher):
    """this handles connecting to the remote server and
    forwarding data from the client """

    def __init__(self, receiver, remoteaddr, remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        receiver.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        pass
    def handle_read(self):
        """read data from the remote server, then store to the Receiver's
        to_remote_buffer which will be written back to the client"""
        read = self.recv(BUFSIZE)
        self.receiver.to_remote_buffer += read

    def writable(self):
        """check if there is client data to send to the remote server"""
        return (len(self.receiver.from_remote_buffer) > 0)

    def handle_write(self):
        """ sends data from the Receiver's from_remote_buffer to the remote server"""
        send = self.send(self.receiver.from_remote_buffer)
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[send:]

    def handle_close(self):
        self.close()
        self.receiver.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Stackless Socket Server example')

    parser.add_argument('--local-host',action='store', dest='local_host', default=LOCAL_SERVER_HOST )
    parser.add_argument('--local-port', action='store', dest='local_port', type=int, required=True)
    parser.add_argument('--remote-host', action='store', dest='remote_host', default=REMOTE_SERVER_HOST)
    parser.add_argument('--remote-port', action='store', dest='remote_port', type=int, default=80)

    given_args = parser.parse_args()

    local_host, remote_host = given_args.local_host, given_args.remote_host
    local_port, remote_port = given_args.local_port, given_args.remote_port

    print("Starting port forwarding local %s:%s => remote %s:%s" %(local_host, local_port, remote_host, remote_port))

    PortForwarder(local_host, local_port, remote_host, remote_port)
    asyncore.loop()
#Listing 1.14 show how to write a simple udp echo client/server application
#!/usr/bin/env python
#Python Network Programming Cookbook,Second Edition -- Chapter - 1
#This program is optimized for Python 2.7.12and Python 3.5.2.
#It may run on any other version with/without modifications

import socket
import argparse

class Server:

    #create a udp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buff_size = 2048


    def __init__(self):

        parser = argparse.ArgumentParser(description="Socket UDP Server")
        parser.add_argument('--host', default='', type=str, action='store')
        parser.add_argument('--port', default=8888, type=int, action='store')

        #processing args
        given_args = parser.parse_args()
        self.host = given_args.host
        self.port = given_args.port


    def receive(self):

        #bind ip to port
        self.s.bind((self.host, self.port))

        while True:

            print("Waiting for client connection....")

            # reads the messages from the socket and returns the data and the client address
            data, addr = self.s.recvfrom(self.buff_size)
            print("Received %s byte from %s " % (len(data), addr))
            print("Data: %s" % data)
            if data:
                #send data back to specific address
                send = self.s.sendto(data, addr)
                print("Echo %s byte back to %s " % (send, addr))


if __name__ == '__main__':
    server = Server()
    server.receive()

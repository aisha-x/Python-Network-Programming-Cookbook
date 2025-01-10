#Listing 1.14 show how to write a simple udp echo client/server application
#!/usr/bin/env python
#Python Network Programming Cookbook,Second Edition -- Chapter - 1
#This program is optimized for Python 2.7.12and Python 3.5.2.
#It may run on any other version with/without modifications

import socket
import argparse


class Client:

    #create udp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buff_size = 2048

    def __init__(self):

        parser = argparse.ArgumentParser(description="Socket UDP Client")
        parser.add_argument('--host', default='localhost', type=str, action='store')
        parser.add_argument('--port', default=8888, type=int, action='store')

        #processing args
        given_args = parser.parse_args()
        self.host = given_args.host
        self.port = given_args.port

    def socket_connection(self):

        #connect to server
        try:
            self.s.connect((self.host, self.port))
            print(f"Connection to {self.host} on port {self.port} has been established!")
        except socket.gaierror as msg:
            print(f"Address-related Error connection to server {msg}")

        except socket.error as msg:
            print(f"Connection Error {msg}")


    def send_data(self):

        self.socket_connection()

        try:
            message = "Test.... test....can..you..hear...mee??"
            print("Sending... %s " % message)
            self.s.sendto(message.encode('utf-8'), (self.host, self.port))
            #receive response
            data, server = self.s.recvfrom(self.buff_size)
            print("Received %s" % data)

        finally:
            print("Closing Connection to the server")
            self.s.close()


if __name__ == '__main__':
    client = Client()
    client.send_data()



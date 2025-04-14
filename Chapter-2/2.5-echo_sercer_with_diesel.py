#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 2
# This program is optimized for Python 2.7.12.
# It will work with Python 3.5.2 once the depedencies for diesel are sorted out.
# It may run on any other version with/without modifications.
# You also need diesel library 3.0 or a later version.
# Make sure to install the dependencies beforehand.

import diesel
import argparse

class EchoServer(object):
    """ An Echo Server using Diesel """

    def handler(self, remote_addr):
        """ Returns the echo server"""
        host, port= remote_addr[0], remote_addr[1]
        print("Echo client connected from: %s:%d" %(host, port))
        while True:
            # loop to keep handling messages
            try:

                message = diesel.until_eol() # wait until client send msg
                your_message = ': '.join(['you said', message])
                # echo back client message
                diesel.send(your_message)
            except Exception as e:
                print("Exception: ", e)


def main(server_port):
    """ Set up and runs the Diesel application """
    app = diesel.Application()
    server = EchoServer() # register the EchoServer to handle connection on the specific port
    app.add_service(diesel.Service(server.handler(), server_port))

    app.run()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Echo server example with Diesel')

    parser.add_argument('--port', action="store", dest="port", type=int, required=True)

    given_args = parser.parse_args()
    port = given_args.port
    main(port)

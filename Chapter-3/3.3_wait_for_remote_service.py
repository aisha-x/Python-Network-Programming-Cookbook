#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 3
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import argparse
import socket
import errno
from time import time as now

DEFAULT_TIMEOUT= 120
DEFAULT_SERVER= "localhost"
DEFAULT_PORT= 80

class NetServiceChecker(object):
    """ wait for network service to come online """

    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket()

    def end_wait(self):
        self.sock.close()

    def check(self):

        if self.timeout:
            end_time = now() + self.timeout
        while True:
            try:
                if self.timeout:
                    next_timeout = end_time - now()  # now() method returns the current time in seconds
                    if next_timeout < 0:
                        # if the next_time reached less than 0, then the time is up
                        return False
                    else:
                        # calculates how much time is left before the deadline.
                        print("Setting socket next timeout %ss" % round(next_timeout))
                        self.sock.settimeout(next_timeout)
                self.sock.connect((self.host, self.port))
            except socket.timeout as e:
                if self.timeout:
                    return False
            except socket.error as e:
                print("Socket Error: %s " % e)
            else:
                self.end_wait()
                return True


if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Wait for network service")

    parser.add_argument('--host', action='store', dest='host', default=DEFAULT_SERVER)
    parser.add_argument('--port', action='store', type= int ,dest='port', default=DEFAULT_PORT)
    parser.add_argument('--time', action='store', type= int ,dest='timeout', default=DEFAULT_TIMEOUT)

    given_arg = parser.parse_args()
    host, port, timeout = given_arg.host, given_arg.port, given_arg.timeout

    service_check = NetServiceChecker(host, port, timeout)
    print("Checking for network service %s:%s..." % (host,port))
    if service_check.check():
        print("Service is available again!")
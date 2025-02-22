# listing 2.1 shows a sample code using ForkingMixIn in socket server application
# this scripts implements a simple multi-process echo server. this script is explained in chapter2_notes.txt
# !/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 2
# This program is optimized for Python 3.5.2.
# It may run on any other version with/without modifications.
# To make it run on Python 2.7.x, needs some changes due to API differences.
# begin with replacing "socketserver" with "SocketServer" throughout the program.
# Note: you will get an error if you execute it in windows, the ForkingMixIn class is not available on windows


import socket
import os
import threading
import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0 # tell the kernel to pick up a port dynamically
BUF_SIZE = 1024
ECHO_MSG = 'HelLO Echo Server'


class ForkingClinet:

    """A client to test Forking Server """
    def __init__(self, ip, port):

        #create a socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to the server
        self.s.connect((ip, port))

    def run(self):
        """Client playing with the server"""
        #send data to server
        current_process_id = os.getpid()
        print('PID %s Sending Echo Messages to the server: "%s"' % (current_process_id, ECHO_MSG))

        send_data_length = self.s.send(bytes(ECHO_MSG, 'utf-8'))
        print("Sent: %d character so far...." % send_data_length)

        #display server response
        response = self.s.recv(BUF_SIZE)
        print("PID %s received: %s" % (current_process_id, response[5:]) )

    def shutdown(self):
        """Clean up the client socket"""
        self.s.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    """Send the Echo Back to the client"""
    def handle(self):
        """Send the Echo Back to the client"""
        # received = str(sock.recv(1024), "utf-8")
        data = str(self.request.recv(BUF_SIZE, 'utf-8'))
        # return the current process id
        current_process_id = os.getpid()
        responses = '%s : %s' %(current_process_id, data)
        print("Server Sending Response: [Current process id: Data] = [%s]" % responses)

        self.request.send(bytes(responses, 'utf-8'))
        return

class ForkingServer(socketserver.ForkingMixIn , socketserver.TCPServer):

    """Nothing to add here, inherited everything necessary from parents"""
    pass


def main():
    # Launch the server
    Server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)

    # retrieve the port number
    ip, port = Server.server_address

    server_threading = threading.Thread(target=Server.serve_forever())
    server_threading.setDaemon(True) # dont hang on exit
    server_threading.start()
    print("Start loop running process: %s" % os.getpid())

    # launch the clients
    client1 = ForkingClinet(ip, port)
    client1.run()
    print("First client running...")

    client2 = ForkingClinet(ip, port)
    client2.run()
    print("Second client running...")

    # Clean them up
    Server.shutdown()
    client1.shutdown()
    client2.shutdown()
    Server.socket.shutdown()

if __name__ == '__main__':
    main()




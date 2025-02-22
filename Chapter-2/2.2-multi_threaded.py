#Listing 2.2 shows a sample code on the echo socket server using ThreadingMixIn
#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 2
# This program is optimized for Python 3.5.2.
# It may run on any other version with/without modifications.
# To make it run on Python 2.7.x, needs some changes due to API differences.
# begin with replacing "socketserver" with "SocketServer" throughout the program.
# See more: http://docs.python.org/2/library/socketserver.html
# See more: http://docs.python.org/3/library/socketserver.html


import os
import socket
import socketserver
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUFF_SIZE = 1024

def client(ip, port, message):

    # create a client to text threading Mixin server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message, 'utf-8'))
        response = sock.recv(BUFF_SIZE)
        print("Client received: %s " % response)
    finally:
        sock.close()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    """ An Example of threaded TCP request handler"""

    def handle(self):

        data = self.request.recv(BUFF_SIZE)
        cur_thread = threading.current_thread()
        response = "%s : %s " % (cur_thread.name, data) #name of the current thread along with the clients data
        self.request.sendall(bytes(response, 'utf-8'))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Nothing to add here, inherited everything necessary from parents"""
    pass

def main():

    # Run the server
    server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)

    ip, port = server.server_address # retrieve ip address

    # start a thread with the server -- one thread per request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread exits
    server_thread.daemon = True
    server_thread.start()
    print("Server Loop Running on thread: %s " % (server_thread.name))

    # Run Clients
    client(ip, port, "Hello From Client 1")
    client(ip, port, "Hello From Client 2")
    client(ip, port, "Hello From Client 3")

    # server clean up
    server.shutdown()

if __name__ == '__main__':
    main()

"""
 This recipe first creates a server thread and launches it in the background. Then it launches
 three test clients to send messages to the server. In response, the server echoes back the
 message to the clients. In the handle() method of the server's request handler, you can see
 that we retrieve the current thread information and print it. This should be different in each
 client connection.
 In this client/server conversation, the sendall() method has been used to guarantee the
 sending of all data without any loss:

"""
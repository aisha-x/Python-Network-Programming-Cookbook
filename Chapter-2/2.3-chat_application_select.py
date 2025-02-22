# listing 2.3 shows an example of chap application using select.select
# !/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 2
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import sys
import socket
import select
import struct
import argparse
import signal
import pickle

SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'

def send(channel, *args):

    # Serializes the given arguments into a byte stream.

    buffer = pickle.dumps(args)
    # Sends the size of the serialized data, and then the data itself over the socket.
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)

def receive(channel):

    # Reads the size of the incoming data
    size = struct.calcsize("L")
    size = channel.recv(size) # Receives the exact amount of data specified, ensuring no partial reads.
    try:
        # Deserializes the received data back to Python objects.
        size = socket.ntohl(struct.unpack("L", size) [0])
    except struct.error as e:
        return " "

    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    return pickle.loads(buf)[0]


class ChatServer(object):
    """ An example of chat server using select """

    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.output = [] # list output socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print("Server is listening on port: %s " % port)
        self.server.listen(backlog)
        # catch keyboard interrupter
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):

        """ Clean up client output"""
        # close the server
        print("Shutting down the server...")
        # Close existing client sockets
        for output in self.output:
            output.close()
        self.server.close()

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    # the main executable method of the chatserver
    def run(self):
        input = [self.server, sys.stdin]
        self.output = []
        running = True
        while running:
            try:
                readable, writable, exceptional = select.select(input, self.output, [])
            except select.error as e:
                break

            for sock in readable:
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print("Chat server: Got connection %d fromm %s " % (client.fileno(), address))
                    # read the login name
                    cname = receive(client).split("NAME: ")[1]
                    # compute client name and send back
                    self.clients += 1
                    send(client, "CLIENT: ", str(address[0]))
                    input.append(client)
                    self.clientmap[client] = (address, cname)
                    # send joining information to other clients
                    msg = "\n (Connected: New Client (%d) from %s )", (self.clients, self.get_client_name(client))
                    for output in self.output:
                        send(output, msg)
                    self.output.append(client)

                elif sock == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = False
                else:
                    # handle all others socket
                    try:
                        data = receive(sock)
                        if data:
                            # send as a new client's message
                            msg = '\n#[' + self.get_client_name(sock) + ']>>' + data
                            # send data to all except yourself
                            for output in self.output:
                                if output != sock:
                                    send(output, msg)
                        else:
                            print("Chat server: %d hang up" % sock.fileno())
                            self.clients -= 1
                            sock.close()
                            input.remove(sock)
                            self.output.remove(sock)

                            # sending client leaving information to other
                            msg = "\n (Now hung up: Client from %s)" % self.get_client_name(sock)

                            for output in self.output:
                                send(output, msg)

                    except socket.error as e:
                        input.remove(sock)
                        self.output.remove(sock)
        self.server.close()


class ChatClient(object):
    """ A command line chat client using select """
    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        # initial prompt
        self.prompt = '[' + '@'.join((name, socket.gethostname().split('.')[0]))

        # connect to the server
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print("Now connected to chat server@ port %d " % self.port)
            self.connected = True
            # send my name ...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']>'
        except socket.error as e:
            print("Failed to Connect to chat server @ port %d " % self.port)
            sys.exit(1)

    def run(self):
        """ Chat client main loop """
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                # wait for input from stdin and socket
                readable, writeable, exceptional = select.select([0, self.sock], [], [])

                for sock in readable:
                    if sock == 0:
                        data = sys.stdin.readline().strip()
                        if data: send(self.sock, data)
                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print("Client shutting down..")
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print("Client Interrupted ..""")
                self.sock.close()
                break

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Socket server example with select")

    parser.add_argument('--name', action='store', dest="name", required=True)
    parser.add_argument('--port', action='store', dest="port", type=int, required=True)

    # processing arguments
    given_args = parser.parse_args()
    name = given_args.name
    port = given_args.port

    if name == CHAT_SERVER_NAME.lower():
        server = ChatServer(port)
        server.run()
    else:
        client = ChatClient(name=name, port=port)
        client.run()




'''
How to run the code:
first execute this command to lunch the server 
python 2.3-chat_application_select.py --name=server --port=8888

then open new terminals for clients to join the chat
python 2.3-chat_application_select.py --name=client1 --port=8888
python 2.3-chat_application_select.py --name=client2 --port=8888
 


'''

# listing 2.3 shows an example of chap application using select.select
# !/usr/bin/env python.
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
    # Loops until all the expected bytes are received
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    # Converts the received byte stream back into the original Python object
    return pickle.loads(buf)[0]


class ChatServer(object):
    """ An example of chat server using select """

    def __init__(self, port, backlog=5):
        self.clients = 0     # Keeps track of connected clients.
        self.clientmap = {}  # stores client info (IP, name).
        self.output = []     # A list of client sockets for broadcasting messages.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow using the same port number
        self.server.bind((SERVER_HOST, port))
        print("Server is listening on port: %s " % port)
        self.server.listen(backlog)
        # catch keyboard interrupter
        signal.signal(signal.SIGINT, self.sighandler) # Catches Ctrl+C (SIGINT) to gracefully close connections

    def sighandler(self, signum, frame):

        """ Handles cleanup when the server shuts down (e.g., due to Ctrl+C). """
        # close the server
        print("Shutting down the server...")
        # Close existing client sockets
        for output in self.output:
            output.close()
        self.server.close()

    def get_client_name(self, client):

        """ Retrieves the nickname and IP address of a client. """
        info = self.clientmap[client]     # {client_socket: ((IP, port), nickname)}
        host, name = info[0][0], info[1]  # info[0][0] → Client’s IP address. info[1] → Client’s nickname.
        return '@'.join((name, host))     # Outputs "nickname@IP"


    def run(self):
        """ This is the main loop of the chat server.
        It manages client connections, incoming messages, and broadcasting messages. """

        input = [self.server, sys.stdin]  # listen for new client connection and allow server-side commands
        self.output = []   # Stores client sockets that are ready for sending messages.
        running = True     # Keeps the server running in a loop.
        while running:
            try:
                # select.select() monitors multiple sockets simultaneously. it returns three lists.
                # readable: Sockets that are ready to read (clients sending messages).
                # writable: Sockets that are ready to send data. exceptional: Sockets with errors.
                readable, writable, exceptional = select.select(input, self.output, [])
            except select.error as e:
                break

            for sock in readable:
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print("Chat server: Got connection %d from %s " % (client.fileno(), address))
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
                    # handle client message
                    try:
                        data = receive(sock)
                        if data:
                            # send as a new client's message. the message format is:
                            # #[nickname@ip]>> message
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

                    except sock.error as e:
                        input.remove(sock)
                        self.output.remove(sock)
        self.server.close()


class ChatClient(object):
    """ This is the client-side of the chat application.
    It connects to the server, sends messages, and listens for incoming messages.
 """
    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name  # store the client name
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
            # If successful, sets self.connected to True
            self.connected = True
            # Sends the client's nickname (NAME: <nickname>) to the server
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)     # The server sends back CLIENT: <IP>, confirming the connection.
            addr = data.split('CLIENT: ')[1]
            # The client's prompt is updated to include its assigned IP address.
            self.prompt = '[' + '@'.join((self.name, addr)) + ']>'
        except socket.error as e:
            print("Failed to Connect to chat server @ port %d " % self.port)
            sys.exit(1)

    def run(self):
        """ Runs continuously while the client is connected. """
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                # wait for input from stdin and socket
                # 0 → Standard input (User typing a message).
                # self.sock → Socket (Messages from the server).
                readable, writeable, exceptional = select.select([0, self.sock], [], [])

                for sock in readable:
                    if sock == 0:
                        # handle user input
                        data = sys.stdin.readline().strip()
                        if data: send(self.sock, data)  # If user types a message, it is sent to the server.

                    elif sock == self.sock:
                        # handle incoming messages from the server
                        data = receive(self.sock)
                        if not data:
                            # If the server closes the connection, the client shuts down.
                            print("Client shutting down..")
                            self.connected = False
                            break
                        else:
                            # If the server sends a message, it is displayed on the screen.
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                # If the user presses Ctrl+C, the client disconnects safely.
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



"""
usage:
first launch the server by typing in terminal 
python 2.3_chat_application.py --name=server --port=8888

in another terminal launch client 
python 2.3_chat_application.py --name=client1 --port=8888

another terminal 
python 2.3_chat_application.py --name=client2 --port=8888

"""

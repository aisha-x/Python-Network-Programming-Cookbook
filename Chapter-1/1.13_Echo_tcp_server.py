#Listing 1.13 show how to write a simple TCP echo client/server application
'''
this is the final project in Chapter-1.
original code has been edited.

steps:
1- we create the server.
2- we set the reuse address so that we can run the server as many times as we need.
3- We bind the socket to the given port on our local machine.
3- In the listening stage, we make sure we listen to multiple clients in a queue using the backlog argument to the listen() method.
4- Finally, we wait for the client to be connected and send some data to the server.
5- When the data is received, the server echoes back the data to the client.

'''

import socket
import argparse


class Server:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_payload = 2048 #buffer size
    backelog = 5

    def __init__(self):


        parser = argparse.ArgumentParser(description="Socket TCP Server")
        parser.add_argument('--host', action='store', type=str, default='', help="Host to bind the server")
        parser.add_argument('--port', action='store',type=int, default=8888, help="Port to bind the server")

        #processing passed arguments
        give_args = parser.parse_args()
        self.host = give_args.host
        self.port = give_args.port





    def receive(self):

        set_opt = self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.s.bind((self.host, self.port))
        self.s.listen(self.backelog)

        while True:
            print("Waiting to receive messages from client")
            conn, addr = self.s.accept()
            print(f"connection {conn} of the address {addr}")
            data = conn.recv(self.data_payload)
            if data:
                print("Data: %s " % data)
                conn.send(data)
                print("send %s byte back to %s" % (data, addr))
            #end connection
            conn.close()





if __name__ == "__main__":
    server = Server()
    server.receive()




'''
Example usage:
first execute "python 1.13_Echo_tcp_server.py" in one terminal
second execute "python 1.13_Echo_tcp_client.py" on another terminal

the output should be like this:
on 1.13_Echo_tcp_client.py  terminal:

Connection to 127.0.0.1 on port 8888 has been established!
enter the message you want to be echoed: hellllllllllllllllloooooooo
Sending... hellllllllllllllllloooooooo
Received Data b'hellllllllllllll'
Received Data b'llloooooooo'
Cloning connection to the server....

on 1.13_Echo_tcp_server.py terminal:

Host  listening on port 8888
Waiting to receive messages from client
Data: b'hellllllllllllllllloooooooo'
send b'hellllllllllllllllloooooooo' byte back to ('127.0.0.1', 56833)
Waiting to receive messages from client




'''
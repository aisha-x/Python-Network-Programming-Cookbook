#Listing 1.13 show how to write a simple TCP echo client/server application

import socket
import argparse


class Client:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):


        parser = argparse.ArgumentParser(description="Socket TCP Client")
        parser.add_argument('--host', action='store', type=str, default='localhost', help="Serve's IP")
        parser.add_argument('--port', action='store', type=int, default=8888, help="Server's port")

        # processing passed arguments
        give_args = parser.parse_args()
        self.host = give_args.host
        self.port = give_args.port

    def connecting_socket(self):


        try:
            self.s.connect((self.host, self.port))
            #handle connection errors
            print(f"Connection to {self.host} on port {self.port} has been established!")
        except socket.gaierror as msg:
            print(f"Address-related Error connection to server {msg}")
        except socket.error as msg:
            print(f"Connection Error {msg}")


    def send_data(self):

        self.connecting_socket()
        #handle sending data
        try:
            data = input("enter the message you want to be echoed: ")
            print("Sending... %s" % data)
            self.s.sendall(data.encode('utf-8'))
            amount_recv = 0
            amount_expected = len(data)
            while amount_recv < amount_expected:
                data = self.s.recv(16)
                amount_recv += len(data)
                print("Received Data %s " % data)

        except socket.error as msg:
            print("Socket Error %s " % msg)
        except Exception as e:
            print("Other Exception %s" % e)
        finally:
            print("Closing connection to the server....")
            self.s.close()


if __name__ == "__main__":
    client = Client()
    client.send_data()

# python 1.13_Echo_tcp_client.py --host='127.0.0.1' --port=8888
# or just type => python 1.13_Echo_tcp_client.py



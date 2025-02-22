# Exercise-2 Echo server-client


import socket
import argparse

HOST = socket.gethostname()
PORT = 8888


class Server:

    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))

    def receive(self):

        try:

            self.sock.listen(2)
            print("Server is listing on port %s " % PORT)

            while True:
                conn, addr = self.sock.accept()
                print(f"Got connection from {addr}")
                data = conn.recv(1024)
                print("Data received: %s " % data)
                if data:
                    conn.send(data)
                    print(f"send byte {data} back to {addr}")
                conn.close()

        except socket.error as e:
            print("Socket error-1 %s" % e)
            self.sock.close()

class Clinet:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

    def send(self):

        try:
            message = input("Enter message to be echoed: ")
            self.sock.sendall(message.encode("utf"))
            amount_received = 0
            while amount_received < len(message):
                data = self.sock.recv(16)
                amount_received += len(data)
                print("Received %s " % data)
        except socket.error as e:
            print("Socket error-2 %s " % e)
            self.sock.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Simple Echo client-server socket")

    parser.add_argument("--name", action="store", dest="name", required=True)

    given_args = parser.parse_args()
    name = given_args.name

    if name.lower() == "server":
        Server = Server()
        Server.receive()
    else:
        Client = Clinet()
        Client.send()
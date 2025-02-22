# Exercise-1. 
# Client and server communicating with each other



import socket
import argparse

HOST = socket.gethostname()
PORT = 8888


class Server:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def receive(self):
        """ handle client messages """
        try:

            self.sock.bind((HOST, PORT))
            self.sock.listen(2)
            print(f"Server is listening on port: {PORT}")
            client, addr = self.sock.accept()  # the address info is a pair (hostaddr, port)
            print(f"Got connection from {addr}")

            while True:
                data = client.recv(1024).decode()
                print("Data: %s " % data)
                message = input("Server ->")
                client.send(message.encode("utf-8"))


        except socket.error as e:
            print(" Socket error-1 %s" % e)
            self.sock.close()


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        print("Connected to the server on port %s" % PORT)

    def send(self):

        try:
            message = input("Client -> ")

            while message.lower().strip() != 'bye':
                self.sock.send(message.encode("utf-8"))
                data = self.sock.recv(1024).decode()
                print("Received from the server:  %s " % data)
                message = input("Client -> ")

            self.sock.send("the Client has left the chat".encode("utf-8"))
            self.sock.close()
        except socket.error as e:
            print(" Socket Error-2: %s " % e)
            self.sock.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Simple client-server socket")

    parser.add_argument("--name", action="store", dest="name", required=True)

    given_args = parser.parse_args()
    name = given_args.name

    if name.lower() == "server":
        Server = Server()
        Server.receive()
    else:
        Client = Client()
        Client.send()









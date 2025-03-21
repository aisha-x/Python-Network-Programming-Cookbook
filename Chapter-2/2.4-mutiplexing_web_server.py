 # Listing 2.4 Simple web server using select.epoll
 #!/usr/bin/env python
 # Python Network Programming Cookbook, Second Edition -- Chapter - 2
 # This program is optimized for Python 2.7.12 and Python 3.5.2.
 # It may run on any other version with/without modifications.

 import socket
 import argparse
 import select

 SERVER_HOST= "localhost"

 # End of line marker used to detect the end of HTTP headers

 EOL1 = b'\n\n'
 EOL2 = b'\n\r\n'

 # A simple HTTP response that the server send back to clients
 SERVER_RESPONSE = b""""Hello from Epoll Server!"""

 class EpollServer(object):

     """ A socket server using Epoll """
     def __init__(self, host=SERVER_HOST, port=0):

         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         self.sock.bind((host, port))
         self.sock.listen(1)
         self.sock.setblocking(0) # for better performance
         self.sock.setsockopt(socket.IPPROTO_IP, socket.TCP_NODELAY, 1) # for low-latency transmission
         print("Start Epoll Server...")
         self.epoll = select.epoll()
         # register the socket file descriptor for EPOLLIN (read event)
         self.epoll.register(self.sock.fileno(),select.EPOLLIN)

     def run(self):

         """ Execute Epoll Server operation """
         try:

             # use a polling loop to wait for events,
             #  use dictionaries to track connections, responses and requests
             connections = {}
             requests = {}
             responses = {}

             while True:
                 events = self.epoll.poll(1)
                 for fileno, event in events:
                     if fileno == self.sock.fileno():

                         connection, addr = self.sock.accept() # accept new conn
                         connection.setblocking(0)             # set it to non-blocking
                         # Register it to monitor incoming data with EPOLLIN
                         self.epoll.register(connection.fileno(), select.EPOLLIN)
                         # then initiate an empty request and predefined response for that connection
                         connections[connection.fileno()] = connection
                         requests[connection.fileno()] = b''
                         responses[connection.fileno()] = SERVER_RESPONSE

                     elif event & select.EPOLLIN:
                         # reading client data (EPOLLIN Event)
                         # accumulate data in the requests dictionary
                         requests[fileno] += connections[fileno].recv(1024)
                         # Checks for end-of-line markers (EOL1, EOL2) to determine the end of the HTTP request.
                         if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                             # Modifies the epoll registration to EPOLLOUT to prepare for sending a response.
                             self.epoll.modify(fileno, select.EPOLLOUT)
                             print('-'*40 + '\n' + requests[fileno].decode()[:-2])

                     elif event & select.EPOLLOUT:
                         # Sending Responses (EPOLLOUT events)
                         byrewritten = connections[fileno].send(responses[fileno])
                         # adjusts the response buffer after sending part of it
                         # close the connection when the entire response is sent
                         responses[fileno] = responses[fileno][byrewritten:]
                         if len(responses[fileno]) == 0:
                             self.epoll.modify(fileno,0)
                             connections[fileno].shutdown(socket.SHUT_RDWR)

                     elif event & select.EPOLLHUP:
                         # handle hang-up and client disconnections
                         self.epoll.unregister(fileno)
                         connections[fileno].close()
                         del connections[fileno]

         finally:
             # Cleanup. ensure the cleanup of the resources (epoll and socket)
             # when the server shutdown
             self.epoll.unregister(self.sock.fileno())
             self.epoll.close()
             self.sock.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Socket Server Example with Epoll")
    parser.add_argument('--port', action='store', dest='port', type=int, required=True)

    given_arg = parser.parse_args()
    port = given_arg.port
    server = EpollServer(host=SERVER_HOST ,port=port)
    server.run()


"""
How to Run it

If you run this script and access the web server from your browsers, such as Google
Chrome or Mozilla Firefox, by entering http://localhost:8800/, the following output
will be shown in the console:
 
  python3 2.4-multiplexing_web_server.py --port=8800
Start Epoll Server...
----------------------------------------
GET / HTTP/1.1
Host: localhost:8800
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1

----------------------------------------
GET /favicon.ico HTTP/1.1
Host: localhost:8800
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: image/avif,image/webp,*/*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://localhost:8800/
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors


"""